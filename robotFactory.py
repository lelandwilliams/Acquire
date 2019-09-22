##################################################
#          r o b o t F a c t o r y
#
# This class manage the various AI agent classes
# and instantiates them with given parameters
# upon request
#
##################################################

from randomAI import randomAI
import subprocess, random, robotNames 

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

