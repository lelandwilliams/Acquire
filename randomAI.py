from network import AcquireClient
from PyQt5.QtCore import QCoreApplication, pyqtSlot, QTimer
import sys, random

class randomAI(AcquireClient):
    def __init__(self, name, acquire_id = None):
        self.name = name
        super().__init__()
        self.outgoing_message_q.put("REGISTER;"+self.name)
#       self.outgoing_message_q.put("KILL;"+self.name)

    def process_private(self, player, parameter):
        print(name +": received a private message")

    def process_register(self, player):
        print(name +": received a registration message")
        QTimer.singleShot(250, self.main)

    def process_disconnect(self, player, parameter):
        print(name +": received a disconnect message")
        QCoreApplication.quit()

    def process_uuid(self, parameter):
        print(name +": received a UUID message")
        self.acquire_id = parameter

if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    name = sys.argv[2]
    ai = randomAI(name)
    sys.exit(app.exec_())
