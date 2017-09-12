import sys, uuid, subprocess
from controller import Controller
from network import AcquireClient, AcquireLogger
from robotFactory import robotFactory
from PyQt5.QtCore import QCoreApplication, pyqtSlot, QTimer

class myClient(AcquireClient):
    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def trigger_messages(self):
        QTimer.singleshot(400, self.here_messages)

    @pyqtSlot()
    def here_messages(self):
        player1 = str(uuid.uuid4())
        player2 = str(uuid.uuid4())
        player3 = str(uuid.uuid4())
        self.send_message("ADDPLAYER;" + master + ";Bender;" + player1) 
        self.send_message("ADDPLAYER;" + master + ";C3P0;" + player2) 
        self.send_message("ADDPLAYER;" + master + ";Hal;" + player3) 
        self.main()

if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    print("starting server")
    master = str(uuid.uuid4())
    print("starting client")
    subprocess.Popen(["python", "controller.py", "-m", master])
#   factory = robotFactory()
#   a = Controller(master)
#   b = myClient()
    b = AcquireClient()
    b.set_id(master)
#   logger = AcquireLogger()
#    b.here_messages()
    player1 = str(uuid.uuid4())
#   b.send_message("ADDPLAYER;" + master + ";Bender;" + player1) 
    player2 = str(uuid.uuid4())
#   b.send_message("ADDPLAYER;" + master + ";C3P0;" + player2) 
    player3 = str(uuid.uuid4())
#   b.send_message("ADDPLAYER;" + master + ";Hal;" + player3) 
#   player1class = factory.getAI(None, "Bender", player1)
#   player2class = factory.getAI(None, "C3PO", player1)
#   player3class = factory.getAI(None, "Hal", player1)
#   b.send_message("BEGIN;" + master) 
#    b.send_message("KILL;" + master) 
    sys.exit(app.exec_())

