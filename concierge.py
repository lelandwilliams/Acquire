import sys, queue, uuid, argparse, subprocess
from PyQt5 import QtNetwork, QtWebSockets
from PyQt5.QtCore import QObject, QDataStream, pyqtSlot, QCoreApplication, QTimer

DEFAULTPORT = 64337

class Concierge(QObject):
    def __init__(self, 
            my_id = None, 
            port = DEFAULTPORT, 
            address = QtNetwork.QHostAddress.LocalHost):
        super().__init__()
        self.server = QtWebSockets.QWebSocketServer('',QtWebSockets.QWebSocketServer.NonSecureMode)
        self.port = port
        self.address = address
        self.readyServers = list()
        self.max_servers = 1
        self.serverObjects = []

        attempts = 0
        max_attempts = 10
        while attempts < max_attempts and not self.server.isListening():
            if self.server.listen(self.address, self.port):
                self.server.newConnection.connect(self.newClient)

        self.runGames()

    def newClient(self):
#       print('a new server connected to concierge')
        client = self.server.nextPendingConnection()
        client.textMessageReceived.connect(self.processTextMessage)
        client.disconnected.connect(self.socketDisconnected)
        self.serverObjects.append(client)

    def processTextMessage(self,message):
#       print("Concierge recieved message: {}".format(message))
        sender= self.sender()
        if len(message.split(';')) != 2:
                return
        m_type,m_body = message.split(';')
        print("Concierge recieved message: {}".format(m_type))

        if m_type == 'READY':
            self.serverReady(m_body)
        elif m_type == 'DONE':
            self.serverDone(m_body)

    def runGames(self):
        if len(self.readyServers) < self.max_servers:
            subprocess.Popen(["python", "gameServer.py", "-cp", str(self.port), "-n", '4'])

    def serverDone(self, port):
        print("Server Done ")

    def serverReady(self, port):
#       print("Concierge: a server said it is ready")
        process_list = list()
        process_list.append(["python", "gameClient.py", "-p", port, "-n", "Max"])
        process_list.append(["python", "gameClient.py", "-p", port, "-n", "Min1"])
        process_list.append(["python", "gameClient.py", "-p", port, "-n", "Min2"])
        process_list.append(["python", "gameClient.py", "-p", port, "-n", "Min3"])
        process_list.append(["python", "GM.py", "-p", port])

        for args in process_list:
            subprocess.Popen(args)

    def socketDisconnected(self):
        pass

if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
#   parser = argparse.ArgumentParser()
#   parser.add_argument('-cp', '--conciergePort', type = int) 
#   args = parser.parse_args()
    c = Concierge()
    app.exec_()
