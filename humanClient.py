from randomClient import RandomClient
from concierge import Concierge


class HumanClient(RandomClient):
    """ An extension of RandomClient to control a GUI """
    def __init__(self):
        super().__init__(client_type = 'HUMAN', name = 'PunyHuman')
        self.Concierge = None

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
        self.Concierge.serverAvailable.connect(self.serverAvailable)
        self.Concierge.runGames()

    def serverAvailable(self, port):
        self.serverPort = port
        self.Concierge.serverAvailable.disconnect(self.serverAvailable)
        self.connectToServer(port = self.serverPort)
