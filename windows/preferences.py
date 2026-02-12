import shutil
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QObject, pyqtSignal
from ui.ui_preferences import Ui_Dialog
from settings.settings import AppSettings

class PreferencesDialog(QDialog, Ui_Dialog):
    # Signals
    settings_saved = pyqtSignal()

    def __init__(self, settings):
        super().__init__()
        self.setupUi(self)
        
        self.settings = settings
        
        # Buttons
        self.buttonSave.clicked.connect(self.on_save_settings_clicked)
        self.buttonSearch.clicked.connect(self.on_search_objcopy_clicked)
        self.checkObjcopy.stateChanged.connect(self.on_checkObjcopy_changed)
        
        # Data
        self.lineFlashStart.setText(self.settings.flash_start_addr)
        self.lineFlashSize.setText(str(self.settings.flash_size))
        self.lineRamStart.setText(self.settings.ram_start_addr)
        self.lineRamSize.setText(str(self.settings.ram_size))
        self.lineObjcopyPath.setText(self.settings.objcopy_path)
        self.checkObjcopy.setChecked(self.settings.objcopy_use)
        self.checkHints.setChecked(self.settings.addr_saving)
        
        # Sync state for checkbox
        self.on_checkObjcopy_changed(self.checkObjcopy.checkState())
        
    def on_save_settings_clicked(self):
        # Take settings from lineEdit'save
        self.settings.flash_start_addr = self.lineFlashStart.text()
        self.settings.flash_size = int(self.lineFlashSize.text())
        self.settings.ram_start_addr = self.lineRamStart.text()
        self.settings.ram_size = int(self.lineRamSize.text())
        self.settings.objcopy_path = self.lineObjcopyPath.text()
        self.settings.objcopy_use = self.checkObjcopy.isChecked()
        self.settings.addr_saving = self.checkHints.isChecked()
        # Saving
        self.settings.save()
        self.settings_saved.emit()
        
    def on_search_objcopy_clicked(self):
        path_to_objcopy = shutil.which("arm-none-eabi-objcopy")
        if path_to_objcopy:
            self.settings.objcopy_path = path_to_objcopy
            self.lineObjcopyPath.setText(self.settings.objcopy_path)
            
    def on_checkObjcopy_changed(self, state):
        is_enabled = state == 2
        self.lineObjcopyPath.setEnabled(is_enabled)
        self.buttonSearch.setEnabled(is_enabled)