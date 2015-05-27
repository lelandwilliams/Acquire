import sys
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QMainWindow, QFrame, QApplication, QDockWidget
from PyQt5.QtCore import Qt
from playerboxgroup import PlayerBoxGroup
from acquire_board import Board

#class AcquireUI(QMainWindow):
class AcquireUI(QFrame):
    def __init__(self):
        super().__init__()
        self.lt = QGridLayout()
        self.board = Board()
#       self.board.test()
        self.pb = PlayerBoxGroup()
        self.board.show()
        self.pb.show()
        self.pb.test()
#       self.pb.setMaximumHeight((self.board.height()))
        self.lt.addWidget(self.board, 0,0, 1,5)
#        self.lt.addStretch()
        self.lt.addWidget(self.pb,0,6,1,2)
        self.lt.setAlignment(Qt.AlignTop)
        self.setLayout(self.lt)
#        self.setMaximumHeight(500)


#        self.setCentralWidget(self.board)
#       self.playerDock = QDockWidget()
#       self.playerDock.setWidget(self.pb)
#       self.playerDock.setAllowedAreas(Qt.RightDockWidgetArea)

#       self.show()

def test():
    app = QApplication(sys.argv)
    ex = AcquireUI()
    ex.show()
    sys.exit(app.exec_())

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
