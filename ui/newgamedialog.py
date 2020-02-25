import sys
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout,\
QLineEdit, QButtonGroup, QGridLayout, QRadioButton
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from robotNames import names

playerTypes = ['Human', 'RandomAI']

class Window(QFrame):
    """ Provides the contents of the dialog box.
    """
    def __init__(self):
        super().__init__()
        self.num_players = 4
        self.players = list()
        self.playerLayout = QVBoxLayout()
        self.addPlayer(player_type='human')
        for _ in range(self.num_players -1):
            self.addPlayer(player_type='robot')

        self.setLayout(self.playerLayout)

    def addPlayer(self, name ='Meat Bag', player_type = 'robot'): 
        player = PlayerBox(name, player_type)
        self.playerLayout.addWidget(player)
        self.players.append(player)


class PlayerBox(QFrame):
    """ Proveds a Horizontal widget to specify player information when starting a game.
    Parameters:
    -----------
        name(str): the specified name for the player.
        restricted_type(str): can be 'human' or 'robot' or ''.
    """
    spacer_width = 0
    def __init__(self, name = "", player_type = 'human'):
        super().__init__()

        self.layout = QHBoxLayout()
        self.typeGroup = QButtonGroup()
        self.button_layout = QGridLayout()

        self.nameBox = QLineEdit(name)
        self.nameBox.setReadOnly(True)

        # Add player type choices as radio buttons
        i = 0
        for pt in playerTypes:
            button = QRadioButton(pt)
            self.button_layout.addWidget(button, 0, i)
            self.typeGroup.addButton(button, id = i)
            i += 1
            if player_type == 'human' and pt == 'Human':
                button.toggle()
            if player_type != 'human' and pt != 'Human':
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

