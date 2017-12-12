from rules import *
from PyQt5.QtCore import QCoreApplication, QUrl, QObject
from PyQt5.QtWebSockets import QWebSocket, QWebSocketProtocol
import random, sys, argparse

class GameClient(QObject):
    def __init__(self, 
            client_id = None, 
            serverPort = 0, 
            serverAddress = 'localhost',
            name = 'Noname',
            client_type = 'PLAYER'):

        super().__init__()
        self.client_id = client_id
        self.name = name
        self.client_type = client_type
        self.connectToServer(serverAddress, serverPort)

    def connectToServer(self, address, port):
        self.socket = QWebSocket()
        url = QUrl()
        url.setScheme("ws")
        url.setHost(address)
        url.setPort(port)
        self.socket.error.connect(self.error)
        self.socket.connected.connect(self.onConnected)
        self.socket.disconnected.connect(self.onDisconnected)
        self.socket.open(url)

    def error(self, errorcode):
        if errorcode != 1:
            print("{}: Error #{}: ".format(self.name, errorcode))
            print(self.socket.errorString())

    def onConnected(self):
        self.socket.textMessageReceived.connect(self.processTextMessage)
        self.socket.sendTextMessage('REGISTER;{};{}'.format(self.client_type, self.name))

    def onDisconnected(self):
        self.socket.close()
        QCoreApplication.quit()

    def processTextMessage(self, message):
#       print("{} recieved message: {}".format(self.name, message))
        if len(message.split(';')) != 3:
            return
        m_type, m_subtype, m_body = message.split(';')
        if m_type == 'REQUEST' and m_subtype == 'PLAY':
            choice =  self.chooseAction(eval(m_body))
            self.socket.sendTextMessage("{};{};{}".format(self.name, 'PLAY', choice))
        elif m_type == 'DISCONNECT':
            QCoreApplication.quit()
            sys.exit()

    def chooseAction(self, actions):
        return actions[-1][0]

if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--serverPort', type = int)
    parser.add_argument('-n', '--playerName', type = str)
    args = parser.parse_args()
    a = GameClient(name = args.playerName, serverPort = args.serverPort)
    app.exec_()

