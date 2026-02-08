from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from PyQt6.QtNetwork import QUdpSocket, QHostAddress, QAbstractSocket


class UdpClient(QObject):
    log = pyqtSignal(str)
    dataReceived = pyqtSignal(bytes)
    error = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.socket = QUdpSocket(self)
        self.socket.readyRead.connect(self._on_ready_read)

        self.timeout_timer = QTimer(self)
        self.timeout_timer.setSingleShot(True)
        self.timeout_timer.timeout.connect(self._on_timeout)

        self.remote_ip = None
        self.remote_port = None

    def open(self, ip: str, port: int) -> bool:
        host = QHostAddress()
        if not host.setAddress(ip):
            self.log.emit(f"Invalid IP: {ip}")
            return False

        if not (1 <= port <= 65535):
            self.log.emit("Invalid port")
            return False

        if self.socket.state() == QAbstractSocket.SocketState.BoundState:
            self.socket.close()

        if not self.socket.bind(QHostAddress.SpecialAddress.AnyIPv4, 0):
            self.log.emit("Failed to bind UDP socket")
            return False

        self.remote_ip = host
        self.remote_port = port

        self.log.emit("UDP socket opened")
        return True

    def send(self, data: bytes, timeout_ms=35000):
        if self.socket.state() != QAbstractSocket.SocketState.BoundState:
            self.error.emit("Socket not opened")
            return

        self.socket.writeDatagram(data, self.remote_ip, self.remote_port)
        self.timeout_timer.start(timeout_ms)

    def _on_ready_read(self):
        self.timeout_timer.stop()

        while self.socket.hasPendingDatagrams():
            datagram = self.socket.receiveDatagram()
            self.dataReceived.emit(bytes(datagram.data()))

    def _on_timeout(self):
        self.error.emit("UDP timeout")
