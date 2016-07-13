from PyQt5.QtWidgets import QHBoxLayout,QDialog,QPushButton
from PyQt5.QtCore import QObject, pyqtSignal

class TileChooserDialog(QDialog):
    chosen = pyqtSignal(str)
    def __init__(self, tileList):
        super().__init__()
        self.tile_list = tileList

        self.tile_size = 40

        l = QHBoxLayout()
        for tile in tileList:
            newTile = QPushButton(str(tile[0])+"-"+tile[1])
            newTile.setStyleSheet("QPushButton {background-color: black;"
                        "color: white;"
                        "border: 2px outset white;}"
                        "QPushButton:hover {border-color: white;"
                        "border: 4px ridge red;}")
            newTile.clicked.connect(self.buttonClicked)
            newTile.setFixedSize(self.tile_size, self.tile_size)
            l.addWidget(newTile)
        self.setLayout(l)

    def buttonClicked(self):
        sender = self.sender()
        print(sender.text())
        txt = sender.text()
        num = 0
        if len(txt) ==4:
            num = 10 + int(txt[1])
        else:
            num = int(txt[0])
        tile = (num,txt[-1])
        self.done(self.tile_list.index(tile))



