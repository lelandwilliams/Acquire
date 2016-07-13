from PyQt5.QtCore import QThread, QTimer
from PyQt5.QtWidgets import QApplication
import sys

#class Timertest(QObject):
class Timertest():
    def __init__(self):
        self.app = QApplication(sys.argv)
#       super().__init__()
#       thread = QThread()
#       thread.exec_()
#        print("Now starting a timer")
#        QTimer.singleShot(5000, self.a)
#       QTimer.singleShot(5000, self, SLOT(self.b()))
#       QTimer.singleShot(5000, self, SLOT(self.c()))
        self.a()
        sys.exit(self.app.exec_())

    def a(self):
        print("Now in a()")
        QTimer.singleShot(5000, self.b)

    def b(self):
        print("Now in b()")
        QTimer.singleShot(5000, self.c)

    def c(self):
        print("Now in c()")
        self.app.quit()


a = Timertest()
