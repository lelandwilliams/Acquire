from playerbox import PlayerBox
from PyQt5.QtWidgets import QFrame, QVBoxLayout
from model import corporations

class PlayerBoxGroup(QFrame):
    def __init__(self, colors):
        super().__init__()

        self.boxLayout = QVBoxLayout()
        self.setLayout(self.boxLayout)
        self.players = {}
        self.setMaximumHeight(400)
        self.colors = colors

    def addPlayer(self, name, money):
        new_player = PlayerBox(self.colors)
        new_player.setName(name)
        new_player.setMoney(money)
        self.players[name] = new_player
        self.boxLayout.addWidget(new_player)

    def endTurn(self, player):
        self.players[player.name].setColor(self.colors["PlayerBackground"])
        self.updatePlayerMoney(player)

    def setPlayerActive(self, player):
        self.players[player.name].setColor(self.colors["ActivePlayerBackground"])

    def test(self):
        self.addPlayer("Bender",20000)
        self.addPlayer("Hal", 1500)
        self.addPlayer("C3P0", 500)
        self.addPlayer("R2D2", 19000)

    def updateAllPlayers(self, state):
        for player in [p for p in state['Players'] if p != 'Bank']:
            self.updatePlayerMoney(player, state['Players'][player]['money'])
            corps = dict()
            for corp in corporations:
                corps[corp] = state['Players'][player][corp]
            self.updatePlayerStock(player, corps)

    def updatePlayerMoney(self, player, money):
        self.players[player].setMoney(money)

    def updatePlayerStock(self, player, stock):
        """ Changes a playerbox to show the player's current stock holdings

        Parameters:
        -----------
        player : str
             the name of the player whose info should not be updated
        stock : dict(str, int)
             a dictionary of (corporation_name, number_of_shares pairs)
        """
        self.players[player].setStock(stock)
