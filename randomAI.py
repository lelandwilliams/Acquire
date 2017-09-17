from network import AcquireClient
from PyQt5.QtCore import QCoreApplication, pyqtSlot, QTimer
import sys, random

class randomAI(AcquireClient):
    def __init__(self, name, acquire_id = None):
        super().__init__()
        self.name = name



if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    print(sys.argv)
    name = sys.argv[2]
    ai = randomAI(name)
    sys.exit(app.exec_())
