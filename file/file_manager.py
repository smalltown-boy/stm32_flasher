from PyQt6.QtCore import QObject, pyqtSignal, QFile, QIODevice
from PyQt6.QtWidgets import QFileDialog, QLineEdit
from ui.ui_main import Ui_MainWindow

class FileManager(QObject):
    
    def __init__(self, parent, path_edit: QLineEdit):
        super().__init__(parent)
        self.parent = parent
        self.path_edit = path_edit

    def open_file(self) -> bytes | None:
        firmware_path, _ = QFileDialog.getOpenFileName(self.parent, "Открыть BIN-файл", "", "BIN-файлы (*.bin)")
        
        if not firmware_path:
            return None
            
        firmware_file = QFile(firmware_path)
        
        if not firmware_file.open(QIODevice.OpenModeFlag.ReadOnly):
            return None
            
        data = firmware_file.readAll()
        firmware_file.close()

        self.path_edit.setText(firmware_path)

        return bytes(data)