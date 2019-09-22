import sys
from network import AcquireSimpleLogger
from PyQt5.QtCore import QCoreApplication

if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    a = AcquireSimpleLogger()
    sys.exit(app.exec_())
