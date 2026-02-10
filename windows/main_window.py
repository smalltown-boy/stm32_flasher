from PyQt6.QtWidgets import QMainWindow
from ui.ui_main import Ui_MainWindow

from network.udp_client import UdpClient
from file.file_manager import FileManager
from parser.data_parser import DataParser
from crc.crc import CalcCRC
from history.history_manager import HistoryManager

from enum import Enum

class FlashState(Enum):
    IDLE = 0
    WAIT_ERASE = 1
    SEND_DATA = 2
    WAIT_ACK = 3
    SEND_CRC = 4
    DONE = 5

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Objects
        self.udp = UdpClient(self)
        self.parser = DataParser(self)
        self.file = FileManager(self, self.pathEdit)
        self.calc_crc = CalcCRC(self)
        self.history = HistoryManager(self)
        
        # Variables
        self.offset = 0
        self.crc = 0
        self.firmware = 0
        
        # State
        self.firmware_loaded = False
        self.waiting_flash_ready = False
        
        self.flash_state = FlashState.IDLE

        # Logs
        self.udp.log.connect(self.logBrowser.append)
        self.udp.error.connect(self.logBrowser.append)
        self.parser.log.connect(self.logBrowser.append)
        
        self.parser.response.connect(self.on_response_code)

        # Data
        self.udp.dataReceived.connect(self.on_udp_data)

        # Buttons
        self.buttonConnect.clicked.connect(self.on_connect_clicked)
        self.buttonAddFile.clicked.connect(self.on_addFirmware_clicked)
        self.buttonErase.clicked.connect(self.on_eraseMCU_clicked)
        self.buttonWriteFlash.clicked.connect(self.on_writeFirmware_clicked)
        self.buttonClear.clicked.connect(self.on_clearLog_clicked)
        
        # 
        self.history.attach_to_lineedit(self.ipEdit)

    def on_connect_clicked(self):
        address = self.ipEdit.text().strip()

        if ":" not in address:
            self.logBrowser.append("Invalid format (ip:port)")
            return

        ip, port = address.split(":", 1)
        self.udp.open(ip, int(port))
        
        self.history.add_address(address)
        self.history.save_history()
        self.history.refresh_completer()

    def on_addFirmware_clicked(self):
        self.firmware = self.file.open_file()
        if self.firmware:
            self.crc = self.calc_crc.crc16(self.firmware)
            self.logBrowser.append("Firmware file opened")
            self.logBrowser.append(f"CRC16 : 0x{self.crc:04X}")
            self.firmware_loaded = True
        else:
            self.firmware_loaded = False

    def on_eraseMCU_clicked(self):
        self.logBrowser.append("Sending chip erase command...")
        self.waiting_flash_ready = True
        self.udp.send(b'\xDD')
        
    def on_writeFirmware_clicked(self):
        if not self.firmware_loaded:
            self.logBrowser.append("Firmware file not open.")
            return
        
        self.offset = 0
        self.flash_state = FlashState.WAIT_ERASE        
        self.logBrowser.append("Sending firmware command...")
        self.waiting_flash_ready = False
        self.udp.send(b'\xAA')

    def on_udp_data(self, data: bytes):
        self.logBrowser.append(f"RX: {data}")
        self.parser.pars_data(data)
        
    def send_next_chunk(self):
        if self.offset >= len(self.firmware):
            self.logBrowser.append("Sending CRC...")
            packet = b'\x01\xEE' + self.crc.to_bytes(2, 'big')
            self.flash_state = FlashState.SEND_CRC
            self.udp.send(packet)
            return

        chunk = self.firmware[self.offset:self.offset + 1024]

        if len(chunk) % 4:
            chunk += b'\xFF' * (4 - len(chunk) % 4)

        packet = b'\x01\xFF' + len(chunk).to_bytes(2, 'big') + chunk
        self.logBrowser.append(f"[TX] offset={self.offset} size={len(chunk)}")

        self.flash_state = FlashState.WAIT_ACK
        self.udp.send(packet)

        
    def on_response_code(self, code: int):
        if code == 0xBB and self.flash_state == FlashState.WAIT_ERASE:
            self.logBrowser.append("Erase complete, start flashing")
            self.flash_state = FlashState.SEND_DATA
            self.send_next_chunk()

        elif code == 0xFF and self.flash_state == FlashState.WAIT_ACK:
            self.offset += 1024
            self.update_progress()
            self.flash_state = FlashState.SEND_DATA
            self.send_next_chunk()

        elif code == 0xE2 and self.flash_state == FlashState.SEND_CRC:
            self.logBrowser.append("Update successful")
            self.flash_state = FlashState.DONE

        elif code == 0xE1:
            self.logBrowser.append("CRC mismatch")

        else:
            self.logBrowser.append(f"Unexpected code: 0x{code:02X}")
            
    def update_progress(self):
        if not self.firmware:
            return

        percent = int((self.offset / len(self.firmware)) * 100)
        percent = min(percent, 100)
        self.progressBar.setValue(percent)
        
    def on_clearLog_clicked(self):
        self.logBrowser.clear()

