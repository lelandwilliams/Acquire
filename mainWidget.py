import sys
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QMainWindow, QFrame, QApplication, QDockWidget, QAction, qApp
from PyQt5.QtCore import Qt
from playerboxgroup import PlayerBoxGroup
from board import Board
from playerDialogBox import PlayerDialogBox

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

        self.fileMenu = self.menuBar().addMenu("&File")
        self.exitAction = QAction("E&xit",self)
        self.fileMenu.addAction(self.exitAction)
        self.exitAction.triggered.connect(qApp.quit)

        self.setWindowTitle('Acquire')

    def changeTileColor(self, tile, company):
        self.board.changeTileColor(tile,company)

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

    def test(self):
        self.pb.test()
        tile = self.dialogbox.chooseTile(["1-A","7-D","11-F"])
        self.board.changeTileColor(tile,'None')

def test():
        app = QApplication(sys.argv)
        a = AcquireUI()
        a.show()
        a.test()
        sys.exit(app.exec_())

def dialogTest():
    app = QApplication(sys.argv)
    a = AcquireUI()
    print(" **** %s ****" %(tile))
    stock = ex.chooseStock(['Tower', "Luxor", "American", "Worldwide"], a.setColors())
    print(" **** %s ****" %(stock))
    sys.exit(app.exec_())
