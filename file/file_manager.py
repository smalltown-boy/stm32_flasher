from PyQt6.QtCore import QObject, pyqtSignal, QFile, QIODevice
from PyQt6.QtWidgets import QFileDialog, QLineEdit
from ui.ui_main import Ui_MainWindow

class FileManager(QObject):
    
    def __init__(self, parent, path_edit: QLineEdit):
        super().__init__(parent)
        self.parent = parent
        self.path_edit = path_edit

    def open_file(self):
        firmware_path, _ = QFileDialog.getOpenFileName(self.parent, "Open firmware file", "", "files (*.bin *.hex *.elf)") 

        if firmware_path:
            self.path_edit.setText(firmware_path)   
            
        return firmware_path