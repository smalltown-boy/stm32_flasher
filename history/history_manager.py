import json
import os
from PyQt6.QtCore import QObject, QStringListModel, Qt
from PyQt6.QtWidgets import QCompleter, QLineEdit

class HistoryManager(QObject):
    def __init__(self, parent=None, filename='network_history.json', max_items=5):
        super().__init__(parent)
        self.filename = filename
        self.max_items = max_items
        self.history = []
        
        self.load_history()
        
    def load_history(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as data_file:
                    self.history = json.load(data_file)
            except (json.JSONDecodeError, IOError):
                self.history = []
                
    def save_history(self):
        try:
            if os.path.exists(self.filename):
                json.dump(self.history, data_file, ensure_ascii=False, indent=2)
        except IOError:
            pass
            
    def add_address(self, address: str):
        address = address.strip()
        if not address:
            return

        if address in self.history:
            self.history.remove(address)

        self.history.insert(0, address)
        self.history = self.history[:self.max_items]
        self.save_history()
        
    def attach_to_lineedit(self, line_edit: QLineEdit):
        self.model = QStringListModel(self.history, self)

        self.completer = QCompleter(self.model, self)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)

        line_edit.setCompleter(self.completer)

    def refresh_completer(self):
        if hasattr(self, "model"):
            self.model.setStringList(self.history)
        
    def get_history(self):
        return self.history
            