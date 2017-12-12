from gameClient import GameClient
from rules import *
from PyQt5.QtCore import QCoreApplication
import sys, argparse, random

class GM(GameClient):
    def __init__(self, client_id = None, serverPort = 0, serverAddress = 'localhost', seed = None):
        super().__init__(client_id, serverPort, serverAddress, 'GM', 'GM')
        self.game_in_progress = False
        self.seed = seed if seed is not None else random.randrange(sys.maxsize)
        self.history = []
        self.cur_actions = None

    def processTextMessage(self, message):
#       print("GM recieved message: {}".format(message))
        if len(message.split(';')) != 3:
            return
        sender, m_type, m_body = message.split(';')
        if not self.cur_actions is None and self.cur_actions[0] == 'Place':
            m_body = eval(m_body) if m_body != 'Nothing' else 'Nothing'

        if sender == 'Server' and m_type == 'Start':
            self.startGame(eval(m_body))
        elif sender == self.cur_player and m_type == 'PLAY' and m_body in self.cur_actions[-1]:
            self.resolveAction(m_body)
        elif sender != 'SERVER' and m_type == 'DISCONNECT':
            QCoreApplication.quit()
            sys.exit()

    def startGame(self, players):
#       print(players)
        players.sort()
        if self.game_in_progress:
            return
        self.game_in_progress = True
        self.players = players
        self.state, self.hands = new_game(players, True, self.seed)
#       model.print_turn(self.state['Turn'])
        self.socket.sendTextMessage('BROADCAST;BEGIN;{}'.format(players)) 
        self.nextAction()

    def nextAction(self):
        self.cur_actions = getActions(self.state, self.hands)
        if len(self.cur_actions) == 2:
            self.cur_player = self.state['Turn']['Player']
        else:
            self.cur_player = self.cur_actions[1]
        self.socket.sendTextMessage("{};{};{}".format('PRIVATE',self.cur_player, self.cur_actions))

    def resolveAction(self, a):
        self.state, self.hands = succ(self.state, self.hands, a, self.history)
        if a == 'Yes':
            self.socket.sendTextMessage('BROADCAST;INFO;Game Over') 
            self.socket.sendTextMessage("{};{};{}".format('SERVER', 'END', (self.state,self.history)))
            self.game_in_progress = False
        else:
            self.socket.sendTextMessage("BROADCAST;PLAY;{}".format(a))
            self.nextAction()

    def quit(self):
        pass


if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--serverPort', type = int)
    parser.add_argument('-s', '--seed', type = int)
    args = parser.parse_args()
    a = GM(serverPort = args.serverPort, seed = args.seed)
    app.exec_()

