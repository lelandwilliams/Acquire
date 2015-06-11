from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QApplication
from PyQt5.QtCore import pyqtSlot, QObject
from stockchooserdialog import StockChooserDialog
from tilechooserdialog import TileChooserDialog
import sys

class PlayerDialogBox(QFrame,QObject):
    def __init__(self):
        super().__init__()
        self.label1 = QLabel()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label1)

        self.setLayout(self.layout)

    def chooseStock(self,companies,colors):
        self.dialog = StockChooserDialog(companies,colors)
        self.label1.setText("Choose your Stock")
        self.layout.addWidget(self.dialog)
        stock =  companies[self.dialog.exec()]
        print(stock)
        self.label1.setText("You Chose " + stock)
        return stock

    def chooseTile(self, tiles):
        self.dialog = TileChooserDialog(tiles)
        self.label1.setText("Choose your Tile")
        self.layout.addWidget(self.dialog)
        tile =  tiles[self.dialog.exec()]
        self.label1.setText("You Chose " + tile)
        return tile

