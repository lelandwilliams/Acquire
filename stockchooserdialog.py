from PyQt5.QtWidgets import QHBoxLayout,QFrame,QPushButton
from PyQt5.QtCore import QObject, pyqtSignal

class StockChooserDialog(QFrame,QObject):
    chosen = pyqtSignal(str)
    def __init__(self, companyList, colors):
        super().__init__()

        self.tile_size = 40

        l = QHBoxLayout()
        for company in companyList:
            newStock = QPushButton()
            newStock.setStyleSheet("QPushButton {background-color: " + colors[company] + ";"
                        "color: white;"
                        "border-color: white;"
                        "border-style: outset;}")
            newStock.clicked.connect(self.buttonClicked)
            newStock.setFixedSize((3 * self.tile_size)//5, self.tile_size)
            newStock.setObjectName(company)
            l.addWidget(newStock)
        self.setLayout(l)

    def buttonClicked(self):
        sender = self.sender()
        print(sender.objectName())
        self.chosen.emit(sender.text())



