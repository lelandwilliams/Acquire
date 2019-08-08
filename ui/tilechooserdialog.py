from PyQt5.QtWidgets import QHBoxLayout,QDialog,QPushButton
from PyQt5.QtCore import QObject, pyqtSignal
import logging

class TileChooserDialog(QDialog):
    chosen = pyqtSignal(str)
    def __init__(self, tileList):
        super().__init__()
        self.tile_list = tileList
        logging.debug(tileList)

        self.tile_size = 40

        l = QHBoxLayout()
        l.addStretch()
        for tile in tileList:
            tile_text = str(tile[0]) + '-' + tile[1]
            logging.debug(tile_text)
            newTile = QPushButton(tile_text)
            newTile.setStyleSheet("QPushButton {background-color: black;"
                        "color: white;"
                        "border: 2px outset white;}"
                        "QPushButton:hover {border-color: white;"
                        "border: 4px ridge red;}")
            newTile.clicked.connect(self.buttonClicked)
            newTile.setFixedSize(self.tile_size, self.tile_size)
            l.addWidget(newTile)
        l.addStretch()
        self.setLayout(l)

    def buttonClicked(self):
        sender = self.sender()
        logging.debug(sender.text())
        txt = ''.join(sender.text().split('&'))
        logging.debug(txt)
#       num = 0
#        if len(txt) ==4:
#            num = 10 + int(txt[1])
#        else:
#            num = int(txt[0])
#       tile = (num,txt[-1])
        txt = txt.split('-')
        logging.debug(txt)
        tile = (int(txt[0]),txt[1])
        logging.debug(tile)
        self.done(self.tile_list.index(tile))



