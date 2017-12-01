import sys, collections, uuid, argparse
from PyQt5.QtCore import QObject, QUrl, QTimer, QCoreApplication, pyqtSlot, QThread
from PyQt5.QtWebSockets import QWebSocket, QWebSocketProtocol

DEFAULTPORT = 64337

class AcquireClient(QObject):
    def __init__(self, 
            client_id = None, 
            port = DEFAULTPORT, 
            address = 'localhost',
            name = 'Noname',
            client_type = 'PLAYER'):
        super().__init__()
        self.socket = QWebSocket()
        self.name = name
        self.client_type = client_type
        self.failed_attempts = 0
        self.max_attempts = 5

        self.url = QUrl()
        self.url.setScheme("ws")
        self.url.setHost(address)
        self.url.setPort(port)
        self.socket.error.connect(self.error)
        self.socket.connected.connect(self.onConnected)
        self.socket.disconnected.connect(self.onDisconnected)
        
        self.openSocket()

    def openSocket(self):
        print('{} attempting connection...'.format(self.name))
        self.socket.open(self.url)

    def error(self, errorcode):
        print("Client Error #{}: ".format(errorcode))
        print(self.socket.errorString())
        self.failed_attempts += 1
        if errorcode == 0 and self.failed_attempts < self.max_attempts:
            QTimer.singleShot(2000, self.openSocket)

    def onConnected(self):
        print('Client Connected')
        self.socket.textMessageReceived.connect(self.processTextMessage)
        self.socket.sendTextMessage('REGISTER;{};{}'.format(self.client_type, self.name))

    def onDisconnected(self):
        self.socket.close()
        QCoreApplication.quit()

    def processTextMessage(self, message):
        print("client recieved message: {}".format(message))

    def send_message(self):
        print('Client sending message')
        self.socket.sendTextMessage('REGISTER;PLAYER;C3PO')
        self.socket.sendTextMessage('Howdy')
        QTimer.singleShot(1000, a.quit_app)
        return

    def send_message_from_queue(self, s):
        print('Client sending message')
        self.socket.sendTextMessage(s)
        QTimer.singleShot(1000, a.quit_app)
        return

    def quit_app(self):
        QCoreApplication.quit()

if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--playerType', type = str, 
            choices = ['GM','LOGGER', 'PLAYER'])
    parser.add_argument('-n', '--playerName', type = str)
    args = parser.parse_args()
    a = AcquireClient(name = args.playerName, client_type = args.playerType)
#   QTimer.singleShot(1000, a.send_message)

    QTimer.singleShot(9000, a.quit_app)
    app.exec_()

