from rules import *
from randomClient import RandomClient
from concierge import Concierge
import logging
from PyQt5.QtCore import QMutex


class HumanClient(RandomClient):
    """ An extension of RandomClient to control a GUI """
    def __init__(self):
        super().__init__(client_type = 'HUMAN', name = 'PunyHuman')
#       self.Concierge = None
        LOG_FORMAT = '%(levelname)s:%(module)s:%(message)s'
        logging.basicConfig(level = logging.INFO, format = LOG_FORMAT)
        self.event_queue = list()

    def announceBegin(self, players):
        """ Overrides base class

        """
        self.addPlayers(players)

    def announcePlay(self, play, action_type):
        """ Updates the UI after receiving notification from the game server of a play.


        """

        player = self.state['Turn']['Player']
        if action_type == 'Place':
            membership = None
            for group, tiles in self.state['Group'].items():
                if play in tiles:
                    membership = group
                    continue
            if 'Anon' in membership:
                self.changeTileColor(play, 'None')
            else:
                self.changeGroupColor(membership)
            model.print_state(self.state)
        elif action_type == 'Found':
            self.changeGroupColor(play)
            stock = dict()
            for corp in model.corporations:
                stock[corp] = self.state['Players'][player][corp]
            self.pb.updatePlayerStock(player, stock)
        elif action_type == 'Choose Survivor':
            pass
        elif action_type == 'Liquidate':
            # for now, same routine as in 'Buy' below
            money = self.state['Players'][player]['money']
            self.pb.updatePlayerMoney(player, money)
            stock = dict()
            for corp in model.corporations:
                stock[corp] = self.state['Players'][player][corp]
            self.pb.updatePlayerStock(player, stock)
        elif action_type == 'Buy':
            #money = self.state['Players'][player]['money']
            #self.pb.updatePlayerMoney(player, money)
            #stock = dict()
            #for corp in model.corporations:
            #    stock[corp] = self.state['Players'][player][corp]
            #self.pb.updatePlayerStock(player, stock)
            self.pb.updateAllPlayers(self.state)
            if not self.state['Turn']['Merger'] is None:
                for newCorp in self.state['Turn']['Merger']['NewCorps']:
                    for tile in self.state['Group'][newCorp]:
                        self.board.changeTileColor(tile, newCorp)
        elif action_type == 'Trade':
            self.pb.updateAllPlayers(self.state)
        elif action_type == 'Call':
            self.pb.updateAllPlayers(self.state)
            self.announceGameOver(player)
        else:
            logging.error("action_type {} not handled".format(action_type))

    def chooseNewCompany(self, actions):
        """ Handles the action to choose which new corporation to found.
        """
        return self.chooseNewCorp(actions)

    def chooseSurvivor(self, actions): return random.choice(actions)

    def chooseLiquidate(self, actions):
        """ Ask the human player what to do with stock in acquired corporation.

        Parameters:
        ___________
        actions : list(str)
            a list of strings containing the actions.
            possible actions include 'Sell' 'Trade' 'All' 'Done'

        Returns:
        --------
        str : the action chosen by the player from the given options
        """

        # First discover which sale is currently being processed
        idx = 0
        while self.state['Turn']['Merger']['Sales'][idx]['Done']:
           idx += 1 
        sale  = self.state['Turn']['Merger']['Sales'][idx]

        # Obtain corporation, and obtain action
        corp = sale['Corporation']
        largestCorp = self.state['Turn']['Merger']['NewCorps'][0]

        return self.chooseMergerStockAction(corp, largestCorp, actions)

    def chooseEndGame(self, actions): return "Yes"

    def enqueueTextMessage(self, message):
        """ Puts valid incoming messages into the event_queue, until 
        a REQUEST message is recieved, in which case it enpties the queue """

        if len(message.split(';')) != 3:
            return
        self.event_queue.append(message)
        m_type, m_subtype, m_body = message.split(';')
        if m_type == 'REQUEST' or m_body == 'Yes':
            while len(self.event_queue) > 0:
                self.processTextMessage(self.event_queue.pop(0))

    def newGame(self):
        """ Begin a new game

        A function specific to this subclass.

        Begins by starting a new Concierge. 
        When the the Concierge finds an available server,
        the method self.connectToServer() will be called.

        TODO:
            [ ] Connect to a remote concierge.
        """
        if self.concierge is None:
            self.concierge = Concierge()
            self.concierge.process_list.append(["python", "randomClient.py", "-n", "Random1"])
            self.concierge.process_list.append(["python", "randomClient.py", "-n", "Random2"])
            self.concierge.process_list.append(["python", "randomClient.py", "-n", "Random3"])
        self.concierge.serverAvailable.connect(self.serverAvailable)
        self.concierge.runGames()

    def onConnected(self):
        """ Overrides parent class method
            called by signal when self.socket successfully connects to a game server
            connects the the sockets recieve signal to enqueueTextMessage() 
            sends it's information to the game server

            args:
                none

            returns:
                nothing
        """
        self.socket.textMessageReceived.connect(self.enqueueTextMessage)
        self.socket.sendTextMessage('REGISTER;{};{}'.format(self.client_type, self.name))


    def onDisconnected(self):
        """ Overrides parent method. Removes closing application command.

        TODO: Add a disconnection handling routine in cases that game is still in session
        
        ____"""
        self.socket.close()

    def serverAvailable(self, port):
        self.serverPort = port
        self.concierge.serverAvailable.disconnect(self.serverAvailable)
        self.connectToServer(port = self.serverPort)

    def quit(self):
        """ Routine to handle receipt of a DISCONNECT message

        Overrides parent routine.
        """
        self.socket.close()
