from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QApplication
from PyQt5.QtCore import pyqtSlot, QObject, Qt
from stockchooserdialog import StockChooserDialog
from tilechooserdialog import TileChooserDialog
from mergeractionchooserdialog import MergerActionDialog
import sys

class PlayerDialogBox(QFrame,QObject):
    def __init__(self):
        super().__init__()
        self.label1 = QLabel()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label1)

        self.setLayout(self.layout)
    
    def announceGameOver(self, name):
        self.dialog = MergerActionDialog(["Continue"])
        text = "<h1> The Game Has Been Called </h1>"
        text += "Player " + name + " has declared the game over"
        text += "<p>Now we will liquidate all the corporations</p>"
        self.label1.setText(text)
        self.layout.addWidget(self.dialog)
        self.dialog.exec()

    def chooseGameOver(self,player):
        actions = ["End Game","Continue"]
        self.dialog = MergerActionDialog(actions)
        text = "<h1>End the Game ?</h1>"
        text += "<p><b>"+ player  + "</b>:"
        text += " you may choose to end the game, or to have it continue<br>"
        text += "The game may end becuase either all corporations on the board<br>"
        text += "Are size 7 or at least one corporation is size 41</p>"
        self.label1.setText(text)
        self.layout.addWidget(self.dialog)
        return actions[self.dialog.exec()]

    def chooseMerger(self, corps, colors):
        self.dialog = StockChooserDialog(corps,colors)
        text = "<h1> Liquidate a Company</h1>"
        text+= "<p>The tile you placed connected two or more corporations.</p>"
        text += "<p>Usually the smallest corporation is absorbed into the larger<br>"
        text += "but in this case there were two equal sized corporations</p>"
        text += "<p>now you choose which of the corporations will be absorbed</p>"
        self.label1.setText(text)
        self.layout.addWidget(self.dialog)
        corp = list(corps)[self.dialog.exec()]
        return corp

    def chooseMergerStockAction(self,player,activePlayer, corp,largestCorp, actions, colors):
        text = "<h1>Choose how to Liquidate Stock</h1>"
        if player.name == activePlayer.name:
            text += "<p>" + "You"
        else:
            text += "<p>" + activePlayer.name
        text += " played a tile that caused " + corp + " to be merged into <br>"
        text += largestCorp +".<p>"
        text += "<p> Now you must choose what to do with your remaining stock in"
        text += corp + "</p>"
        text += "<p> Depending on share availibilty, you may:"
        text += "<li> Trade in two shares of " + corp + "for one share of " + largestCorp
        text += "<li> Sell a shares to the bank"
        text += "<li> Hold on to your shares hoping for the re-establishment of the corporation</p>"
        self.dialog = MergerActionDialog(actions, colors)
        self.label1.setText(text)
        self.layout.addWidget(self.dialog)
        return actions[self.dialog.exec()]


    def chooseStock(self,number,companies,colors):
        text = ""
        if  number == -1 :
            text = "<h1>Found a New Corporation</h1>"
            text += "<p>You played a tile that joins one or more single tiles together<br>"
            text += "so you must choose which new corporation to form<br>"
            text += "You will recieve one free share of stock in the new corporation</p>"
        else:
            text = "<h1>Purchase Stock</h1>"
            text += "<p>At this point in your turn you can purchase up to<br>"
            text += "three shares of stock in active companies</p>"

        self.dialog = StockChooserDialog(companies,colors)
        if number == 1:
            self.label1.setText(text +"Choose your <b>first</b> stock")
        elif number == 2:
            self.label1.setText(text +"Choose your <b>second</b> stock")
        elif number == 3:
            self.label1.setText(text +"Choose your <b>third</b> stock")
        elif number == -1:
            self.label1.setText(text +"Choose which company to found")
        self.layout.addWidget(self.dialog)
        stock =  list(companies)[self.dialog.exec()]
        print(stock)
        self.label1.setText("You Chose " + stock)
        return stock

    def chooseTile(self, tiles):
        label = "<h1><font color=\"blue\"></font> Choose a Tile</h1>\n"
        label += "<p> It's now your turn.</p>" 
        label += "<p> Choose one of your tiles to place on the board.</p> "
        label += "<li> Tiles that played next to (a) solitary tile(s) <br>"
        label += "will form a new corporation</li>"
        label += "<li> Tiles that are adjacent to (colored) corporation tiles <br>"
        label += "will increase the size of the corporation and (often) its value.</li>"
        label += "<li> Tiles that connect two corporations will cause a merger. </li>"
        label += "<p><small>(Tiles that connect two companies that are both size 11<br>"
        label += "or that would found a new company when there are already 7 companies<br>"
        label += "on the board are <b>illegal</b> plays and will be ignored"
        label += "</small></p>"
        self.dialog = TileChooserDialog(tiles)
        self.label1.setText(label)
        self.label1.setAlignment(Qt.AlignHCenter)
        self.layout.addWidget(self.dialog)
        tile =  tiles[self.dialog.exec()]
        self.label1.setText("You Chose " + str(tile))
        return tile

    def chooseCorporation(self, corps, colors):
        self.dialog = StockChooserDialog(corps,colors)
        text = "<h1>Found a New Corporation</h1>"
        text += "<p> The tile you placed joined with one or more tiles. </p>"
        text += "<p> This begins a new corporation </p>"
        text += "<p> You choose which corporation to form </p>"
        text += "<p> As a bonus, you get one share of stock in the new corporation </p>"
        self.label1.setText(text)
        self.layout.addWidget(self.dialog)
        corp =  list(corps)[self.dialog.exec()]
        print(corp)
#       self.label1.setText("You Chose " + stock)
        return corp
