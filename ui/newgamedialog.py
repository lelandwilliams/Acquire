import sys
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout,\
QLineEdit, QButtonGroup, QGridLayout, QRadioButton

playerTypes = ['Human', 'Random']

class Window(QFrame):
    """ Provides the contents of the dialog box.
    """
    def __init__(self):
        super().__init__()
        self.num_players = 4
        self.players = list()
        self.playerLayout = QVBoxLayout()
        self.addPlayer(True)
        for _ in range(self.num_players -1):
            self.addPlayer(False)

        self.setLayout(self.playerLayout)

    def addPlayer(self, human = False): 
        player = PlayerBox(None, human)
        self.playerLayout.addWidget(player)
        self.players.append(player)


class PlayerBox(QFrame):
    """ Proveds a Horizontal widget to specify player information when starting a game.
    Parameters:
    -----------
        name(str): the specified name for the player.
        restricted_type(str): can be 'human' or 'robot' or ''.
    """
    def __init__(self, name = "", restricted_type = 'human'):
        super().__init__()
        self.layout = QHBoxLayout()
        if name == "" and restricted_type == 'human':
            self.name = "Puny Human"
        elif name == "" and restricted_type != 'human':
            self.name = "Bender"
        else:
            self.name = name
        self.typeGroup = QButtonGroup()
        self.button_layout = QGridLayout()

        self.nameBox = QLineEdit(self.name)
        self.nameBox.setReadOnly(True)

        i = 0
        for pt in playerTypes:
            button = QRadioButton(pt)
            self.button_layout.addWidget(button, 0, i)
            self.typeGroup.addButton(button, id = i)
            i += 1
            if restricted_type == 'human' and pt == 'Human':
                button.toggle()
            if not human and pt != 'Human':
                button.toggle()

        self.layout.addWidget(self.nameBox)
        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
#   a = PlayerBox()
    a = Window()
    a.show()
    sys.exit(app.exec_())

