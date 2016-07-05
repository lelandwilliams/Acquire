from playerbox import PlayerBox
from PyQt5.QtWidgets import QFrame, QVBoxLayout

class PlayerBoxGroup(QFrame):
    def __init__(self):
        super().__init__()

        self.boxLayout = QVBoxLayout()
        self.setLayout(self.boxLayout)
        self.players = {}
        self.setMaximumHeight(400)

    def addPlayer(self, name, money):
        new_player = PlayerBox()
        new_player.setName(name)
        new_player.setMoney(money)
        self.players[name] = new_player
        self.boxLayout.addWidget(new_player)

    def test(self):
        self.addPlayer("Bender",20000)
        self.addPlayer("Hal", 1500)
        self.addPlayer("C3P0", 500)
        self.addPlayer("R2D2", 19000)

    def updatePlayerMoney(self, player):
        players[player.name].setMoney(player.money)
