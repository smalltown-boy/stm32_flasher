from PyQt6.QtCore import QObject, pyqtSignal


class DataParser(QObject):
    log = pyqtSignal(str)
    response = pyqtSignal(int)

    def pars_data(self, data: bytes):
        if not data or len(data) != 1:
            self.log.emit("Invalid response")
            return

        code = data[0]
        self.response.emit(code)

    
            
        
    
        
        
        
        
        
        
         
            
