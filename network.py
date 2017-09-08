import sys, queue
from PyQt5 import QtNetwork
from PyQt5.QtCore import QObject, pyqtSlot, QCoreApplication, QThread, QByteArray, QTimer

class ConnectionInfo:
    def __init__(self):
        self.role = None
        self.acquire_id = None
        self.master = False

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

        self.message_num = 0
        self.clients = list()
        self.player_id = dict()
        self.message_q = queue.Queue()
        self.master = master

    @pyqtSlot()
    def newClientFound(self):
#       print("A client has connected")
        client = self.server.nextPendingConnection()
#       print(client.peerAddress())
        self.clients.append(client)

    @pyqtSlot()
    def onStarted(self):
        self.app.exec_()

    def broadcast(self, message):
        data = QByteArray()
        data.append(str(self.message_num))
        data.append(";")
        data.append(message)
#       for c in self.clients.values():
        for c in self.clients_raw:
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
        self.__acquireID = 0

    @pyqtSlot()
    def onStarted(self):
        self.app.exec_()

    @pyqtSlot()
    def receiveData(self):
        s = self.net.readLine().data().decode() 
        priority = s.split(';',1)[0]
        self.message_q.put(s)
    
    def set_id(self, acquire_id):
        if self.__acquireID == 0:
            self.__acquireID = acquire_id

    def authenticate(self, acquire_id = None):
        # Not currently used
        if acquire_id != None:
            self.set_id(acquire_id)
        message = "AUTH;" + self.acquire_id + ";"
        self.send_message(message)
    
    def send_message(self, message):
        data = QByteArray()
        data.append(message)
        self.net.write(message)

class AcquireLogger(AcquireClient):
    def __init__(self):
        super().__init__()
        self.f = open('acquire.log', 'w')
        self.timer = QTimer.timer
        self.timer.timeout.connect(self.read_queue)
        self.done = False
        self.timer.start(1000)

    @pyqtSlot()
    def read_queue(self):
        if self.done:
            self.f.close()
        else:
            while not self.message_q.empty():
                m = self.message_q.get()
                self.f.write(m)
                if m.split(';',2)[1] == "END":
                    self.done = True

if __name__ == "__main__":
    a = AcquireServer()
    b = AcquireClient(a.get_port())
