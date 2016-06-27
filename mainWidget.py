import sys
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QMainWindow, QFrame, QApplication, QDockWidget, QAction, qApp
from PyQt5.QtCore import Qt
from playerboxgroup import PlayerBoxGroup
from board import Board
from playerDialogBox import PlayerDialogBox
import acquire 

class AcquireUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.frame = QFrame()
        self.lt = QGridLayout()
        self.board = Board(self.setColors())
        self.pb = PlayerBoxGroup()
        self.dialogbox = PlayerDialogBox()
        self.board.show()
        self.pb.show()
        self.lt.addWidget(self.board, 0,0, 1,5)
        self.lt.addWidget(self.pb,0,6,1,2)
        self.lt.addWidget(self.dialogbox,1,2,1,3)
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

    def addPlayers(self, players):
        for player in players:
            self.pb.addPlayer(player.name, player.money)

    def changeTileColor(self, tile, company):
        self.board.changeTileColor(tile,company)
    
    def chooseNewCorp(self,player,tile): 
        corp = None
        corps = self.game.inactiveCorps()
        if(player.playerType == 'Human'):
            corp = self.dialogbox.chooseCorp(corps)
        else:
            corp = self.game.aiChooseTile(corps)
        
        groups = self.game.adjoiningGroups(tile)
        if len(groups) > 1:
            print ("Group Error")
        self.game.tilegroups.append(tile)
        for member in groups[0]:
            self.changeTileColor(member, corp)

    def chooseTile(self,player):
        tile = None
        while True:
            if(player.playerType == 'Human'):
                tile = self.dialogbox.chooseTile(player.hand)
            else:
                tile = self.game.aiChooseTile(player)
            if self.game.evaluatePlay(tile) != "Illegal":
                if self.debug:
                    print(player.name, "chose", tile)
                return tile
         
    def newGame(self):
        players = self.setPlayers()
        self.game = acquire.Acquire(players)
        self.addPlayers(self.game.players)

        starters = self.game.setStarters()
        for tile in starters:
            self.changeTileColor(tile, 'None')
        self.game.fillHands()
        while(not self.game.gameOver()):
            player = self.game.getCurrentPlayer()
            if self.debug:
                print(str(player))
            tile = self.chooseTile(player)
            outcome = self.game.evaluatePlay(tile)
            if outcome == "Regular":
                self.game.placeTile(tile)
                self.changeTileColor(tile, 'None')
            elif outcome == "NewCorp":
                self.chooseNewCorp(player,tile)

            player.hand.remove(tile)
            player.hand.append(self.game.tiles.pop())
            player.hand.sort()
            self.game.advanceCurrentPlayer()



    def setColors(self): 
        colorscheme = {}
        colorscheme['None'] = "rgb(32,32,32)"
        colorscheme['Tower'] = "rgb(246,214,86)"
        colorscheme['Luxor'] = "rgb(246,153,153)"
        colorscheme['Worldwide'] = "rgb(155,98,41)"
        colorscheme['Festival'] = "rgb(5,119,51)"
        colorscheme['American'] = "rgb(0,0,102)"
        colorscheme['Imperial'] = "rgb(242,82,42)"
        colorscheme['Continental'] = "rgb(0,128,255)"

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
