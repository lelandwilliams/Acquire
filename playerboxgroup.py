from playerbox import PlayerBox
from PyQt5.QtWidgets import QFrame, QVBoxLayout

class PlayerBoxGroup(QFrame):
    def __init__(self, colors):
        super().__init__()

        self.boxLayout = QVBoxLayout()
        self.setLayout(self.boxLayout)
        self.players = {}
        self.setMaximumHeight(400)
        self.colors = colors

    def addPlayer(self, name, money):
        new_player = PlayerBox(colors)
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

    def updatePlayerMoney(self, player):
        self.players[player.name].setMoney(player.money)

    def updatePlayerStock(self, player):
        self.players[player.name].setStock(player.stock)
