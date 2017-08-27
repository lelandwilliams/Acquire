from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QFrame, QLabel
from acquire_model import Acquire

class PlayerBox(QFrame):
    def __init__(self):
        """ The nameFrameLayout holds the player name, and current cash holding
            The lastPlayFrameLayout remembers the player's last move, and which stocks they hold
        """
        super().__init__()

        self.layout = QVBoxLayout()
        self.nameFrame = QFrame()
        self.lastPlayFrame = QFrame()
        self.nameFrameLayout = QHBoxLayout()

        self.lastPlayFrameLayout = QHBoxLayout()
        self.stockFrameLayout = QHBoxLayout()

        self.nameLabel = QLabel()
        self.moneyLabel = QLabel()
        self.nameFrameLayout.addWidget(self.nameLabel)
        self.nameFrameLayout.addStretch()
        self.nameFrameLayout.addWidget(self.moneyLabel)
        self.nameFrame.setLayout(self.nameFrameLayout)

        self.lastPlayLabel = QLabel()
        self.lastPlayFrameLayout.addWidget(self.lastPlayLabel)
        self.corporationLabel = dict()
        self.lastPlayFrameLayout.addLayout(self.stockFrameLayout)
        for corp in Acquire.corpNames:
            self.corporationLabel[corp] = QLabel()
            self.corporationLabel[corp].hide()
            self.lastPlayFrameLayout.addWidget(self.corporationLabel[corp])

        self.setLayout(self.layout)
        self.layout.addWidget(self.nameFrame)
        self.layout.addWidget(self.lastPlayFrame)

        self.setLineWidth(1)
        self.setFrameStyle(QFrame.Panel)

    def setBackground(self, color):
        self.setStyleSheet("QFrame {background-color:" + color +"}")

    def setName(self, name):
        self.nameLabel.setText(name)

    def setMoney(self, money):
        self.moneyLabel.setText( "$ " + str(money))

    def test(self):
        self.setName("Jimmy")
        self.setMoney(20000)
        

