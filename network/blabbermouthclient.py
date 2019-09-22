import sys,random
from PyQt5.QtCore import QCoreApplication, QTimer
from client import AcquireClient

class BlabberMouthClient(AcquireClient):
    def __init__(self):
        super().__init__(self)
        self.messagelist = list()
        self.messagelist.append('I wet my arm pants')
        self.messagelist.append('My knob tastes funny')
        self.messagelist.append("Daddy, Im scared. Too scared to wet my pants.")
        self.messagelist.append("Principal Skinner, I got carsick in your office. ")

    def sendAMessage(self):
        if len(self.messagelist) > 0:
            m = random.choice(self.messagelist)
            self.messagelist.remove(m)
            self.socket.sendTextMessage(m)
            QTimer.singleShot(500, self.sendAMessage)
        return

if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    a = BlabberMouthClient()

    QTimer.singleShot(750, a.sendAMessage)
    QTimer.singleShot(9000, a.quit_app)
    app.exec_()


