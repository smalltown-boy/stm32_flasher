from PyQt6.QtCore import QSettings, QObject

class AppSettings(QObject):

    FLASH_START = "STM32 MEMORY SETTINGS/START FLASH ADDR"
    FLASH_SIZE = "STM32 MEMORY SETTINGS/FLASH SIZE"
    RAM_START = "STM32 MEMORY SETTINGS/START RAM ADDR"
    RAM_SIZE = "STM32 MEMORY SETTINGS/RAM SIZE"
    USE_OBJCOPY = "CONVERSION SETTINGS/USE OBJCOPY"
    OBJCOPY_PATH = "CONVERSION SETTINGS/PATH OBJCOPY"
    SAVING_ADDRESS = "INPUT HINTS/SAVING ADDRESS"

    def __init__(self):
        super().__init__()

        self.settings = QSettings("app_settings.ini", QSettings.Format.IniFormat)
        self.load_settings()

    def load_settings(self):
        self.flash_start_addr = self.settings.value(self.FLASH_START, "0x08000000", type=str)
        self.flash_size = self.settings.value(self.FLASH_SIZE, 480, type=int)
        self.ram_start_addr = self.settings.value(self.RAM_START, "0x20000000", type=str)
        self.ram_size = self.settings.value(self.RAM_SIZE, 128, type=int)
        self.objcopy_use = bool(self.settings.value(self.USE_OBJCOPY, False, type=bool))
        self.objcopy_path = self.settings.value(self.OBJCOPY_PATH, "", type=str)
        self.addr_saving = bool(self.settings.value(self.SAVING_ADDRESS, False, type=bool))

    def save(self):        
        self.settings.setValue(self.FLASH_START, self.flash_start_addr)
        self.settings.setValue(self.FLASH_SIZE, self.flash_size)
        self.settings.setValue(self.RAM_START, self.ram_start_addr)
        self.settings.setValue(self.RAM_SIZE, self.ram_size)
        self.settings.setValue(self.USE_OBJCOPY, self.objcopy_use)
        self.settings.setValue(self.OBJCOPY_PATH, self.objcopy_path)
        self.settings.setValue(self.SAVING_ADDRESS, self.addr_saving)
        self.settings.sync()
        #
        self.load_settings()
        
    @property
    def flash_start(self) -> int:
        return int(self.flash_start_addr, 16)

    @property
    def flash_end(self) -> int:
        return self.flash_start + self.flash_size * 1024

    @property
    def ram_start(self) -> int:
        return int(self.ram_start_addr, 16)

    @property
    def ram_end(self) -> int:
        return self.ram_start + self.ram_size * 1024
        


        
        
            