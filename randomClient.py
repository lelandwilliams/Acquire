from rules import *
from PyQt5.QtCore import QCoreApplication, QUrl, QObject
from PyQt5.QtWebSockets import QWebSocket, QWebSocketProtocol
import random, sys, argparse

class RandomClient(QObject):
    """ A base class for all networked clients
        Provides methods to communicate with a game server, and parse it's methods
        Provides methods to make choices, called chooseXXX()
        Non-random clients need only override those choice methods.

        Args:
            client_id (str): not currently used
            serverPort (int): the port number of the game server
            serverAddress (str): the address of the game server, defaults to localhost
            name (str): The name of the player
            client_type (str): if the client is a GM, a PLAYER, or a LOGGER

        Attributes:
            name (str): the name of the player
            client_type (str): if the client is a GM, a PLAYER, or a LOGGER
            state (dict): the current state of the game board, players, and stock
            hand (list): the tile held in the player's 'hand'
            history (dict): all the moves that have happened in the game
            socket (QWebsocket): the socket class, set by connectToServer()

        Todo:
            [ ] Code to handle network failures
            [ ] Code to create nonnetworked clients, perhaps have network code as an addin
    """

    def __init__(self, 
            client_id = None, 
            serverPort = 0, 
            serverAddress = 'localhost',
            name = 'Noname',
            client_type = 'PLAYER'):

        super().__init__()
#        self.client_id = client_id
        self.name = name
        self.client_type = client_type
        self.connectToServer(serverAddress, serverPort)
        self.state = None
        self.hand = None
        self.history = None

    def connectToServer(self, address, port):
        """ Connects to game server, and sends a signal to onConnected() when connected

            args:
                address (str): the address of the game server.
                port (int): the port number of the game server. 
            
            returns:
                nothing
        """

        self.socket = QWebSocket()
        url = QUrl()
        url.setScheme("ws")
        url.setHost(address)
        url.setPort(port)
        self.socket.error.connect(self.error)
        self.socket.connected.connect(self.onConnected)
        self.socket.disconnected.connect(self.onDisconnected)
        self.socket.open(url)

    def error(self, errorcode):
        """ Routine to handle an error message from server"""
        if errorcode != 1:
            print("{}: Error #{}: ".format(self.name, errorcode))
            print(self.socket.errorString())

    def onConnected(self):
        """ called by signal when self.socket successfully connects to a game server
            connects the the sockets recieve signal to procesTextMessage() 
            sends it's information to the game server

            args:
                none

            returns:
                nothing
        """
        self.socket.textMessageReceived.connect(self.processTextMessage)
        self.socket.sendTextMessage('REGISTER;{};{}'.format(self.client_type, self.name))

    def onDisconnected(self):
#       if self.name == "Min1":
#           print(self.state)
        self.socket.close()
        QCoreApplication.quit()

    def processTextMessage(self, message):
        """ The central client routine, it parses a message from the server and calls the relevant handling routine"""
#       print("{} recieved message: {}".format(self.name, message))
        if len(message.split(';')) != 3:
            return
        m_type, m_subtype, m_body = message.split(';')
        if m_type == 'REQUEST' and m_subtype == 'PLAY':
#           choice =  self.chooseAction(eval(m_body))
#           self.socket.sendTextMessage("{};{};{}".format(self.name, 'PLAY', choice))
            actions = eval(m_body)
            if actions[0] == 'Place':
                choice = self.chooseTile(actions[-1])
                self.socket.sendTextMessage("{};{};{}".format(self.name, 'PLAY', choice))
            elif actions[0] == 'Found':
                choice = self.chooseNewCompany(actions[-1])
                self.socket.sendTextMessage("{};{};{}".format(self.name, 'PLAY', choice))
            elif actions[0] == 'Choose Survivor':
                choice = self.chooseSurvivor(actions[-1])
                self.socket.sendTextMessage("{};{};{}".format(self.name, 'PLAY', choice))
            elif actions[0] == 'Liquidate':
                choice = self.chooseLiquidate(actions[-1])
                self.socket.sendTextMessage("{};{};{}".format(self.name, 'PLAY', choice))
            elif actions[0] == 'Buy':
                choice = self.chooseStock(actions[-1])
                self.socket.sendTextMessage("{};{};{}".format(self.name, 'PLAY', choice))
            elif actions[0] == 'Call':
                choice = self.chooseEndGame(actions[-1])
                self.socket.sendTextMessage("{};{};{}".format(self.name, 'PLAY', choice))
        elif m_type == 'BROADCAST' and m_subtype == 'BEGIN':
            self.announceBegin()
            self.state = model.new_game(eval(m_body))
        elif m_type == 'BROADCAST' and m_subtype == 'PLAY':
            if m_body[0] in ['(','[']:
                m_body = eval(m_body)
            self.announcePlay(m_body)
            self.state, self.hands = succ(self.state, None, m_body, self.history)
        elif m_type == 'DISCONNECT':
            self.quit()

    def announceBegin(self): pass
    def announcePlay(self, msg): pass
    def chooseTile(self, actions): return random.choice(actions)
    def chooseNewCompany(self, actions): return random.choice(actions)
    def chooseSurvivor(self, actions): return random.choice(actions)
    def chooseLiquidate(self, actions): return random.choice(actions)
    def chooseStock(self, actions): return random.choice(actions)
    def chooseEndGame(self, actions): return "Yes"

    def quit(self):
        """ Method to handle the reciept of a quit request """
#       if self.name == "Min1":
#           print(self.state)
        QCoreApplication.quit()
        sys.exit()

if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--serverPort', type = int)
    parser.add_argument('-n', '--playerName', type = str)
    args = parser.parse_args()
    a = RandomClient(name = args.playerName, serverPort = args.serverPort)
    app.exec_()

