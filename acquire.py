import sys, string, random
from PyQt5.QtWidgets import QApplication
from mainWidget import AcquireUI

class Player:
    def __init(self, name, playerType):
        self.name = name
        self.playerType = playerType
        self.hand = []
        self.money = 5000

class Game:
    def __init__(self, ui = nil):
        self.tiles = self.initiate_tiles()
        self.tilegroups = []
        for i in range(7):
            self.tilegroups.append([])

        self.ui = ui
        self.players = []
        for newplayer in self.ui.setPlayers():
            self.players.append(Player(i, playerType[i]))

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

    def setStarters():
        for i in range(len(self.players)):
            starters.append(self.tiles.pop())
        for tile in starters:
            game.ui.changeTileColor(tile, 'None')

            groups = self.adjoiningGroups(tile)
            if len(groups) > 0:
                while len(groups) > 1:
                    self.tilegrousp[groups[0]] += self.tilegrousp[groups[1]] 
                    del self.tilegrousp[groups[1]] 
                    groups = self.adjoiningGroups(tile)
                self.tilegroups[groups[0]].append(tile)
            else:
                self.tilegroups.append([tile])

def play():
    game = Game()
    starters = []
    hand = []
#-------->    while(len( <----------------------------
    sys.exit(game.app.exec_())



