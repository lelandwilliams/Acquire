import sys, string, random
from PyQt5.QtWidgets import QApplication
from mainWidget import AcquireUI

class Game:
    def __init__(self):
        self.tiles = self.initiate_tiles()
        self.app = QApplication(sys.argv)
        self.ui = AcquireUI()
        self.tilegroups = []
        for i in range(7):
            self.tilegroups.append([])
        self.ui.show()

    def addTiletoGroup(self,tile,group):
        index = self.tilegroups.index(group)
        self.tilegroups[index].append(tile)

    def adjoiningGroups(self, tile):
        adjoininggrouplist  = []
        for i in range(len(self.tilegroups)):
            if self.isAdjoining(tile, self.tilegroups[i]):
                adjoininggrouplist.append(i)
        return adjoininggrouplist
                
    def initiate_tiles(self):
        tiles = []
        for i in string.ascii_uppercase[:9]:
            for j in range(1,13):
                tiles.append(str(j) + '-' + i)
        random.shuffle(tiles)
        return tiles

    def isAdjoining(self,tile,group):
        if (tile[0] + '-' + chr(ord(tile[2])+1))in group:
            return True
        if (tile[0] + '-' + chr(ord(tile[2])-1)) in group:
            return True
        if (chr(ord(tile[0])+1) + '-' + tile[2]) in group:
            return True
        if (chr(ord(tile[0])-1) + '-' + tile[2]) in group:
            return True
        return False

def play():
    game = Game()
    starters = []
    hand = []
    for i in range(6):
        starters.append(game.tiles.pop())
        hand.append(game.tiles.pop())
    for tile in starters:
        if len(game.tiles) < 8:
            game.tiles.append([tile])
        else:
            groups = game.adjoiningGroups(tile)
            if len(groups) > 0:
                game.tilegroups[groups[0]].append(tile)
            else:
                game.tilegroups.append([tile])
            game.ui.changeTileColor(tile, 'None')
#-------->    while(len( <----------------------------
    sys.exit(game.app.exec_())



