from randomClient import RandomClient
from concierge import Concierge
import logging


class HumanClient(RandomClient):
    """ An extension of RandomClient to control a GUI """
    def __init__(self):
        super().__init__(client_type = 'HUMAN', name = 'PunyHuman')
        self.Concierge = None
        LOG_FORMAT = '%(levelname)s:%(module)s:%(message)s'
        logging.basicConfig(level = logging.INFO, format = LOG_FORMAT)

    def announceBegin(self, players):
        """ Overrides base class

        """
        self.addPlayers(players)

    def announcePlay(self, play, action_type):
        """ Updates the UI after a play.


        """

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
        elif action_type == 'Found':
            self.changeGroupColor(play)
        elif action_type == 'Choose Survivor':
            pass
        elif action_type == 'Liquidate':
            pass
        elif action_type == 'Buy':
            pass
        elif action_type == 'Call':
            pass
        else:
            logging.error("action_type {} not handled".format(action_type))

    def newGame(self):
        """ Begin a new game

        Begins by starting a new Concierge. 
        When the the Concierge finds an available server,
        the method self.connectToServer() will be called.

        TODO:
            [ ] Connect to a remote concierge.
        """
        if self.Concierge is None:
            self.Concierge = Concierge()
            self.Concierge.process_list.append(["python", "randomClient.py", "-n", "Random1"])
            self.Concierge.process_list.append(["python", "randomClient.py", "-n", "Random2"])
            self.Concierge.process_list.append(["python", "randomClient.py", "-n", "Random3"])
        self.Concierge.serverAvailable.connect(self.serverAvailable)
        self.Concierge.runGames()

    def chooseNewCompany(self, actions):
        """ Handles the action to choose which new corporation to found.
        """
        return self.chooseNewCorp(actions)

    def serverAvailable(self, port):
        self.serverPort = port
        self.Concierge.serverAvailable.disconnect(self.serverAvailable)
        self.connectToServer(port = self.serverPort)
