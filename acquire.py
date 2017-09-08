import sys, uuid
from controller import Controller
from network import AcquireClient
from robotFactory import robotFactory

if __name__ == "__main__":
    master = uuid.uuid4().hex
    factory = robotFactory()
    a = Controller(master)
    b = AcquireClient()
    b.set_id(master)
    player1 = uuid.uuid4().hex
    b.send_message("ADDPLAYER;" + master + ";Bender;" + player1) 
    player2 = uuid.uuid4().hex
    b.send_message("ADDPLAYER;" + master + ";C3P0;" + player2) 
    player3 = uuid.uuid4().hex
    b.send_message("ADDPLAYER;" + master + ";Hal;" + player3) 
    player1class = factory.getAI(None, "Bender", player1)
    player2class = factory.getAI(None, "C3PO", player1)
    player3class = factory.getAI(None, "Hal", player1)
    b.send_message("BEGIN;" + master) 

