from PyQt5.QtWidgets import QHBoxLayout,QFrame,QPushButton
from PyQt5.QtCore import QObject, pyqtSignal

class TileChooserDialog(QFrame,QObject):
    chosen = pyqtSignal(str)
    def __init__(self, tileList):
        super().__init__()

        self.tile_size = 40

        l = QHBoxLayout()
        for tile in tileList:
            newTile = QPushButton(tile)
            newTile.setStyleSheet("QPushButton {background-color: black;"
                        "color: white;"
                        "border-color: white;"
                        "border-style: outset;}")
            newTile.clicked.connect(self.buttonClicked)
            newTile.setFixedSize((3 * self.tile_size)//5, self.tile_size)
            l.addWidget(newTile)
        self.setLayout(l)

    def buttonClicked(self):
        sender = self.sender()
        print(sender.text())
        self.chosen.emit(sender.text())



