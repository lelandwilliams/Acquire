import sys
from PyQt5.QtCore import QCoreApplication, QTimer
from client import AcquireClient

if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    a = AcquireClient()

    QTimer.singleShot(9000, a.quit_app)
    app.exec_()



