from network import AcquireClient
from PyQt5.QtCore import QCoreApplication, pyqtSlot, QTimer
import sys

class randomAI(AcquireClient):
    def __init__(self, name, acquire_id):
        super().__init__()
        self.set_id(acquire_id)
        self.name = name


if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    ai = randomAI()
    sys.exit(app.exec_())
