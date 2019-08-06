import sys, queue, uuid, argparse, subprocess, statistics
from PyQt5 import QtNetwork, QtWebSockets
from PyQt5.QtCore import QObject, QDataStream, pyqtSlot, QCoreApplication, QTimer
import model

DEFAULTPORT = 64337

class Concierge(QObject):
    """ A Server Management Class """
    def __init__(self, 
            my_id = None, 
            port = DEFAULTPORT, 
            address = QtNetwork.QHostAddress.LocalHost,
            num_servers = 1):
        super().__init__()
        self.server = QtWebSockets.QWebSocketServer('',QtWebSockets.QWebSocketServer.NonSecureMode)
        self.port = port
        self.address = address
        self.readyServers = list()
        self.num_servers = num_servers
        self.max_servers = 1
        self.serverPort = 0
        self.serverPorts = dict()
        self.servers_active = 0
        self.servers = list() # A place to store obj references so the garbarge collector
                            # won't take them away

        attempts = 0
        max_attempts = 10

        while attempts < max_attempts and not self.server.isListening():
            if self.server.listen(self.address, self.port):
                self.server.newConnection.connect(self.newClient)
#               print("Concierge listening on port {}".format(self.port))
            else:
                self.port += 1
        if not self.server.isListening():
            raise('Concierge unable to bind port')

        self.game_seed = 0
        self.num_games = 0
        self.scores = list()
        self.highscores = list()

#       self.runGames()

    def newClient(self):
#       print('a new server connected to concierge')
        client = self.server.nextPendingConnection()
        client.textMessageReceived.connect(self.processTextMessage)
        client.disconnected.connect(self.socketDisconnected)
        self.servers.append(client) # solely to keep the garbage collector from destroying

    def processTextMessage(self,message):
#       print("Concierge recieved message: {}".format(message))
        sender= self.sender()
        if len(message.split(';')) != 2:
                return
        m_type,m_body = message.split(';')
#       print("Concierge recieved message: {}".format(m_type))

        if m_type == 'READY':
            self.serverPorts[sender] = m_body
            self.serverReady(m_body)
        elif m_type == 'DONE':
            self.serverDone(m_body, sender)

    def runGames(self):
#       self.of = open('results.txt', 'w')
#       self.of.write("{:^3}, {:^8}, {:^8}, {:^5}, {:^8}, {:^8}\n".format('num','avg','std','max','w_avg','w_std'))
#       self.of.close()
#       self.num_games += 1
#       if len(self.readyServers) < self.max_servers:
        for i in range(self.num_servers):
            self.servers_active += 1
            subprocess.Popen(["python", "gameServer.py", "-cp", str(self.port), "-n", '4'])

    def serverDone(self, game, server):
        s, hist = eval(game)
#       for h in hist:
#           model.print_turn(h)
        print("\rResults of game # {}".format(self.num_games))
        for player in [p for p in s['Players'] if p != 'Bank']:
            print("{}: {}".format(player, model.netWorth(player, s)))
        scores = [model.netWorth(player, s) for player in s['Players'] if player != "Bank"]
        self.highscores.append(max(scores))
        self.scores += scores
        if self.num_games < 1:
            self.num_games += 1
#           print("\rRunning game # {}".format(self.num_games), end = '')
            server.sendTextMessage("RESET")
#           self.serverReady(self.serverPort)
        else:
#           self.of = open('results.txt', 'a')
#           self.of.write("{:3d}, {:6.2f}, {:6.2f}, {:5}, {:6.2f}, {:6.2f}\n".format(self.game_seed,
#                   statistics.mean(self.scores),
#                   statistics.stdev(self.scores),
#                   max(self.highscores),
#                   statistics.mean(self.highscores),
#                   statistics.stdev(self.highscores)))
#           self.of.close()
            server.sendTextMessage("DISCONNECT")
            if self.game_seed == 1000:
                self.num_games = 0
                self.scores = list()
                self.highscores = list()
                self.game_seed += 1
                self.runGames()
            else:
                QCoreApplication.quit()

#          print("Average Score was {:5.2f} with a std dev of {:5.2f}".format(
#               statistics.mean(self.scores), statistics.stdev(self.scores)))
#           print("Average High Score was {:5.2f} with a std dev of {:5.2f}".format(
#               statistics.mean(self.highscores), statistics.stdev(self.highscores)))

    def serverReady(self, port):
#       print("Concierge: a server said it is ready")
        process_list = list()
        process_list.append(["python", "randomClient.py", "-p", port, "-n", "Random1"])
        process_list.append(["python", "randomClient.py", "-p", port, "-n", "Random2"])
        process_list.append(["python", "reflexAgent.py", "-p", port, "-n", "Flex1"])
        process_list.append(["python", "reflexAgent2.py", "-p", port, "-n", "Flex2"])
        process_list.append(["python", "GM.py", "-p", port, "-s", str(self.game_seed)])

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
    c.runGames()
    app.exec_()
