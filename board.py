import sys, string
from PyQt5.QtWidgets import QLabel, QFrame, QGridLayout, QApplication
from PyQt5.QtCore import Qt, QCoreApplication

class Board(QFrame):
    def __init__(self):
        super().__init__()

        self.setLineWidth(1)
        self.setFrameShape(QFrame.Box)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.tiles = {}
        self.companycolors = self.setColors()
#       self.setAlignment(Qt.AlignTop)

        self.tile_size = 40

        for i in string.ascii_uppercase[:9]:
            for j in range(1,13):
                text = str(j) + '-' + i
                space = QLabel(text,self)
                self.tiles[text] = space
#               space.setAlignment(Qt.AlignCenter)
                space.setFrameShape(QFrame.Panel)
                space.setFrameShadow(QFrame.Sunken)
            
                self.grid.addWidget(space, ord(i) - ord('A'), j - 1 )
                space.setFixedSize(self.tile_size, self.tile_size)

#        self.setMaximumSize(self.frameWidth(), self.frameWidth())

    def changeTileColor(self,tile, company):
        item = self.tiles[tile]
        color = self.companycolors[company]
        item.setStyleSheet("QLabel {background-color: " + color + "; color: white;}")
        item.setFrameShadow(QFrame.Raised)

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
