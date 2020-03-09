from concierge import Concierge
import model
import subprocess, sys
from PyQt5.QtCore import QCoreApplication, pyqtSignal
from PyQt5.QtNetwork import QHostAddress

DEFAULTPORT = 64337

class statsBuilder(Concierge):
    completedRounds = pyqtSignal(int)
    gamesComplete = pyqtSignal()

    def __init__(
            self,
            my_id = None, 
            port = DEFAULTPORT, 
            address = QHostAddress.LocalHost,
            num_servers = 4,
            players = None):
        super().__init__(my_id, port, address, num_servers)
        self.players = players
        self.num_games_desired = 1000
        self.filename = "results.csv"


    def runGames(self):
        header = str()
        for player in self.players:
            header += "{} score,".format(player)
        for player in self.players:
            header += "{} won,".format(player)
        of = open(self.filename, 'a')
        of.write(header[:-1])
        of.write('\n')
        of.close()
        for i in range(self.num_servers):
            subprocess.Popen(["python", 
                    "gameServer.py", 
                    "-cp", 
                    str(self.port), 
                    "-n", 
                    str(len(self.players))])

    def serverDone(self,game, server):
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
        of = open('results.csv', 'a')
        of.write(line[:-1])
        of.write('\n')
        of.close()

        if self.num_games < self.num_games_desired:
            self.num_games += 1
            server.sendTextMessage("RESET")
        else:
            server.sendTextMessage("DISCONNECT")
            QCoreApplication.quit()

    def serverReady(self, port):
        subprocess.Popen(["python", "GM.py", "-p", port ])
        for player in self.players:
            subprocess.Popen(["python", players[player], "-p", port, "-n", player])

if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    players = dict()
#   players['Random1'] = 'randomClient.py'
#   players['Random2'] = 'randomClient.py'
#   players['Random3'] = 'randomClient.py'
    players['Flex4'] = 'reflexAgent4.py'
    players['Flex3'] = 'reflexAgent3.py'
    players['Flex1'] = 'reflexAgent.py'
    players['Flex2'] = 'reflexAgent2.py'
    s = statsBuilder()
    s.players = players
    s.runGames()
    app.exec_()

            



