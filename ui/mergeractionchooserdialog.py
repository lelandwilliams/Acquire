from PyQt5.QtWidgets import QHBoxLayout,QDialog,QPushButton
from PyQt5.QtCore import QObject, pyqtSignal

class MergerActionDialog(QDialog):
    chosen = pyqtSignal(str)
    def __init__(self, actions, colors = None):
        super().__init__()

#        self.tile_size = 40
        self.actions = actions

        l = QHBoxLayout()
        l.addStretch()
#       l.addSpacing()
        for action in actions:
            newButton = QPushButton(action)
#            newStock.setStyleSheet("QPushButton {background-color: " + colors[company] + ";"
#                       "color: white;"
#                       "border-color: white;"
#                       "border-style: outset;}")
            newButton.clicked.connect(self.buttonClicked)
            newButton.setObjectName(action)
#            newStock.setFixedSize((3 * self.tile_size)//5, self.tile_size)
            l.addWidget(newButton)
            l.addStretch()
#        l.addSpacing()
        self.setLayout(l)

    def buttonClicked(self):
        sender = self.sender()
        print(sender.objectName())
        self.done(self.actions.index(sender.objectName()))



