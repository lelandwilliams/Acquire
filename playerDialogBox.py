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

    def chooseStock(self,number,companies,colors):
        self.dialog = StockChooserDialog(companies,colors)
        if number == 1:
            self.label1.setText("Choose your first stock")
        elif number == 2:
            self.label1.setText("Choose your second stock")
        elif number == 3:
            self.label1.setText("Choose your third stock")
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
        self.label1.setText("You Chose " + str(tile))
        return tile

    def chooseCorporation(self, corps, colors):
        self.dialog = StockChooserDialog(corps,colors)
        self.label1.setText("You have founded a corporation. Which one ?")
        self.layout.addWidget(self.dialog)
        corp =  corps[self.dialog.exec()]
        print(corp)
#       self.label1.setText("You Chose " + stock)
        return corp
