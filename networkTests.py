import unittest, sys
import network
from PyQt5.QtCore import QCoreApplication

class Test(unittest.TestCase):

    def test_serverOpens(self):
        a = network.NetworkBaseClass()
        a.openServer()
        opens = a.server.isListening()
        a.server.close()
        self.assertTrue(opens)
        self.assertFalse(a.server.isListening())

if __name__ == "__main__":
    app = QCoreApplication
    unittest.main()
    sys.exit(app.exec_())

