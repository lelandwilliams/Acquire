from rules import *
from randomClient import RandomClient
from concierge import Concierge
import logging
from PyQt5.QtCore import QMutex, QTimer, Qt


class HumanClient(RandomClient):
    """ An extension of RandomClient to control a GUI """
    def __init__(self):
        super().__init__(client_type = 'HUMAN', name = 'PunyHuman')
#       self.Concierge = None
        LOG_FORMAT = '%(levelname)s:%(module)s:%(message)s'
        logging.basicConfig(level = logging.INFO, format = LOG_FORMAT)

        self.event_queue = list()
        self.eq_mutex = QMutex() # eq = event_queue

        self.use_timers = True
        self.event_delay = 400
        self.empty_timer = 200

    def announceBegin(self, players):
        """ Overrides base class

        """
        self.addPlayers(players)
        if self.use_timers:
            QTimer.singleShot(self.event_delay, self.de_enqueueTextMessage)

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

        if self.use_timers:
            QTimer.singleShot(self.event_delay, Qt.PreciseTimer, self.de_enqueueTextMessage)

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

        choice = self.chooseMergerStockAction(corp, largestCorp, actions)
        if self.use_timers:
            QTimer.singleShot(self.ui_time, Qt.PreciseTimer, self.de_enqueueTextMessage)
        return choice

    def chooseEndGame(self, actions): return "Yes"

    def de_enqueueTextMessage(self):
        """ This method is the target of the timer. It removes the front event
        from the queue and processes it. If there is no event it sets a timer to call itself. """
        assert(self.use_timers)
        self.eq_mutex.lock()
        q_length =  len(self.event_queue)
        self.eq_mutex.unlock()
        if q_length == 0:
            QTimer.singleShot(self.empty_timer, self.de_enqueueTextMessage)
        else:
            self.eq_mutex.lock()
            event = (self.event_queue.pop(0))
            self.eq_mutex.unlock()
            self.processTextMessage(event)

    def enqueueTextMessage(self, message):
        """ Puts valid incoming messages into the event_queue, until 
        a REQUEST message is recieved, in which case it enpties the queue """

        if len(message.split(';')) != 3:
            return
        self.eq_mutex.lock()
        self.event_queue.append(message)
        self.eq_mutex.unlock()
        m_type, m_subtype, m_body = message.split(';')

        if self.use_timers and m_subtype == "BEGIN":
            QTimer.singleShot(400, self.de_enqueueTextMessage)
        elif not self.use_timers and m_type == 'REQUEST' or m_body == 'Yes':
            self.eq_mutex.lock()
            queue_length = len(self.event_queue)
            self.eq_mutex.unlock()
            while queue_length > 0:
                self.eq_mutex.lock()
                event = (self.event_queue.pop(0))
                queue_length = len(self.event_queue)
                self.eq_mutex.unlock()
                self.processTextMessage(event)

    def newGame(self):
        """ DEPRECATED - Begin a new game

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
