from PyQt6.QtWidgets import QDialog, QHeaderView, QMessageBox
from PyQt6.QtCore import QSettings
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import QObject, pyqtSignal
from pathlib import Path
from ui.ui_profile import Ui_Dialog


class ProfilesDialog(QDialog, Ui_Dialog):
    # Signals 
    reload_profile = pyqtSignal()

    PROFILE_NAME = "STM32 PROFILE/PROFILE NAME"
    FLASH_START = "STM32 MEMORY SETTINGS/START FLASH ADDR"
    FLASH_SIZE = "STM32 MEMORY SETTINGS/FLASH SIZE"
    RAM_START = "STM32 MEMORY SETTINGS/START RAM ADDR"
    RAM_SIZE = "STM32 MEMORY SETTINGS/RAM SIZE"

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.project_root = Path(__file__).parent.parent
        self.profiles_dir = self.project_root / "profiles"
        self.profiles_dir.mkdir(exist_ok=True)

        self.check_profiles()

        # Signals
        self.tableView.clicked.connect(self.on_row_clicked)
        self.buttonAddProfile.clicked.connect(self.on_add_profile_clicked)
        
    def clear_profile_fields(self):
        self.lineAddName.clear()
        self.lineAddFlashStart.clear()
        self.lineAddFlashSize.clear()
        self.lineAddRamStart.clear()
        self.lineAddRamSize.clear()

    def on_add_profile_clicked(self):

        profile_name = self.lineAddName.text().strip()
        flash_start_addr = self.lineAddFlashStart.text().strip()
        flash_size = self.lineAddFlashSize.text().strip()
        ram_start_addr = self.lineAddRamStart.text().strip()
        ram_size = self.lineAddRamSize.text().strip()

        if not all([profile_name, flash_start_addr, flash_size, ram_start_addr, ram_size]):
            QMessageBox.warning(self, "Warning", "Set all fields!")
            return

        try:
            int(flash_size)
            int(ram_size)
        except ValueError:
            QMessageBox.warning(self, "Warning", "Flash and RAM size must be integers!")
            return

        file_path = self.profiles_dir / f"{profile_name}.ini"

        settings = QSettings(str(file_path), QSettings.Format.IniFormat)

        settings.setValue(self.PROFILE_NAME, profile_name)
        settings.setValue(self.FLASH_START, flash_start_addr)
        settings.setValue(self.FLASH_SIZE, flash_size)
        settings.setValue(self.RAM_START, ram_start_addr)
        settings.setValue(self.RAM_SIZE, ram_size)

        settings.sync()

        self.lineAddName.clear()
        self.lineAddFlashStart.clear()
        self.lineAddFlashSize.clear()
        self.lineAddRamStart.clear()
        self.lineAddRamSize.clear()

        self.check_profiles()

    def check_profiles(self):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Profiles"])

        if self.profiles_dir.exists():

            ini_files = sorted(self.profiles_dir.glob("*.ini"))

            for ini_file in ini_files:
                item = QStandardItem(ini_file.name)
                model.appendRow(item)

        model.appendRow(QStandardItem(""))

        self.tableView.setModel(model)
        self.tableView.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

    def on_row_clicked(self, index):
        item = self.tableView.model().itemFromIndex(index)

        if not item:
            return
            
        file_name = item.text()

        if file_name == "":
            # Если файл пуст
            self.buttonAddProfile.setEnabled(True)
            self.buttonDeleteProfile.setEnabled(False)

            self.lineAddName.setEnabled(True)
            self.lineAddFlashStart.setEnabled(True)
            self.lineAddFlashSize.setEnabled(True)
            self.lineAddRamStart.setEnabled(True)
            self.lineAddRamSize.setEnabled(True)
            
            self.clear_profile_fields()
            return
        else:
            # А если нет
            self.buttonAddProfile.setEnabled(False)
            self.buttonDeleteProfile.setEnabled(True)

            self.lineAddName.setEnabled(False)
            self.lineAddFlashStart.setEnabled(False)
            self.lineAddFlashSize.setEnabled(False)
            self.lineAddRamStart.setEnabled(False)
            self.lineAddRamSize.setEnabled(False)
            
            file_path = self.profiles_dir / file_name
            
            if not file_path.exists():
                QMessageBox.warning(self, "Error", "Profile file not found!")
                return
                
            settings = QSettings(str(file_path), QSettings.Format.IniFormat)

            profile_name = settings.value(self.PROFILE_NAME, "")
            flash_start = settings.value(self.FLASH_START, "")
            flash_size = settings.value(self.FLASH_SIZE, "")
            ram_start = settings.value(self.RAM_START, "")
            ram_size = settings.value(self.RAM_SIZE, "")

            # Заполняем поля
            self.lineAddName.setText(str(profile_name))
            self.lineAddFlashStart.setText(str(flash_start))
            self.lineAddFlashSize.setText(str(flash_size))
            self.lineAddRamStart.setText(str(ram_start))
            self.lineAddRamSize.setText(str(ram_size))
            
            self.reload_profile.emit()
            
    def on_delete_clicked(self):
        pass
