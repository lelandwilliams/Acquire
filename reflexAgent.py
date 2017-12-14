from randomClient import RandomClient
from featureExtractor import *
import random, argparse, sys
from PyQt5.QtCore import QCoreApplication

class reflexAgent(RandomClient):
    def __init__(self, client_id = None, serverPort = 0, 
            serverAddress = 'localhost', name = 'Noname', client_type = 'PLAYER'):
        super().__init__(client_id, serverPort, serverAddress, name, client_type)

        
    def chooseTile(self, actions):
        if len(actions) == 1:
            return actions[0]
        outcomes = placementOutcome(self.state, actions)
        for k,v in outcomes:
            if v == 'found':
                return k
        return random.choice(actions)

    def chooseNewCompany(self, actions): return random.choice(actions)
    def chooseSurvivor(self, actions): return random.choice(actions)
    def chooseLiquidate(self, actions): return random.choice(actions)
    def chooseStock(self, actions): 
        if len(actions) == 1:
            return actions[0]
        choice = actions[0]
        for company in actions[1:]:
            if company == 'Done':
                continue
            elif stockPrice(self.state, company) < stockPrice(self.state, choice):
                choice = company
            elif stockPrice(self.state, company) == stockPrice(self.state, choice) and random.random() < 0.5:
                choice = company
        return choice

    def chooseEndGame(self, actions): return "Yes"








if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--serverPort', type = int)
    parser.add_argument('-n', '--playerName', type = str)
    args = parser.parse_args()
    a = reflexAgent(name = args.playerName, serverPort = args.serverPort)
    app.exec_()

