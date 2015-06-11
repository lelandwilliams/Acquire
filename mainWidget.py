import sys
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QMainWindow, QFrame, QApplication, QDockWidget
from PyQt5.QtCore import Qt
from playerboxgroup import PlayerBoxGroup
from board import Board
from stockchooserdialog import StockChooserDialog
from playerDialogBox import PlayerDialogBox

class AcquireUI(QMainWindow):
#class AcquireUI(QFrame):
    def __init__(self):
        super().__init__()
        self.frame = QFrame()
        self.lt = QGridLayout()
        self.board = Board()
        self.pb = PlayerBoxGroup()
        self.board.show()
        self.pb.show()
        self.pb.test()
        self.lt.addWidget(self.board, 0,0, 1,5)
        self.lt.addWidget(self.pb,0,6,1,2)
        self.lt.setAlignment(Qt.AlignTop)
        self.frame.setLayout(self.lt)


        self.setCentralWidget(self.frame)

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

def stockChooserTest():
    app = QApplication(sys.argv)
    a = AcquireUI()
    ex = StockChooserDialog(['Tower', "Luxor", "American", "Worldwide"], a.setColors())
    ex.show()
    sys.exit(app.exec_())

def test():
    app = QApplication(sys.argv)
    a = AcquireUI()
    a.show()
    sys.exit(app.exec_())

def dialogTest():
    app = QApplication(sys.argv)
    a = AcquireUI()
    ex = PlayerDialogBox()
    ex.show()
    tile = ex.chooseTile(["1-A","7-D","11-F"])
    print(" **** %s ****" %(tile))
    stock = ex.chooseStock(['Tower', "Luxor", "American", "Worldwide"], a.setColors())
    print(" **** %s ****" %(stock))
    sys.exit(app.exec_())
