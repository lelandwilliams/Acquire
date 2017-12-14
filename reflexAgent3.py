from randomClient import RandomClient
from featureExtractor import *
import model
import random, argparse, sys
from PyQt5.QtCore import QCoreApplication

class reflexAgent(RandomClient):
    def __init__(self, client_id = None, serverPort = 0, 
            serverAddress = 'localhost', name = 'Noname', client_type = 'PLAYER'):
        super().__init__(client_id, serverPort, serverAddress, name, client_type)

        
    def chooseTile(self, actions):
        if len(actions) == 1: # covers the case that the only tile is 'Nothing'
            return actions[0]
        outcomes = placementOutcome(self.state, actions)
        good_choices = list()
        for k,v in outcomes:
            if v == 'found':
                good_choices.append(v)
            elif v == 'merger':
                # find what companies the tile merges
                # and don't play it if no interest in the merger
                nb = neighbors(k)
                corps = list()
                for n in nb:
                    for c in model.corporations:
                        if n in self.state['Group'][c]:
                            corps.append(c)
                corp_interests = [c for c in corps if self.name in model.getBonusPlayers(self.state,c)]
                if len(corp_interests):
                    good_choices.append(k)

        if len(good_choices):
            return random.choice(good_choices)
        return random.choice(actions)

    def chooseNewCompany(self, actions): return random.choice(actions)
    def chooseSurvivor(self, actions): return random.choice(actions)
    def chooseLiquidate(self, actions): return random.choice(actions)

    def chooseStock(self, actions): 
        actions.remove('Done')
        if len(actions) == 0:
            return 'Done'
        if len(actions) == 1:
            return actions[0]

        choices = list()
        for company in actions:
            bonuses = getBonus(self.state, company) 
            if bonuses[0]['Player'] == bonuses[1]['Player'] and bonuses[0]['Player'] != self.name:
                choices.append(company)
            elif self.name != bonuses[0]['Player'] and self.name != bonuses[1]['Player']:
                choices.append(company)

        if len(choices):
            return random.choice(choices)
        else:
            return random.choice(actions)

    def chooseEndGame(self, actions): return "Yes"








if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--serverPort', type = int)
    parser.add_argument('-n', '--playerName', type = str)
    args = parser.parse_args()
    a = reflexAgent(name = args.playerName, serverPort = args.serverPort)
    app.exec_()

