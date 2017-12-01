##################################################
#          n e t w o r k T e s t 
#
# This class starts a logger client, a GM,
# and three clients as players,
# The server should then start.
#
##################################################

import subprocess, random

class robotFactory:
    def __init__(self):
        self.taken = list()

    def getAI(self, robotType, name, acquire_id):
        return randomAI(name, acquire_id)

    def startAI(self, robotType='Random', name = None, acquire_id = None):
        arg_list = ["python"]
        if robotType == 'Random':
            arg_list.append("randomAI.py")
        arg_list.append("-n")
        if name == None:
            arg_list.append(self.getName())
        else:
            arg_list.append(name)
        if not acquire_id == None:
            arg_list.append("-i")
            arg_list.append(acquire_id)
        subprocess.Popen(arg_list)

    def getName(self):
        name = random.choice(robotNames.names)
        while name in self.taken:
            name = random.choice(robotNames.names)
        return name
if __name__ == '__main__':
    process_list = list()
    process_list.append(["python", "server.py"])
    process_list.append(["python", "client.py", "-t", "LOGGER"])
    process_list.append(["python", "client.py", "-t", "GM"])
    process_list.append(["python", "client.py", "-t", "PLAYER", "-n", "C3P0"])
    process_list.append(["python", "client.py", "-t", "PLAYER", "-n", "C3P1"])
    process_list.append(["python", "client.py", "-t", "PLAYER", "-n", "C3P2"])

    for args in process_list:
        subprocess.Popen(args)
