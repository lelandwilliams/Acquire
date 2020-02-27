import sys
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout,\
QLineEdit, QButtonGroup, QGridLayout, QRadioButton, QFileDialog
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from robotNames import names as robotnames
from random import choice

playerTypes = ['Human', 'RandomAI']

class NewGameDialog(QFrame):
    """ Provides the contents of the dialog box.
    """
    def __init__(self, num_players = 2, standalone = True):
        super().__init__()
        self.num_players = num_players
        self.standalone = standalone

        self.players = list()
        self.playerLayout = QVBoxLayout()
        if not standalone:
            self.addPlayer(player_type='human')
        while len(self.players) < self.num_players:
            self.addPlayer(player_type='robot')

        self.mainLayout = QHBoxLayout()
        self.leftLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.leftLayout)
        self.leftLayout.addLayout(self.playerLayout)

        self.setLayout(self.mainLayout)

    def addPlayer(self, name ='', player_type = 'robot'): 
        cur_names = [p.nameBox.text() for p in self.players]
        while name in cur_names or name == '':
            name = choice(robotnames)
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
    a = NewGameDialog(num_players = 4, standalone=True)
    a.show()
    sys.exit(app.exec_())

