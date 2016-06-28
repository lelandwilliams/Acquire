from PyQt5.QtWidgets import QHBoxLayout,QDialog,QPushButton
from PyQt5.QtCore import QObject, pyqtSignal

class StockChooserDialog(QDialog):
    chosen = pyqtSignal(str)
    def __init__(self, companyList, colors):
        super().__init__()
        self.company_list = companyList

        self.width = 100

        l = QHBoxLayout()
        for company in companyList:
            newStock = QPushButton(company)
            newStock.setStyleSheet("QPushButton {background-color: " + colors[company] + ";"
                        "color: white;"
                        "border-color: white;"
                        "border-style: outset;}")
            newStock.clicked.connect(self.buttonClicked)
            newStock.setObjectName(company)
            newStock.setFixedSize(self.width, int(1.5 *self.width))
            l.addWidget(newStock)
        self.setLayout(l)

    def buttonClicked(self):
        sender = self.sender()
        print(sender.objectName())
        self.done(self.company_list.index(sender.objectName()))



