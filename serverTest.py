import sys
from network import AcquireServer
from PyQt5.QtCore import QCoreApplication
from controller import Controller

if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
#    a = AcquireServer()
    a = Controller()
#   a.outgoing_message_q.put("HiHiHiHi")
#   a.outgoing_message_q.put("RebelRebel")
#   a.outgoing_message_q.put("Eat My Shorts")
    sys.exit(app.exec_())
