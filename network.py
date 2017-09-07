import sys, queue
from PyQt5 import QtNetwork
from PyQt5.QtCore import QObject, pyqtSlot, QCoreApplication, QThread, QByteArray

class AcquireServer(QObject):
    def __init__(self, master = None, port = 0):
        super().__init__()
        self.app = QCoreApplication(sys.argv)
        self.thread = QThread()
        self.thread.started.connect(self.onStarted)
        if port == 0 :
            self.PORT = 65337
        else:
            self.PORT = port
        
        self.server = QtNetwork.QTcpServer()
        if not self.server.listen(QtNetwork.QHostAddress.LocalHost, self.PORT):
            sys.exit("Error! Could not open server")
        self.server.newConnection.connect(self.newClientFound)

        self.clients_raw = list()
        self.message_num = 0
        self.clients = dict()
        self.player_id = dict()
        self.message_q = queue.Queue()
        self.master = master

    @pyqtSlot()
    def newClientFound(self):
        print("A client has connected")
        client = self.server.nextPendingConnection()
        print(client.peerAddress())
        self.clients_raw.append(client)

    @pyqtSlot()
    def onStarted(self):
        self.app.exec_()

    def broadcast(self, message):
        data = QByteArray()
        data.append(str(self.message_num))
        data.append(";")
        data.append(message)
        for c in self.clients.values():
            c.write(data)
        self.message_num += 1

    def get_port(self):
        return self.server.serverPort()

    @pyqtSlot()
    def receiveData(self):
        s = self.net.readLine().data().decode() 
        self.message_q.put(s)

    def __del__(self):
        self.server.close()

class AcquireClient(QObject):
    def __init__(self, port=65337):
        super().__init__()
        self.app = QCoreApplication(sys.argv)
        self.thread = QThread()
        self.thread.started.connect(self.onStarted)
        
        self.net = QtNetwork.QTcpSocket()
        self.net.connectToHost(QtNetwork.QHostAddress.LocalHost, port)
        self.net.readyRead.connect(self.receiveData)

        self.message_q = queue.PriorityQueue()

    @pyqtSlot()
    def onStarted(self):
        self.app.exec_()

    @pyqtSlot()
    def receiveData(self):
        s = self.net.readLine().data().decode() 
        priority = s.split(';',1)[0]
        self.message_q.put(s)

if __name__ == "__main__":
    a = AcquireServer()
    b = AcquireClient(a.get_port())
