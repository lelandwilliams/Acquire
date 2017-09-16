##################################################
#          r o b o t F a c t o r y
#
# This class helps manage the various AI agents
# classes and distributes them to requesters
#
##################################################
from randomAI import randomAI
import subprocess 

class robotFactory:
    def getAI(self, robotType, name, acquire_id):
        return randomAI(name, acquire_id)

    def startAI(self, robotType='Random', name = None, acquire_id = None):
        process_list = ["python"]
        if robotType == 'Random':
            arg_list.append("randomAI.py")
        if not name == None:
            arg_list.append("-n")
            arg_list.append(name)
        if not acquire_id == None:
            arg_list.append("-i")
            arg_list.append(acquire_id)
        subprocess.Popen(arg_list)

