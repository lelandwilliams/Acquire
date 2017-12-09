from rules import *
from PyQt5.QtCore import QCoreApplication, QUrl, QObject
from PyQt5.QtWebSockets import QWebSocket, QWebSocketProtocol
import random, sys, argparse

class RandomClient(QObject):
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
        self.state = None
        self.hand = None
        self.history = None

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
        print("Client Error #{}: ".format(errorcode))
        print(self.socket.errorString())

    def onConnected(self):
        self.socket.textMessageReceived.connect(self.processTextMessage)
        self.socket.sendTextMessage('REGISTER;{};{}'.format(self.client_type, self.name))

    def onDisconnected(self):
        if self.name == "Min1":
            print(self.state)
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
        elif m_type == 'BROADCAST' and m_subtype == 'BEGIN':
            self.state = model.new_game(eval(m_body))
        elif m_type == 'BROADCAST' and m_subtype == 'PLAY':
            if m_body[0] == '(':
                m_body = eval(m_body)
            self.state, self.hands = succ(self.state, None, m_body, self.history)
        elif m_type == 'DISCONNECT':
            self.quit()

    def chooseAction(self, actions):
        """ This is the good candidate to be overidden by subclasses """
#       choices = actions[-1][0]
        choices = actions[-1]
        if len(choices) == 1:
            return choices[0]
        else:
            return random.choice(choices)

    def quit(self):
        if self.name == "Min1":
            print(self.state)
        QCoreApplication.quit()
        sys.exit()

if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--serverPort', type = int)
    parser.add_argument('-n', '--playerName', type = str)
    args = parser.parse_args()
    a = RandomClient(name = args.playerName, serverPort = args.serverPort)
    app.exec_()

