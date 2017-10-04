import sys, queue, uuid
from PyQt5 import QtNetwork
from PyQt5.QtCore import QObject, pyqtSlot, QCoreApplication, QThread, QByteArray, QTimer, QDataStream

DEFAULTPORT = 65337

class NetworkBaseClass(QObject):
    def __init__(self, 
            client_id = None, 
            port = DEFAULTPORT, 
            address = QtNetwork.QHostAddress.LocalHost):
        super().__init__()
        self.server = QtNetwork.QTcpServer()
        self.port = port
        self.address = address
        self.openAttach = False
        self.lastMessageSent = ""
        self.lastMessageReceived = "Whoa"

        if client_id == None:
            self.client_id = str(uuid.uuid4())
        else:
            self.client_id = client_id

    @pyqtSlot()
    def mainLoop(self):
        if self.server.isListening():
            QTimer.singleShot(750, self.read())

    def openServer(self):
        attempts = 0
        max_attempts = 10
        while attempts < max_attempts and (not self.server.isListening()):
            if not self.server.listen(QtNetwork.QHostAddress.LocalHost, self.port):
                self.port += 1
                attempts += 1
        self.server.setMaxPendingConnections(1)
        self.server.newConnection.connect(self.read)

    @pyqtSlot()
    def read(self):
        print("In read()")
#       client = None
#       while client == None:
#           if self.server.hasPendingConnections():
        self.client = self.server.nextPendingConnection()
        self.client.setTextModeEnabled(True)
        self.client.readyRead.connect(self.readMessage)

    @pyqtSlot()
    def readMessage(self):
        print("In readMessage()")
        s = self.client.readLine().data().decode() 
#       s = str(client.readLine().toStr())
#       s = client.read(256)
#           istream = QDataStream(client)
#           istream >> s
        self.lastMessageReceived = s
        print(s)
        self.client.close()
    
    @pyqtSlot()
    def write(self, address, port, message):
        socket = QtNetwork.QTcpSocket()
        success = -1
        socket.connectToHost(address, port)
        socket.setTextModeEnabled(True)
        if socket.waitForConnected(5000) != -1:
            data = QByteArray()
            data.append("Scooby Do")
            success = socket.write(data)
            socket.close()
        return success


class Host(NetworkBaseClass):
    def __init__(self, 
            client_id = None, 
            port = DEFAULTPORT, 
            address = QtNetwork.QHostAddress.LocalHost):

        super.__init__(client_id, port, address)
        self.clients = []
        self.openServer()
