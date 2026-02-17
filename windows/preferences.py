import shutil
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QObject, pyqtSignal
from ui.ui_preferences import Ui_Dialog
from settings.settings import AppSettings
from windows.profile import ProfilesDialog
from PyQt6.QtCore import QSettings, QObject

class PreferencesDialog(QDialog, Ui_Dialog):
    # Signals
    settings_saved = pyqtSignal()

    def __init__(self, settings):
        super().__init__()
        self.setupUi(self)
        
        self.settings = settings
        self.manage_dialog = ProfilesDialog()
        
        # Buttons
        self.buttonSave.clicked.connect(self.on_save_settings_clicked)
        self.buttonSearch.clicked.connect(self.on_search_objcopy_clicked)
        self.buttonManage.clicked.connect(self.on_manage_clicked)
        self.checkObjcopy.stateChanged.connect(self.on_checkObjcopy_changed)
        
        # Data
        self.lineFlashStart.setText(self.settings.flash_start_addr)
        self.lineFlashSize.setText(str(self.settings.flash_size))
        self.lineRamStart.setText(self.settings.ram_start_addr)
        self.lineRamSize.setText(str(self.settings.ram_size))
        self.lineObjcopyPath.setText(self.settings.objcopy_path)
        self.checkObjcopy.setChecked(self.settings.objcopy_use)
        self.checkHints.setChecked(self.settings.addr_saving)
        
        # Do lineEdit's not editable
        self.lineFlashStart.setEnabled(False)
        self.lineFlashSize.setEnabled(False)
        self.lineRamStart.setEnabled(False)
        self.lineRamSize.setEnabled(False)
        
        # Signals
        self.manage_dialog.reload_profile.connect(self.load_profiles)
        
        # Sync state for checkbox
        self.on_checkObjcopy_changed(self.checkObjcopy.checkState())
        
        self.comboBox.currentTextChanged.connect(self.on_profile_selected)
        self.load_profiles()
        
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
        
    def on_manage_clicked(self):
        self.manage_dialog.exec()
        
    def load_profiles(self):
        self.comboBox.clear()
        profiles_dir = self.manage_dialog.profiles_dir
        ini_files = sorted(profiles_dir.glob("*.ini"))
        
        for ini_file in ini_files:
            profile_name = ini_file.stem
            self.comboBox.addItem(profile_name)
        
        '''        
        if self.settings.active_profile:
            index = self.comboBox.findText(self.settings.active_profile)
            if index >= 0:
                self.comboBox.setCurrentIndex(index)
        '''
                
    def on_profile_selected(self, profile_name):
        if not profile_name:
            return
        
        file_path = self.manage_dialog.profiles_dir / f"{profile_name}.ini"

        if not file_path.exists():
            return

        settings = QSettings(str(file_path), QSettings.Format.IniFormat)

        flash_start = settings.value(self.manage_dialog.FLASH_START, "")
        flash_size = settings.value(self.manage_dialog.FLASH_SIZE, "")
        ram_start = settings.value(self.manage_dialog.RAM_START, "")
        ram_size = settings.value(self.manage_dialog.RAM_SIZE, "")

        # Отображаем (read-only)
        self.lineFlashStart.setText(str(flash_start))
        self.lineFlashSize.setText(str(flash_size))
        self.lineRamStart.setText(str(ram_start))
        self.lineRamSize.setText(str(ram_size))
