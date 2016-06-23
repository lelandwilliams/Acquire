import sys, string
from PyQt5.QtWidgets import QLabel, QFrame, QGridLayout
#from PyQt5.QtCore import Qt, QCoreApplication

class Board(QFrame):
    def __init__(self,colors):
        super().__init__()

        self.setLineWidth(1)
        self.setFrameShape(QFrame.Box)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.tiles = {}
        self.companycolors = colors

        self.tile_size = 40

        for i in string.ascii_uppercase[:9]:
            for j in range(1,13):
                text = str(j) + '-' + i
                space = QLabel(text,self)
                self.tiles[text] = space
                space.setFrameShape(QFrame.Panel)
                space.setFrameShadow(QFrame.Sunken)
            
                self.grid.addWidget(space, ord(i) - ord('A'), j - 1 )
                space.setFixedSize(self.tile_size, self.tile_size)

#        self.setMaximumSize(self.frameWidth(), self.frameWidth())

    def changeTileColor(self,tile, company):
        tilestr = str(tile[0])+"-"+tile[1]
        item = self.tiles[tilestr]
        color = self.companycolors[company]
        item.setStyleSheet("QLabel {background-color: " + color + "; color: white;}")
        item.setFrameShadow(QFrame.Raised)

