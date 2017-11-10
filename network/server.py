import sys, queue, uuid
from PyQt5 import QtNetwork, QtWebSockets
from PyQt5.QtCore import QObject, QDataStream, pyqtSlot, QCoreApplication, QTimer, QMutex

DEFAULTPORT = 64337

class AcquireWebSocketServer(QObject):
    def __init__(self, 
            my_id = None, 
            port = DEFAULTPORT, 
            address = QtNetwork.QHostAddress.LocalHost):
        super().__init__()
        self.server = QtWebSockets.QWebSocketServer('',QtWebSockets.QWebSocketServer.NonSecureMode)
        self.port = port
        self.address = address
        self.concierge = None
        self.clients = dict()
        self.clients_mutex = QMutex()
        self.GM = None
        self.gameInProgress = False
        self.numPlayersNeeded = 3

        attempts = 0
        max_attempts = 10
        while attempts < max_attempts and not self.server.isListening():
            if not self.server.listen(self.address, self.port):
                raise('failed to open server')
            else:
                print(' now listening')
                self.server.newConnection.connect(self.newClient)
                QTimer.singleShot(20000, QCoreApplication.quit)
#        print(self.server.isListening())

    def newClient(self):
        print('server recieved a connection')
        client = self.server.nextPendingConnection()
        self.clients_mutex.lock()
        self.clients[client] = 'Undefined'
        self.clients_mutex.unlock()
        client.textMessageReceived.connect(self.processTextMessage)
        client.disconnected.connect(self.socketDisconnected)

    def processTextMessage(self,message):
        print("server recieved message: {}".format(message))
        sender= self.sender()
#       self.clients_mutex.lock()
        if len(message.split(';') != 3):
                return
        m_type,m_subtype,m_val = message.split(';')

        if m_type == 'GENERAL':
            for client in [c for c in self.clients if c!= sender]:
                client.sendTextMessage(message)
        elif m_type == 'REGISTER' and m_subtype == 'GM' and self.GM is None:
            self.GM = sender
            self.clients[sender] = 'GM'
        elif m_type == 'REGISTER' and m_subtype == 'PLAYER' and not self.gameInProgress:
            self.clients[sender] = m_val
            print( "player {} registered".format(m_val))
            self.numPlayersNeeded -= 1
            if self.numPlayersNeeded == 0:
                # start the game
                if self.GM is None:
                    self.startGM()

        elif m_type == 'REGISTER' and m_subtype == 'Logger' and self.clients[sender] == 'Undefined':
            self.clients[sender] = 'Logger'

#       self.clients_mutex.unlock()
#       QTimer.singleShot(1000, self.sendMessage)

    def sendMessage(self):
        self.client.sendTextMessage("wazzup")

    def socketDisconnected(self):
        print('server lost connection to client')
        sender= self.sender()
        sender.deleteLater()
#        QCoreApplication.quit()

if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    a = AcquireWebSocketServer()
    app.exec_()
