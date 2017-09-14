import sys
from network import AcquireServer
from PyQt5.QtCore import QCoreApplication

if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    a = AcquireServer()
    a.outgoing_message_q.put("HiHiHiHi")
    sys.exit(app.exec_())
