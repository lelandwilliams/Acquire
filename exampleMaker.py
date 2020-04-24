#! /usr/bin/python

from concierge import Concierge
import model, train
import subprocess, sys
from PyQt5.QtCore import QCoreApplication, QMutex, pyqtSignal
from PyQt5.QtNetwork import QHostAddress

DEFAULTPORT = 64337

Bots = ["randomClient.py", "reflexAgent2.py", "reflexAgent3.py",\
        "reflexAgent4.py"]

"""Provides class statsBuilder
"""

class statsBuilder(Concierge):
    """
    Parameters:
    -----------
    int my_id: not currently used
    int port: the network port number to use
    dict players: a dictionary of name -> playerfile entries


    """
    finished = pyqtSignal()
    completedGames = pyqtSignal(int)

    def __init__(
            self,
            my_id = None,
            port = DEFAULTPORT,
            address = QHostAddress.LocalHost,
            num_servers = 1,
            players = None):
        super().__init__(my_id, port, address, num_servers)
        self.player_dict = players
        self.num_games = 0
        self.max_games = 1
        self.fname = 'flex4_examples.gam'
        self.mutex = QMutex()


    def serverDone(self, game, server):
#       try:
#           _ = train.reconstruct_states(game)
#       except:
#           self.server.disconnect()
#           QCoreApplication.quit()
        self.mutex.lock()
        of = open(self.fname, 'a')
        of.write(game)
        of.write('\n')
        of.close()
        self.num_games += 1
        self.completedGames.emit(self.num_games)
        if self.num_games < self.max_games:
            server.sendTextMessage("RESET")
        else:
            server.sendTextMessage("DISCONNECT")
            self.servers_active -= 1
            self.server.disconnect()
            self.finished.emit()
        self.mutex.unlock()
        
        if self.servers_active == 0:
            QCoreApplication.quit()

#   def serverReady(self, port):
#       self.num_games += 1
#       subprocess.Popen(["python", "GM.py", "-p", port ])
#       for player in self.players:
#           subprocess.Popen(["python", players[player], "-p", port, "-n", player])

if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    f = open('playerDict.gam')
    players = eval(f.read())
    f.close()
    s = statsBuilder()
    s.players = players
    s.runGames()
    app.exec_()

            



