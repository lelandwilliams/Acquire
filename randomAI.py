from network import AcquireClient
from PyQt5.QtCore import QCoreApplication, pyqtSlot, QTimer
import sys, random

class randomAI(AcquireClient):
    def __init__(self, name, acquire_id = None):
        self.name = name
        super().__init__()
        self.outgoing_message_q.put("REGISTER;"+self.name)


if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    name = sys.argv[2]
    ai = randomAI(name)
    sys.exit(app.exec_())
