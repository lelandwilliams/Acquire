import sys, string, random
#from PyQt5.QtWidgets import QApplication
#from mainWidget import AcquireUI

class Player:
    def __init__(self, name, playerType):
        self.name = name
        self.playerType = playerType
        self.hand = []
        self.money = 5000

class Acquire:
    def __init__(self, players):
        self.players = players
        self.tiles = self.initiate_tiles()
        self.tilegroups = []
        for i in range(7):
            self.tilegroups.append([])

        random.shuffle(self.players)

    def addTiletoGroup(self,tile,group):
        index = self.tilegroups.index(group)
        self.tilegroups[index].append(tile)

    def adjoiningGroups(self, tile):
        adjoininggrouplist  = []
        for i in range(len(self.tilegroups)):
            if self.isAdjoining(tile, self.tilegroups[i]):
                adjoininggrouplist.append(i)
        return adjoininggrouplist
                
    def advanceCurrentPlayer(self):
        self.currentPlayer = (self.currentPlayer + 1 ) % (len(self.players) -1)

    def aiChooseTile(player):
        random.shuffle(player.hand)
        return player.hand.pop()

    def determineStartingPlayer(self, arr, start=0, current=1):
        if current >= len(arr):
            return start

        if arr[start][2] < arr[current][2]:
            return self.determineStartingPlayer(arr, start, current +1)
        elif arr[start][2] > arr[current][2]:
            return self.determineStartingPlayer(arr, current, current +1)
        else:
            if arr[start][0] < arr[current][0]:
                return self.determineStartingPlayer(arr, start, current +1)
            elif arr[start][0] > arr[current][0]:
                return self.determineStartingPlayer(arr, current, current +1)

    def gameOver(self):
        return len(self.tiles) <= 1

    def getCurrentPlayer(self):
        return self.players[self.currentPlayerNumber]

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

    def setStarters(self):
        starters = []
        for i in range(len(self.players)):
            starters.append(self.tiles.pop())

        for tile in starters:
            groups = self.adjoiningGroups(tile)
            if len(groups) > 0:
                while len(groups) > 1:
                    self.tilegroups[groups[0]] += self.tilegroups[groups[1]] 
                    del self.tilegroups[groups[1]] 
                    groups = self.adjoiningGroups(tile)
                self.tilegroups[groups[0]].append(tile)
            else:
                self.tilegroups.append([tile])

        self.currentPlayerNumber = self.determineStartingPlayer(starters)

        return starters

def play():
    game = Game()
    starters = []
    hand = []
#-------->    while(len( <----------------------------
    sys.exit(game.app.exec_())



