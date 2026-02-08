from PyQt6.QtCore import QObject, pyqtSignal, QTimer

class CalcCRC(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)

    def crc16(self, data: bytes) -> int:
        crc = 0xFFFF
        for b in data:
            crc ^= b << 8
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ 0x1021
                else:
                    crc <<= 1
                crc &= 0xFFFF
        return crc


