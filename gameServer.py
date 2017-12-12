import sys, queue, uuid, argparse
from PyQt5 import QtNetwork, QtWebSockets
from PyQt5.QtCore import QObject, QDataStream, pyqtSlot, QCoreApplication, QTimer, QUrl

DEFAULTPORT = 64337

class GameServer(QObject):
    def __init__(self, 
            my_id = None, 
            port = DEFAULTPORT, 
            address = QtNetwork.QHostAddress.LocalHost,
            conciergePort = None,
            numPlayers = 4):
        super().__init__()
        self.server = QtWebSockets.QWebSocketServer('',QtWebSockets.QWebSocketServer.NonSecureMode)
        self.port = port
        self.address = address
        self.clients = dict() # client_obj -> name
        self.GM = None
        self.gameInProgress = False
        self.numPlayersNeeded = numPlayers
        self.players = dict() # This is a dict name -> client_obj

        attempts = 0
        max_attempts = 10
        while attempts < max_attempts and not self.server.isListening():
            self.port += 1
            if not self.server.listen(self.address, self.port):
                attempts +=1
            else:
#               print('Game Server now listening')
                self.server.newConnection.connect(self.newClient)
                self.c_socket = QtWebSockets.QWebSocket()
                self.url = QUrl()
                self.url.setScheme("ws")
                self.url.setHost('localhost')
                self.url.setPort(port)
                self.c_socket.connected.connect(self.onConnected)
                self.c_socket.open(self.url)

    def onConnected(self):
#       print('Game Server connected to concierge')
        self.c_socket.textMessageReceived.connect(self.processConciergeMessage)
        self.c_socket.disconnected.connect(self.conciergeDisconnected)
        self.c_socket.sendTextMessage("READY;{}".format(self.port))

    def conciergeDisconnected(self):
        QCoreApplication.quit()
        sys.exit()

    def newClient(self):
#       print('Game server recieved a connection')
        self.consecutive_timeouts = 0
        client = self.server.nextPendingConnection()
        self.clients[client] = 'Undefined'
        client.textMessageReceived.connect(self.processTextMessage)
        client.disconnected.connect(self.socketDisconnected)

    def processConciergeMessage(self,message):
        if message == 'DISCONNECT':
            self.sendDisconnectMessage()
            QCoreApplication.quit()
            sys.exit()
        elif message == 'RESET':
            self.startGame()

    def processTextMessage(self,message):
#       print("server recieved message: {}".format(message))
        sender= self.sender()
        if len(message.split(';')) != 3:
                return
        m_type,m_subtype,m_val = message.split(';')

        if m_type == 'BROADCAST':
            for client in [c for c in self.clients if c!= sender]:
                client.sendTextMessage(message)
        elif m_type == 'REGISTER' and m_subtype == 'GM' and self.GM is None:
            self.GM = sender
            self.clients[sender] = 'GM'
            if not self.numPlayersNeeded:
                self.startGame()
        elif m_type == 'REGISTER' and m_subtype == 'PLAYER' and self.numPlayersNeeded:
            self.clients[sender] = m_val
            self.players[m_val] = sender
#           print( "player {} registered".format(m_val))
            self.numPlayersNeeded -= 1
            if self.numPlayersNeeded == 0 and self.GM is not None:
                self.startGame()
        elif self.clients[sender] == 'GM' and m_type == 'PRIVATE':
            self.players[m_subtype].sendTextMessage("REQUEST;PLAY;{}".format(m_val))
        elif self.clients[sender] == 'GM' and m_type == 'SERVER' and m_subtype == 'END':
            self.c_socket.sendTextMessage("DONE;{}".format(m_val))
        elif sender == self.players[m_type] and m_subtype == 'PLAY':
            self.GM.sendTextMessage(message)

    def sendDisconnectMessage(self):
        for c in self.clients:
            c.disconnected.disconnect(self.socketDisconnected)
            c.sendTextMessage("DISCONNECT;;")
        self.GM.sendTextMessage("SERVER;DISCONNECT;")

    def startGame(self):
        p_list = [v for v in self.clients.values() if not v in ['Logger','GM','Undefined']]
        self.GM.sendTextMessage("Server;Start;{}".format(str(p_list)))

    def socketDisconnected(self):
#       print('server lost connection to client')
        sender= self.sender()
        sender.deleteLater()
#        QCoreApplication.quit()    

if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    parser = argparse.ArgumentParser()
    parser.add_argument('-cp', '--conciergePort', type = int) 
    parser.add_argument('-n', '--numPlayers', type = int)
    args = parser.parse_args()
    if args.numPlayers is None:
        a = GameServer()
    else:
        a = GameServer(numPlayers = args.numPlayers, conciergePort = args.conciergePort)
    app.exec_()
