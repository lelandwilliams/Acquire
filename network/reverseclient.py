import sys
from PyQt5.QtCore import QCoreApplication, QTimer
from client import AcquireClient

class ReverseClient(AcquireClient):
    def processTextMessage(self, message):
        print("ReverseClient recieved message: {}".format(message))
        new_message = list(message)
        new_message.reverse()
        new_message = ''.join(new_message)
        self.socket.sendTextMessage(new_message)

if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    a = ReverseClient()

    QTimer.singleShot(9000, a.quit_app)
    app.exec_()

