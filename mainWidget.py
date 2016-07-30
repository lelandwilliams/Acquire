import sys
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QMainWindow, QFrame, QApplication, QDockWidget, QAction, qApp
from PyQt5.QtCore import Qt
from playerboxgroup import PlayerBoxGroup
from board import Board
from playerDialogBox import PlayerDialogBox
from controller import Controller
import acquire 

class AcquireUI(QMainWindow, Controller):
    def __init__(self):
        super().__init__()
        self.frame = QFrame()
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
        self.startAction.triggered.connect(self.newGame)
        self.exitAction = QAction("E&xit",self)
        self.fileMenu.addAction(self.exitAction)
        self.exitAction.triggered.connect(qApp.quit)

        self.setWindowTitle('Acquire')
        self.debug = True
        self.gui = True

    def addPlayers(self, players):
        for player in players:
            self.pb.addPlayer(player.name, player.money)

    def changeTileColor(self, tile, company):
        self.board.changeTileColor(tile,company)

    def changeGroupColor(self, corp):
        idx = self.game.corporations[corp].groupIndex
        for member in self.game.tilegroups[idx]:
            self.changeTileColor(member, corp)
    
    def chooseNewCorp(self,available): 
        return self.dialogbox.chooseCorporation(available, self.setColors())

    def chooseGameOver(self):
        return self.dialogbox.chooseGameOver(self.game.getCurrentPlayer().playerName) == "End"

    def chooseMerger(self, corps):
        companyList = {}
        for corp in corps:
            companyList[corp] = ""
        return self.dialogbox.chooseMerger(companyList, self.setColors())

    def chooseMergerStockAction(self, player, corp, largestCorp, actions):
        return self.dialogbox.chooseMergerStockAction(player,self.game.getCurrentPlayer(), corp,largestCorp, actions, self.setColors())

    def chooseStock(self,corps,number):
        return self.dialogbox.chooseStock(number, corps, self.setColors())

    def chooseTile(self,player):
        tile = None
        while True:
            if(player.playerType == 'Human'):
                tile = self.dialogbox.chooseTile(player.hand, player)
            else:
                tile = self.game.aiChooseTile(player)
            if self.game.evaluatePlay(tile) != "Illegal":
                if self.debug:
                    print(player.name, "chose", tile, self.game.evaluatePlay(tile))
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
        players = []
        players.append(acquire.Player('Bender', 'Robot'))
        players.append(acquire.Player('C3P0', 'Robot'))
        players.append(acquire.Player('Hal 9000', 'Robot'))
        players.append(acquire.Player('Puny Human', 'Human'))

        return players

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

play()
