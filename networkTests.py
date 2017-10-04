import unittest, sys
import network
from PyQt5.QtCore import QCoreApplication

class Test(unittest.TestCase):

    def test_serverOpens(self):
        a = network.NetworkBaseClass()
        a.openServer()
        opens = a.server.isListening()
        a.server.close()
        self.assertTrue(opens, "Server Failed to Open")
        self.assertFalse(a.server.isListening(), "Server Failed to Close")

    def test_twoServers(self):
        message = "Scooby Do"
        a = network.NetworkBaseClass()
        a.openServer()
        opens = a.server.isListening()
        self.assertTrue(opens, "Server A Failed to Open")

        b = network.NetworkBaseClass(None,a.server.serverPort() +1)
        b.openServer()
        opens = b.server.isListening()
        self.assertTrue(opens, "Server B Failed to Open")

        bytesWritten = b.write(a.server.serverAddress(), a.server.serverPort(), message) 
        self.assertEqual(len(message), bytesWritten,
                "b.write() only transmitted " + str(bytesWritten) + " bytes")

#       messageReceived = a.read()
        self.assertEqual(message, b.lastMessageReceived, "Message not properly received")
        a.server.close()
        b.server.close()

if __name__ == "__main__":
    app = QCoreApplication([])
    unittest.main()
    sys.exit(app.exec_())

