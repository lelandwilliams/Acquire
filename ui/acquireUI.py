import sys, os, inspect, logging
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QMainWindow, QFrame, QApplication, QDockWidget, QAction, \
        qApp, QDialog, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from playerboxgroup import PlayerBoxGroup
from board import Board
from playerDialogBox import PlayerDialogBox
import model
from concierge import Concierge
from humanClient import HumanClient
from newgamedialog import NewGameDialog

class AcquireUI(QMainWindow, HumanClient):
    """
        Todo:
            [ ] clean up cruft in chooseTile()
    """
    def __init__(self):
        super().__init__()
        self.game_in_progress = False

        self.frame = QFrame()
#       self.frame.setMinimumSize(270,360)
        self.lt = QGridLayout()
        self.board = Board(self.setColors())
        self.pb = PlayerBoxGroup(self.setColors())
        self.dialogbox = PlayerDialogBox()
        self.board.show()
        self.pb.show()
        self.lt.addWidget(self.board, 0,0, 1,5)
        self.lt.addWidget(self.pb,0,6,1,2)
        self.lt.addWidget(self.dialogbox,1,0,1,5)
        self.lt.setAlignment(Qt.AlignTop)
        self.frame.setLayout(self.lt)

        self.setCentralWidget(self.frame)

        self.fileMenu = self.menuBar().addMenu("&Game")
        self.startAction = (QAction("&New", self))
        self.fileMenu.addAction(self.startAction)
        self.startAction.triggered.connect(self.startNewGame)
        self.exitAction = QAction("E&xit",self)
        self.fileMenu.addAction(self.exitAction)
        self.exitAction.triggered.connect(qApp.quit)

        self.setWindowTitle('Acquire')
        self.debug = True
        self.gui = True
        self.stockChoiceNum = 1

        self.concierge = None
        self.ui_time = 150

    def addPlayers(self, players):
        """ Adds a player box for each player to the playerBoxGroup


        Parameters:
            players: a python list of the names of the players

        """
        for player in players:
            money = self.state['Players'][player]['money']
            self.pb.addPlayer(player, money)

#   def announceBegin(self):
#       if self.use_timers:
#           QTimer.singleShot(self.ui_time, self.de_enqueueTextMessage)

    def announceGameOver(self, name):
        for player in self.state['Players']:
            if player == "Bank":
                continue
            self.pb.updatePlayerMoney(player, model.netWorth(player, self.state))
        #self.dialogbox.announceGameOver(name)
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Game Over")
        msgBox.setText("{} ended the game".format(name))
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    def changeTileColor(self, tile, company):
        self.board.changeTileColor(tile,company)

    def changeGroupColor(self, corp):
        for member in self.state['Group'][corp]:
            self.changeTileColor(member, corp)
    
    def chooseNewCorp(self, choices): 
        companies = dict()
        for corp in choices:
            companies[corp] = model.stockPrice(self.state, corp)
        choice = self.dialogbox.chooseStock(-1, companies, self.setColors())
        self.stockChoiceNum = 1
        if self.use_timers:
            QTimer.singleShot(self.ui_time, self.de_enqueueTextMessage)
        return choice

    def chooseGameOver(self):
        choice = self.dialogbox.chooseGameOver(self.game.getCurrentPlayer().name) == "End"
        if self.use_timers:
            QTimer.singleShot(self.ui_time, self.de_enqueueTextMessage)
        return choice

    def chooseMerger(self, corps):
        companyList = {}
        for corp in corps:
            companyList[corp] = ""
        choice =  self.dialogbox.chooseMerger(companyList, self.setColors())
        if self.use_timers:
            QTimer.singleShot(self.ui_time, self.de_enqueueTextMessage)
        return choice

    def chooseMergerStockAction(self, corp, largestCorp, actions):
        activePlayer = self.state['Turn']['Player']
        choice =  self.dialogbox.chooseMergerStockAction(self.name, activePlayer, corp,largestCorp, actions, self.setColors())
        if self.use_timers:
            QTimer.singleShot(self.ui_time, self.de_enqueueTextMessage)
        return choice

    def chooseStock(self,corps):
        corps.remove('Done')
        if len(corps) == 0:
            if self.use_timers:
                QTimer.singleShot(self.ui_time, self.de_enqueueTextMessage)
            return 'Done'
        if self.stockChoiceNum == 3:
            self.stockChoiceNum = 1

        companies = dict()
        for corp in corps:
            companies[corp] = model.stockPrice(self.state, corp)
        choice =  self.dialogbox.chooseStock(self.stockChoiceNum, companies, self.setColors())
        self.stockChoiceNum += 1
        if self.use_timers:
            QTimer.singleShot(self.ui_time, self.de_enqueueTextMessage)
        return choice

    def chooseTile(self, hand):
        tile = self.dialogbox.chooseTile(hand)
        logging.info("Player chose " + str(tile))
        if self.use_timers:
            QTimer.singleShot(self.ui_time, self.de_enqueueTextMessage)
        return tile

    def setColors(self): 
        colorscheme = {}
#       colorscheme['None'] = "rgb(32,32,32)"
        colorscheme['None'] = "rgb(46,45,50)"
#       colorscheme['Tower'] = "rgb(246,214,86)"
        colorscheme['Tower'] = "rgb(215,155,23)"
#       colorscheme['Luxor'] = "rgb(246,153,153)"
        colorscheme['Luxor'] = "rgb(255,81,57)"
#       colorscheme['Worldwide'] = "rgb(155,98,41)"
        colorscheme['Worldwide'] = "rgb(145,72,45)"
#       colorscheme['Festival'] = "rgb(5,119,51)"
        colorscheme['Festival'] = "rgb(32,132,86)"
#       colorscheme['American'] = "rgb(0,0,102)"
        colorscheme['American'] = "rgb(29,75,102)"
#       colorscheme['Imperial'] = "rgb(242,82,42)"
        colorscheme['Imperial'] = "rgb(238,98,137)"
#       colorscheme['Continental'] = "rgb(0,128,255)"
        colorscheme['Continental'] = "rgb(42,157,150)"
        colorscheme['ActivePlayerBackground'] = "rgb(250,250,250)"
        colorscheme['PlayerBackground'] = "rgb(230,230,230)"
        colorscheme['Board'] = "rgb(228,202,127)"
        return colorscheme

    def setPlayers(self):
        """ DEPRECATED: gives a way to create default players
        """
        players = []
        players.append(acquire_model.Player('Bender', 'Robot'))
        players.append(acquire_model.Player('C3P0', 'Robot'))
        players.append(acquire_model.Player('Hal 9000', 'Robot'))
        players.append(acquire_model.Player('Puny Human', 'Human'))

        return players

    def startNewGame(self):
        dialog = NewGameDialog(parent=self, num_players=4)
        dialog.exec()
        if dialog.result() == QDialog.Rejected:
            return
        player_dict = dialog.getPlayers()
        if self.concierge is None:
            self.concierge = Concierge()
        if dialog.seedCheckBox.isChecked():
            self.game_seed = int(dialog.numBox.text())
        else:
            self.game_seed = 0

        self.concierge.process_list.clear()
        for name, executable in player_dict.items():
            if "Human" not in executable:
                self.concierge.process_list.append(["python", executable, "-n", name])
        self.concierge.serverAvailable.connect(self.serverAvailable)
        self.concierge.runGames()



    def test(self):
        self.pb.test()
        tile = self.dialogbox.chooseTile(["1-A","7-D","11-F"])
        self.board.changeTileColor(tile,'None')

def play():
        app = QApplication(sys.argv)
        a = AcquireUI()
        a.show()
        #a.test()
        sys.exit(app.exec_())

def dialogTest():
    app = QApplication(sys.argv)
    a = AcquireUI()
    print(" **** %s ****" %(tile))
    stock = ex.chooseStock(['Tower', "Luxor", "American", "Worldwide"], a.setColors())
    print(" **** %s ****" %(stock))
    sys.exit(app.exec_())

if __name__ == "__main__":
    play()
