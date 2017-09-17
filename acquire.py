import sys, uuid, subprocess
from controller import Controller
#from network import AcquireClient, AcquireSimpleLogger
from robotFactory import robotFactory
from PyQt5.QtCore import QCoreApplication, pyqtSlot, QTimer

if __name__ == "__main__":
#   print("starting server")
#   print("starting client")
    subprocess.Popen(["python", "serverTest.py"])
    subprocess.Popen(["python", "clientTest.py"])
    factory = robotFactory()
    factory.startAI()

