from randomClient import RandomClient
from featureExtractor import *
import random, argparse, sys
from PyQt5.QtCore import QCoreApplication

class reflexAgent(RandomClient):
    def __init__(self, client_id = None, serverPort = 0, 
            serverAddress = 'localhost', name = 'Noname', client_type = 'PLAYER'):
        super().__init__(client_id, serverPort, serverAddress, name, client_type)
        f = open('weights.gam')
        self.gw = eval(f.readline())
        self.dw = eval(f.readline())
        f.close()
        
    def chooseTile(self, actions):
        if len(actions) == 1: # covers the case that the only tile is 'Nothing'
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
        actions.remove('Done')
        if len(actions) == 0:
            return 'Done'
        if len(actions) == 1:
            return actions[0]

        choices = list()
        shortTermCorps = list()
        longTermCorps = list()
        for company in actions:
            bonuses = getBonus(self.state, company) 
            if bonuses[0]['Player'] == bonuses[1]['Player'] and bonuses[0]['Player'] != self.name:
                return company

            cur_length = len(self.state['Group'][company])
            if cur_length > 10:
                longTermCorps.append(company)
            elif cur_length + int(dot_product(feature_extractor(self.state, company), self.gw)) > 10:
                longTermCorps.append(company)
            elif dot_product(feature_extractor(self.state, company), self.dw) < 12:
                shortTermCorps.append(company)

        if self.state['Players'][self.name]['money'] < 5000 and len(shortTermCorps) > 0:
            for company in shortTermCorps:
                bonuses = getBonus(self.state, company) 
                if bonuses[0]['Player'] != self.name and bonuses[1]['Player'] != self.name\
                    and self.state['Players'][bonuses[1]['Player']][company] - \
                    self.state['Players'][self.name][company] <= 3:
                        choices.append(company)
            if len(choices):
                return random.choice(choices)
        elif len(longTermCorps):
            choice = None
            highest_growth = 0
            for company in longTermCorps:
                expectation =  int(dot_product(feature_extractor(self.state, company), self.gw)) 
                if expectation > highest_growth:
                    highest_growth = expectation
                    choice = company
            if choice is not None:
                return choice

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

