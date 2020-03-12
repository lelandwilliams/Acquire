from concierge import Concierge
import model
import subprocess, sys
from PyQt5.QtCore import QCoreApplication, pyqtSignal
from PyQt5.QtNetwork import QHostAddress

DEFAULTPORT = 64337

class statsBuilder(Concierge):
    """ statsBuilder
    This class extends Concierge to create a game runner solely to generate data from
    bot players.

    It's original use was to run games and record the final scores and the winner.
    It is being overhauled to record (optionally) the entire game's data.
    """
    completedRounds = pyqtSignal(int)
    roundComplete = pyqtSignal()
    ready = pyqtSignal()

    def __init__(
            self,
            my_id = None, 
            port = DEFAULTPORT, 
            address = QHostAddress.LocalHost,
            num_servers = 1,
            players = None):
        super().__init__(my_id, port, address, num_servers)
        self.players = players
        self.num_games_desired = 1000
        self.filename = "results.csv"
        self.num_servers = num_servers
        self.evaluate_results = False
        self.num_games_finished = 0
        self.interupt = False
        self.managed = False

    def startServers(self):
        if self.evaluate_results:
            self.printHeader()

        for i in range(self.num_servers):
            subprocess.Popen(["python", 
                    "gameServer.py", 
                    "-cp", 
                    str(self.port), 
                    "-n", 
                    str(len(self.players))])

        if self.managed:
            self.roundComplete.connect(self.serverManage)

    def printHeader(self):
        header = str()
        for player in self.players:
            header += "{} score,".format(player)
        for player in self.players:
            header += "{} won,".format(player)
        of = open(self.filename, 'a')
        of.write(header[:-1])
        of.write('\n')
        of.close()

    def serverDone(self, game, server):
        """ called when a server reports to the concierge that a game is finished """
        if self.evaluate_results:
            s, hist = eval(game)
            player_scores = dict()
            player_won = dict()
            for player in self.players:
                player_scores[player] = model.netWorth(player, s)
            for player in self.players:
                player_won[player] = int(player_scores[player] == max(player_scores.values()))
            line = str()
            for player in self.players:
                line += "{},".format(player_scores[player])
            for player in self.players:
                line += "{},".format(player_won[player])
            of = open(self.filename, 'a')
            of.write(line[:-1])
            of.write('\n')
            of.close()
        else:
            of = open(self.filename, 'a')
            of.write(game)
            of.write('\n')
            of.close()

        self.num_games_finished += 1
        self.readyServers.append(server)
        self.roundComplete.emit()

    def serverDisconnect(self):
        if len(self.readyServers) > 0:
            server = self.readyServers.pop()
            server.sendTextMessage("DISCONNECT")

    def serverReset(self):
        if len(self.readyServers) > 0:
            server = self.readyServers.pop()
            server.sendTextMessage("RESET")
    
    def serverManage(self):
        """ provides a method to run the desired number of games """
        if self.interupt:
            self.serverDisconnect()
        elif self.num_games_finished < self.num_games_desired:
            self.serverReset()
        else:
            self.serverDisconnect()
            QCoreApplication.quit()

    def serverReady(self, port):
        """ serverReady()
        called when the concierge recieves a ready message from one of the
        game servers it manages
        """
        subprocess.Popen(["python", "GM.py", "-p", port ])
        for player in self.players:
            subprocess.Popen(["python", players[player], "-p", port, "-n", player])

if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    players = dict()
    players['Random1'] = 'randomClient.py'
#   players['Random2'] = 'randomClient.py'
#   players['Random3'] = 'randomClient.py'
#   players['Flex4'] = 'reflexAgent4.py'
    players['Flex3'] = 'reflexAgent3.py'
    players['Flex1'] = 'reflexAgent.py'
    players['Flex2'] = 'reflexAgent2.py'
    s = statsBuilder()
    s.players = players
    s.num_games_desired = 1
    s.evaluate_results = False
    s.managed = True
    s.startServers()
    app.exec_()

            



