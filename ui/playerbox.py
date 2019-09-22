from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame, QLabel
#from acquire_model import Acquire
from PyQt5.QtCore import Qt

class PlayerBox(QFrame):
    def __init__(self, colors):
        """ The topFrame holds the player name, and current cash holding
            The bottomFrame remembers the player's last move, and which stocks they hold
        """
        super().__init__()

        self.colorPallet = colors
        self.stockWidth = 20
        self.stockHeight = 30

        self.topFrame = QFrame()
        self.bottomFrame = QFrame()
        self.stockFrame = QFrame()

        self.mainlayout = QVBoxLayout()
        self.setLayout(self.mainlayout)
        self.toplayout = QHBoxLayout()
        self.bottomlayout = QHBoxLayout()
        self.stockFrameLayout = QHBoxLayout()

        self.nameLabel = QLabel()
        self.moneyLabel = QLabel()
        self.toplayout.addWidget(self.nameLabel)
        self.toplayout.addStretch()
        self.toplayout.addWidget(self.moneyLabel)
        self.topFrame.setLayout(self.toplayout)
        self.mainlayout.addWidget(self.topFrame)

        self.lastPlayLabel = QLabel()
        self.bottomlayout.addWidget(self.lastPlayLabel)
        self.corporationLabel = dict()
        corpNames = ["Tower","Luxor","Worldwide","Festival","American", "Continental","Imperial"]
        for corp in corpNames:
            self.corporationLabel[corp] = QLabel()
            self.corporationLabel[corp].setText("")
#           self.stockFrameLayout.addWidget(self.corporationLabel[corp])
            self.bottomlayout.addWidget(self.corporationLabel[corp])
            color = self.colorPallet[corp]
            self.corporationLabel[corp].setStyleSheet("QLabel {background-color: " + color + "; color: white; }")
            self.corporationLabel[corp].setFixedWidth(12)
            self.corporationLabel[corp].setFixedHeight(20)
#           self.corporationLabel[corp].setFixedSize(20, 50) 
#           self.corporationLabel[corp].setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
#            self.corporationLabel[corp].setAlignment(Qt.AlignCenter)
            self.corporationLabel[corp].setScaledContents(True)
            self.corporationLabel[corp].hide()

        self.stockFrame.setLayout(self.stockFrameLayout)
        self.stockFrame.setMinimumHeight(10)
        self.bottomlayout.addWidget(self.stockFrame)
        self.bottomFrame.setLayout(self.bottomlayout)

        self.mainlayout.addWidget(self.topFrame)
        self.mainlayout.addWidget(self.bottomFrame)

        self.setLineWidth(1)
        self.setFrameStyle(QFrame.Panel)

    def setBackground(self, color):
        self.setStyleSheet("QFrame {background-color:" + color +"}")

    def setName(self, name):
        self.nameLabel.setText(name)

    def setMoney(self, money):
        self.moneyLabel.setText( "$ " + str(money))

    def setStock(self, stocks):
        for corp,numshares in stocks.items():
            self.corporationLabel[corp].setText(str(numshares))
            if numshares ==0:
                self.corporationLabel[corp].hide()
            else:
                self.corporationLabel[corp].show()

    def test(self):
        self.setName("Jimmy")
        self.setMoney(20000)
        

