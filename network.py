import sys, queue, uuid
from PyQt5 import QtNetwork
from PyQt5.QtCore import QObject, pyqtSlot, QCoreApplication, QThread, QByteArray, QTimer

DEFAULTPORT = 65337

class ClientConnection(QObject):
    """ Used by AcquireServer to interact with clients """
    def __init__(self, client, message_q):
        super().__init__()
        self.client = client
        self.client_id = str(uuid.uuid4())
        self.client.setTextModeEnabled(True)
        self.name = None
        self.message_q = message_q
        client.readyRead.connect(self.receiveData)

    @pyqtSlot()
    def receiveData(self):
        print("Server: A message has been recieved from client 0")
        m = self.client.readLine().data().decode() 
        self.message_q.put(m)

    def write(self, m):
        self.client.write(m)

class ClientServerBaseClass(QObject):
    def __init__(self, port = 65337):
        super().__init__()
        self.port = port
        self.incoming_message_q = queue.Queue()
        self.outgoing_message_q = queue.Queue()
        self.read_incoming_next = True
        self.gameDone = False
        self.name = ""
        self.read_incoming_next  = True

    @pyqtSlot()
    def main(self):
        self.read_incoming_next = not self.read_incoming_next

        if self.gameDone:
            QCoreApplication.quit()
        elif self.read_incoming_next and \
                not self.incoming_message_q.empty():
            self.parse_message(self.incoming_message_q.get())
            self.incoming_message_q.task_done()
        elif not self.read_incoming_next and \
                not self.outgoing_message_q.empty():
            self.send_message(self.outgoing_message_q.get())
            self.outgoing_message_q.task_done()
            QTimer.singleShot(250, self.main)
        else:
            QTimer.singleShot(250, self.main)

class AcquireServer(ClientServerBaseClass):
    def __init__(self, port = DEFAULTPORT):
        super().__init__(port)
        self.mainStarted = False
        self.clients = list()
        self.master_id = None
        self.server = QtNetwork.QTcpServer()
        self.message_num = 1
        if not self.server.listen(QtNetwork.QHostAddress.LocalHost, self.port):
            sys.exit("Server: Error! Could not open server")
        else:
            print("Server: server listening to port " + str(self.port))
        self.server.newConnection.connect(self.newClientConnected)

    def broadcast(self, message):
        for c in self.clients:
            self.send_message(message, client)

    @pyqtSlot()
    def newClientConnected(self):
        print("Server: A client has connected")
        client = self.server.nextPendingConnection()
        self.clients.append(ClientConnection(client, self.outgoing_message_q))
        if self.master_id == None:
            self.master_id = clients[0].client_id
        if not self.mainStarted:
            self.mainStarted = True
            QTimer.singleShot(500, self.main)
        
    def send_message(self, message, client):
        data = QByteArray()
        data = data.append(str(self.message_num))
        data = data.append(";")
        data = data.append(message)
        client.write(data)
        self.message_num += 1

class AcquireClient(ClientServerBaseClass):
    def __init__(self, port = DEFAULTPORT):
        super().__init__(port)
        self.mainStarted = False
        self.name = "Client"
        self.client_id = str(uuid.uuid4())
        self.incoming_message_q = queue.PriorityQueue()
        self.net = QtNetwork.QTcpSocket()
        self.net.connectToHost(QtNetwork.QHostAddress.LocalHost, self.port)
        if self.net.waitForConnected(5000):
            print(self.name + ": connected")
            self.net.setTextModeEnabled(True)
            QTimer.singleShot(500, self.main)
            self.net.readyRead.connect(self.receiveData)
            if not self.mainStarted:
                self.mainStarted = True
                QTimer.singleShot(500, self.main)
        else:
            print(self.name + ": connection Failed")
            QCoreApplication.quit()

    @pyqtSlot()
    def receiveData(self):
        s = self.net.readLine().data().decode() 
        priority = s.split(';',1)[0]
        self.incoming_message_q.put([priority, s])
        print(self.name + ": message recieved")
 
    def send_message(self, message):
        data = QByteArray()
        data.append(message)
        if self.net.write(data) == -1:
            print("Error sending message")
        else:
            print("client: message sent")

class AcquireSimpleLogger(AcquireClient):
    def __init__(self, port = DEFAULTPORT):
        super().__init__(port)
        self.name = "Logger"

    def parse_message(self, m):
        print(self.name + ": " + m[1])
        QTimer.singleShot(250, self.main)

