import sys, queue, uuid
from PyQt5 import QtNetwork
from PyQt5.QtCore import QObject, pyqtSlot, QCoreApplication, QThread, QByteArray, QTimer

DEFAULTPORT = 65337

class ClientConnection(QObject):
    """ An Instance of this class is created by AcquireServer 
    for each client upon connection"""
    def __init__(self, client, message_q):
        super().__init__()
        self.client = client
        self.client_id = str(uuid.uuid4())
        self.client.setTextModeEnabled(False)
        self.name = None
        self.message_q = message_q
        self.outgoing_message_q = queue.Queue()
        client.readyRead.connect(self.receiveData)
        QTimer.singleShot(750, self.main)

    @pyqtSlot()
    def receiveData(self):
        m = self.client.readLine().data().decode() 
        self.message_q.put(m)
#        QTimer.singleShot(250, self.main)

    @pyqtSlot()
    def main(self):
        if not self.outgoing_message_q.empty():
            message = self.outgoing_message_q.get()
#           self.outgoing_message_q.task_done()
            if self.client.write(message) == -1:
                sys.exit("error writing to client " + self.name)
        QTimer.singleShot(750, self.main)

    def write(self, m):
#       print("ClientConnection.write() recieved message: " + str(m))
#        self.client.write(m)
        self.outgoing_message_q.put(m)
        return 0

class ClientServerBaseClass(QObject):
    def __init__(self, port = 65337):
        super().__init__()
        self.port = port
        self.incoming_message_q = queue.Queue()
        self.outgoing_message_q = queue.Queue()
        self.gameDone = False

    @pyqtSlot()
    def main(self):
        if not self.outgoing_message_q.empty():
            self.send_message(self.outgoing_message_q.get())
#           self.outgoing_message_q.task_done()
        elif not self.incoming_message_q.empty():
            message = self.incoming_message_q.get()
#           self.incoming_message_q.task_done()
            self.parse_message(message)

        QTimer.singleShot(399, self.main)

    @pyqtSlot()
    def oldmain(self):
        self.read_incoming_next = (not self.read_incoming_next)
        print(self.name + ": in main():")

        if self.gameDone:
            QCoreApplication.quit()
        elif self.read_incoming_next and \
                not self.incoming_message_q.empty():
            self.parse_message(self.incoming_message_q.get())
            self.incoming_message_q.task_done()
        elif (not self.read_incoming_next) and \
                not self.outgoing_message_q.empty():
            self.send_message(self.outgoing_message_q.get())
            self.outgoing_message_q.task_done()

        QTimer.singleShot(450, self.main)

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
#       else:
#           print("Server: server listening to port " + str(self.port))
        self.server.newConnection.connect(self.newClientConnected)

    def broadcast(self, message):
        # deprecated. should be removed
        for c in self.clients:
            self.send_message(message, client)

    @pyqtSlot()
    def newClientConnected(self):
        client = self.server.nextPendingConnection()
        self.clients.append(ClientConnection(client, self.incoming_message_q))
        data = QByteArray()
        data.append("-1;UUID;" + self.clients[-1].client_id)
        client.write(data)
        if self.master_id == None:
            self.master_id = self.clients[0].client_id
        if not self.mainStarted:
            self.mainStarted = True
            QTimer.singleShot(500, self.main)
        
    def send_message(self, message):
#       self.outgoing_message_q.task_done()
#       print("Server.send_message() received: " + message)
        data = QByteArray()
        data = data.append(str(self.message_num))
        data = data.append(";")
        data = data.append(message)
#       data = data.append('\n')
        self.message_num += 1
        for client in self.clients:
            client.write(data)

    def send_private_message(self, message, player):
        data = QByteArray()
        data = data.append(str(-1))
        data = data.append(";")
        data = data.append(message)
        for client in self.clients:
            if client.name == player:
                client.write(data)

class AcquireClient(ClientServerBaseClass):
    def __init__(self, port = DEFAULTPORT):
        super().__init__(port)
        self.mainStarted = False
        self.client_id = str(uuid.uuid4())
        self.incoming_message_q = queue.PriorityQueue()
        self.net = QtNetwork.QTcpSocket()
        self.attempts = 0
        QTimer.singleShot(500, self.attachToServer)

    @pyqtSlot()
    def attachToServer(self):
#       print(self.name + ": Connection Attempt " + str(self.attempts))
        self.net.connectToHost(QtNetwork.QHostAddress.LocalHost, self.port)
        if self.net.waitForConnected(5000):
            self.net.setTextModeEnabled(False)
#           print(self.name + ": connected")
            QTimer.singleShot(500, self.main)
            self.net.readyRead.connect(self.receiveData)
            if not self.mainStarted:
                self.mainStarted = True
                QTimer.singleShot(500, self.main)
            connected = True
        else:
            self.attempts += 1
            if self.attempts < 5:
                QTimer.singleShot(500, self.attachToServer)
            else:
                print(self.name + ": Too many attempts. Exiting")
                QCoreApplication.quit()
                
    def parse_message(self, m):
 #      print(self.name + ".parse_message() received: " + str(m))
        priority, command, parameter = m[1].split(';')
 #      print(self.name + " priorty: " + priority)
 #      print(self.name + " command: " + command)
 #      print(self.name + " parameter: " + parameter)
        if command == 'REGISTER':
            self.process_register(parameter)
        elif command == 'DISCONNECT':
            self.process_disconnect(parameter)
        elif command == 'PLACESTARTER':
            self.process_placestarter(parameter)
        elif command == 'PLACETILE':
            self.process_placetile(parameter)
        elif command == 'REQUEST':
            self.process_requesT(parameter)
        elif command == 'ERROR':
            self.process_error(parameter)
        elif command == 'INFO':
            self.process_info(parameter)
        elif command == 'PRIVATE':
            self.process_private(parameter)
        elif command == 'UUID':
            self.process_uuid(parameter)
#       self.outgoing_message_q.task_done()
#        QTimer.singleShot(250, self.main)

    def process_register(self, player, parameter):
        pass
    
    def process_disconnect(self, player, parameter):
        QCoreApplication.quit()

    def process_placestarter(self, player, parameter):
        pass

    def process_placetile(self, player, parameter):
        pass

    def process_request(self, player, parameter):
        pass

    def process_error(self, player, parameter):
        pass

    def process_info(self, player, parameter):
        pass

    def process_private(self, player, parameter):
        pass

    def process_uuid(self, parameter):
        pass

    @pyqtSlot()
    def receiveData(self):
        s = self.net.readLine().data().decode() 
        priority = s.split(';',1)[0]
        self.incoming_message_q.put([priority, s])
#       print(self.name + ": message recieved")
 
    def send_message(self, message):
        data = QByteArray()
        data.append(self.client_id)
        data.append(';')
        data.append(message)
        if self.net.write(data) == -1:
#           self.outgoing_message_q.task_done()
            sys.exit(self.name + ": Error sending message")
#       else:
#           print("client: message sent")

class AcquireSimpleLogger(AcquireClient):
    def __init__(self, port = DEFAULTPORT):
        self.name = "Logger"
        super().__init__(port)

    def parse_message(self, m):
        print(self.name + ": " + m[1])
        priority, command, parameter = m[1].split(';')
        if command == 'DISCONNECT':
            QCoreApplication.quit()
#       self.outgoing_message_q.task_done()
#       QTimer.singleShot(250, self.main)

