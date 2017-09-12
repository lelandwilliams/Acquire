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
        self.message_num = 0
        self.clients = list()
        self.player_id = dict()
        self.message_q = queue.Queue()
        self.master = master

        super().__init__()

#        self.app = QCoreApplication(sys.argv)
        if port == 0 :
            self.PORT = 65337
        else:
            self.PORT = port
        self.server = QtNetwork.QTcpServer()
        #self.thread = QThread()
        #self.thread.started.connect(self.onStarted)
        self.onStarted()
        
    @pyqtSlot()
    def newClientFound(self):
        print("Server: A client has connected")
        client = self.server.nextPendingConnection()
        client.setTextModeEnabled(True)
#       print(client.peerAddress())
        if len(self.clients) == 0:
            client.readyRead.connect(self.receiveData0)
        elif len(self.clients) == 1:
            client.readyRead.connect(self.receiveData1)
        elif len(self.clients) == 2:
            client.readyRead.connect(self.receiveData2)
        elif len(self.clients) == 3:
            client.readyRead.connect(self.receiveData3)
        elif len(self.clients) == 4:
            client.readyRead.connect(self.receiveData4)
        elif len(self.clients) == 5:
            client.readyRead.connect(self.receiveData5)
        elif len(self.clients) == 6:
            client.readyRead.connect(self.receiveData6)

        self.clients.append(client)
        QTimer.singleShot(500, self.main)

    @pyqtSlot()
    def onStarted(self):
        if not self.server.listen(QtNetwork.QHostAddress.LocalHost, self.PORT):
            sys.exit("Server: Error! Could not open server")
        else:
            print("Server: server listening to port " + str(self.PORT))
        self.server.newConnection.connect(self.newClientFound)
        QTimer.singleShot(500, self.main)

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
    def disconnected(self):
        print("Server: disconnected")

    @pyqtSlot()
    def receiveData0(self):
        print("Server: A message has been recieved from client0")
        s = self.clients[0].readLine().data().decode() 
        self.message_q.put(s)

    @pyqtSlot()
    def receiveData1(self):
        print("Server: A message has been recieved")
        s = self.clients[1].readLine().data().decode() 
        self.message_q.put(s)

    @pyqtSlot()
    def receiveData2(self):
        print("Server: A message has been recieved")
        s = self.clients[2].readLine().data().decode() 
        self.message_q.put(s)

    @pyqtSlot()
    def receiveData3(self):
        print("Server: A message has been recieved")
        s = self.clients[3].readLine().data().decode() 
        self.message_q.put(s)

    @pyqtSlot()
    def receiveData4(self):
        print("Server: A message has been recieved")
        s = self.clients[4].readLine().data().decode() 
        self.message_q.put(s)

    @pyqtSlot()
    def receiveData5(self):
        print("Server: A message has been recieved")
        s = self.clients[5].readLine().data().decode() 
        self.message_q.put(s)

    @pyqtSlot()
    def receiveData6(self):
        print("Server: A message has been recieved")
        s = self.clients[6].readLine().data().decode() 
        self.message_q.put(s)

    def __del__(self):
        self.server.close()

class AcquireClient(QObject):
    def __init__(self, port=65337):
        self.__acquireID = 0
        self.done = False
        self.message_q = queue.PriorityQueue()

        super().__init__()
#        self.app = QCoreApplication(sys.argv)
        if port == 0 or port == 65337:
            self.PORT = 65337
        else:
            self.PORT = port
        self.net = QtNetwork.QTcpSocket()
#        self.thread = QThread()
#        self.thread.started.connect(self.onStarted)
#       self.onStarted()
        QTimer.singleShot(500, self.startNet)

    @pyqtSlot()
    def startNet(self):
        self.net.connected.connect(self.onConnect)
        self.net.connectToHost(QtNetwork.QHostAddress.LocalHost, self.PORT)
        if self.net.waitForConnected(5000):
            print("Client: connected")
        else:
            print("Client: connection Failed")
            QCoreApplication.quit()
        self.net.setTextModeEnabled(True)



    @pyqtSlot()
    def onStarted(self):
        self.net.connectToHost(QtNetwork.QHostAddress.LocalHost, self.PORT)
        self.net.connected.connect(self.onConnect)
#       self.app.exec_()

    @pyqtSlot()
    def onConnect(self):
        self.net.setTextModeEnabled(True)
        self.net.readyRead.connect(self.receiveData)
        QTimer.singleShot(500, self.main)
        self.send_message("Howdy")

    @pyqtSlot()
    def main(self):
        if self.done:
            self.app.quit()
        else:
            while not self.message_q.empty():
                m = self.message_q.get()
                self.parse_message(m)
                m_type = m.split(';',2)[1] 
                if  m_type == "INFO":
                    self.report_info(m)
                elif m_type == "DISCONNECT":
                    self.report_disconnect(m)
                elif m_type == "":
                    pass
                elif m_type == "":
                    pass
                elif m_type == "":
                    pass
                elif m_type == "":
                    pass
            QTimer.singleShot(500, self.main)

    @pyqtSlot()
    def receiveData(self):
        s = self.net.readLine().data().decode() 
        priority = s.split(';',1)[0]
        self.message_q.put(s)
        print("message recieved")
    
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
        if self.net.write(data) == -1:
            print("Error sending message")
        else:
            print("client: message sent")

class AcquireLogger(AcquireClient):
    def __init__(self, port=0):
        super().__init__(port)
        self.f = open('acquire.log', 'w')
        self.app.aboutToQuit.connect(self.cleanup)
        self.report_info = self.parse_message

    def parse_message(self, message):
        self.f.write(message)

    def report_disconnect(self,message):
         self.parse_message(message)

    @pyqtSlot()
    def cleanup(self):
        self.f.close()

if __name__ == "__main__":
#   a = AcquireServer()
    b = AcquireClient()
