import sys
from network import AcquireSimpleLogger
from PyQt5.QtCore import QCoreApplication

if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    a = AcquireSimpleLogger()
#   a.outgoing_message_q.put("HiHiHiHi")
    sys.exit(app.exec_())
