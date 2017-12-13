#! /usr/bin/python

from concierge import Concierge
import model
import subprocess, sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtNetwork import QHostAddress

DEFAULTPORT = 64337

class statsBuilder(Concierge):
    def __init__(
            self,
            my_id = None, 
            port = DEFAULTPORT, 
            address = QHostAddress.LocalHost,
            num_servers = 4,
            players = None):
        super().__init__(my_id, port, address, num_servers)
        self.players = players

    def runGames(self):
        subprocess.Popen(["python", 
                "gameServer.py", 
                "-cp", 
                str(self.port), 
                "-n", 
                str(len(self.players))])

    def serverDone(self, game, server):
        of = open('example.gam', 'w')
        of.write(game)
        of.write('\n')
        of.close()
        QCoreApplication.quit()

    def serverReady(self, port):
        subprocess.Popen(["python", "GM.py", "-p", port ])
        for player in self.players:
            subprocess.Popen(["python", players[player], "-p", port, "-n", player])

if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    f = open('playerDict.gam')
    players = eval(f.read())
    f.close()
    s = statsBuilder()
    s.players = players
    s.runGames()
    app.exec_()

            



