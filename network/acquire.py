#! /usr/bin/env python3
import subprocess
from controller import Controller
from robotFactory import robotFactory
from PyQt5.QtCore import QCoreApplication, pyqtSlot, QTimer

if __name__ == "__main__":
    print("Starting")
    subprocess.Popen(["python", "serverTest.py"])
    subprocess.Popen(["python", "clientTest.py"])
    factory = robotFactory()
    factory.startAI()

