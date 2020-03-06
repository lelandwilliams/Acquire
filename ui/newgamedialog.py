import sys
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout,\
QLineEdit, QButtonGroup, QGridLayout, QRadioButton, QFileDialog, QPushButton,\
QToolButton, QLabel
from PyQt5.QtGui import QIcon, QIntValidator
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from robotNames import names as robotnames
from random import choice
from exampleMaker import statsBuilder, Bots

playerTypes = ['Human']
for b in Bots:
    playerTypes.append(b[:-3])

class NewGameDialog(QFrame):
    """ Provides a dialog to start a new game
    """
    def __init__(self, num_players = 2, standalone = True):
        super().__init__()
        self.num_players = num_players
        self.standalone = standalone
        self.logfile = ""
        self.num_rounds = 0

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

        if self.standalone:
            self.logfile = ""
            self.standalonelayout = QHBoxLayout()
            self.filedialogbutton = QToolButton()
            self.filedialogbutton.setIcon(QIcon.fromTheme('folder'))
            self.filedialogbutton.clicked.connect(self.chooseFile)
            self.saLabel = QLabel("Log File:")
            self.saLabel2 = QLabel("Num Games:")
            self.saEditBar = QLineEdit(self.logfile)
            self.numBox = QLineEdit("10")
            self.validator = QIntValidator(1,100)
            self.numBox.setValidator(self.validator)

            self.standalonelayout.addWidget(self.saLabel)
            self.standalonelayout.addWidget(self.saEditBar)
            self.standalonelayout.addWidget(self.filedialogbutton)
            self.standalonelayout.addWidget(self.saLabel2)
            self.standalonelayout.addWidget(self.numBox)

            self.buttonRow = QHBoxLayout()
            self.startButton = QPushButton('Start')
            self.quitButton = QPushButton('Quit')
            self.buttonRow.addWidget(self.startButton)
            self.buttonRow.addWidget(self.quitButton)
            self.quitButton.clicked.connect(self.close)
            self.startButton.clicked.connect(self.makeExamples)

            self.leftLayout.addLayout(self.standalonelayout)
            self.leftLayout.addLayout(self.buttonRow)


        self.setLayout(self.mainLayout)

    def addPlayer(self, name ='', player_type = 'robot'): 
        cur_names = [p.nameBox.text() for p in self.players]
        while name in cur_names or name == '':
            name = choice(robotnames)
        player = PlayerBox(name, player_type, self.standalone)
        self.playerLayout.addWidget(player)
        self.players.append(player)

    def chooseFile(self):
        """ initiates the use of QFileDialog and handles the results """
        self.filename = QFileDialog.getSaveFileName(options=(QFileDialog.DontConfirmOverwrite))
        print(self.filename)
        self.saEditBar.setText(self.filename[0])

    def makeExamples(self):
        game_runner = statsBuilder()
        player_dict = dict()
        for p in self.players:
            p_name = p.nameBox.text()
            selected = p.typeGroup.checkedButton().text()
            player_dict[p_name] = selected + ".py"
        game_runner.players = player_dict



class PlayerBox(QFrame):
    """ Proveds a Horizontal widget to specify player information when starting a game.
    Parameters:
    -----------
        name(str): the specified name for the player.
        player_type(str): the default player type for this player
        standalong(bool): if the dialog is standalone, then all the clients should be bots
    """
    spacer_width = 0
    def __init__(self, name = "", player_type = 'human', standalone = False):
        super().__init__()

        self.layout = QHBoxLayout()
        self.typeGroup = QButtonGroup()
        self.button_layout = QGridLayout()

        self.nameBox = QLineEdit(name)
        self.nameBox.setReadOnly(True)

        # Add player type choices as radio buttons
        playerOptions = []
        if standalone:
            playerOptions = playerTypes[1:]
        else:
            playerOptions = playerTypes

        i = 0
        for pt in playerOptions:
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

