from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QFrame, QLabel

class PlayerBox(QFrame):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.nameFrame = QFrame()
        self.lastPlayFrame = QFrame()
        self.nameFrameLayout = QHBoxLayout()
        self.lastPlayFrameLayout = QHBoxLayout()

        self.nameLabel = QLabel()
        self.moneyLabel = QLabel()
        self.nameFrameLayout.addWidget(self.nameLabel)
        self.nameFrameLayout.addStretch()
        self.nameFrameLayout.addWidget(self.moneyLabel)
        self.nameFrame.setLayout(self.nameFrameLayout)

#       self.lastPlayFrame.setMinimumHeight(60)

        self.setLayout(self.layout)
        self.layout.addWidget(self.nameFrame)
        self.layout.addWidget(self.lastPlayFrame)

        self.setLineWidth(1)
        self.setFrameStyle(QFrame.Panel)

    def setName(self, name):
        self.nameLabel.setText(name)

    def setMoney(self, money):
        self.moneyLabel.setText( "$ " + str(money))

    def test(self):
        self.setName("Jimmy")
        self.setMoney(20000)
        

