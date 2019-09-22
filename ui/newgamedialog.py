import sys
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout, QLineEdit

class Window(QFrame):
    """ Provides the contents of the dialog box.
    """
    def __init__(self):
        super().__init__()
        self.num_players = 1
        self.players = list()
        self.playerLayout = QVBoxLayout()
        self.addPlayer(True)
        for _ in self.num_players -1:
            self.addPlayer(False)

        self.setLayout(self.playerBox)

    def addPlayer(human = False): 
        player = self.PlayerBox(human = human)
        self.playerLayout.addWidget(player)
        self.players.append(player)


class PlayerBox(QFrame):
    """ Proveds a Horizontal widget to define a player"""
    def __init__(self, name = None, human = True):
        super().__init__()
        self.layout = QHBoxLayout()
        if name is None:
            if human:
                self.name = "Puny Human"
            else:
                self.name = "Bender"
        else:
            self.name = name
        self.nameBox = QLineEdit(self.name)
        self.nameBox.setReadOnly(True)

        self.layout.addWidget(self.nameBox)
        self.setLayout(self.layout)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = PlayerBox()
    a.show()
    sys.exit(app.exec_())

