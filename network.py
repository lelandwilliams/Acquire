import sys, queue, uuid
from PyQt5 import QtNetwork
from PyQt5.QtCore import QObject, pyqtSlot, QCoreApplication, QThread, QByteArray, QTimer

DEFAULTPORT = 65337

class NetworkBaseClass(QObject):
    def __init__(self, client_id = None, port = DEFAULTPORT, address = QtNetwork.QHostAddress.LocalHost):
        super().__init__()
        self.server = QtNetwork.QTcpServer()
        self.port = port
        self.address = address
        self.openAttach = False

        if client_id == None:
            self.client_id = str(uuid.uuid4())
        else:
            self.client_id = client_id

    def openServer(self):
        attempts = 0
        max_attempts = 10
        while attempts < max_attempts and (not self.server.isListening()):
            if not self.server.listen(QtNetwork.QHostAddress.LocalHost, self.port):
                port += 1
                attempts += 1

    def read(self):
        if self.server.hasPendingConnections():
            client = self.server.nextPendingConnection()
            client.waitForReadyRead()
            s = client.readLine().data().decode() 
            print(s)

class Host(NetworkBaseClass):
    def __init__(self, client_id = None, port = DEFAULTPORT, address = QtNetwork.QHostAddress.LocalHost):
        super.__init__(client_id, port, address)
        self.openServer()
