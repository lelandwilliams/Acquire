##################################################
#          r o b o t F a c t o r y
#
# This class helps manage the various AI agents
# classes and distributes them to requesters
#
##################################################
from randomAI import randomAI

class robotFactory:
    def getAI(self, robotType, name, acquire_id):
        return randomAI(name, acquire_id)

