import sys, string, random

class Player:
    def __init__(self, name, playerType):
        self.name = name
        self.playerType = playerType
        self.hand = []
        self.money = 6000

    def __repr__(self):
        s = '\t'
        s.append(self.name)
        s.append(" $")
        s.append(self.money)
        s.append(" ")
        for i in self.hand:
            s.append(i)
        s.append(" \n")
        return s

class Corp:
    def __init__(self, name):
        self.name = name
        self.shares_available = 25
        self.share_price = self.setInitialPrice()
        self.active = False
        self.anchor_tile = None

    def __repr__(self):
        s = "\t"
        s += (self.name)
        s += (" active: ")
        if self.active:
            s += ("Yes  shares outstanding: ")
        else:
            s += ("No   shares outstanding: ")
        s += str(self.shares_available)
        s += (" price: $ ")
        s += str(self.price())
        s += ('\n')
        return s

    def isActive(self):
        return self.active

    def setAnchorTile(self, tile):
        self.anchor_tile = tile

    def setActive(self, b):
        self.active = b

    def setInitialPrice(self):
        if self.name in ["Worldwide", "American", "Festival"]:
            return 300
        if self.name in ["Imperial", "Continental"]:
            return 400
        return 200

    def price(self):
        return self.share_price


class Acquire:
    def __init__(self, players):
        self.corpNames = ["Tower","Luxor","Worldwide","Festival","American",
                "Continental","Imperial"]
        self.players = players
        self.currentPlayerNumber = 0
        self.tiles = self.initiate_tiles()
        self.tilegroups = []
        self.corporations = self.initiate_corps()

        random.shuffle(self.players)

    def __repr__(self):
        s = "Corporations\n"
        for corp in self.corporations:
            s += str(self.corporations[corp])
        return s

    def addTiletoGroup(self,tile,group):
        index = self.tilegroups.index(group)
        self.tilegroups[index].append(tile)

    def adjoiningGroups(self, tile):
        adjoininggrouplist  = []
        for i in range(len(self.tilegroups)):
            if self.isAdjoining(tile, self.tilegroups[i]):
                adjoininggrouplist.append(i)
        return adjoininggrouplist

    def adjoiningCorps(self, tile):
        corps = []
        groups = self.adjoiningGroups(tile)
        for corp in self.corporations:
            for group in groups:
                if self.corporations[corp].anchorTile in self.tilegroups[group]:
                    corps.append(corp)
        return corps
                
    def advanceCurrentPlayer(self):
        self.currentPlayerNumber = (self.currentPlayerNumber + 1 ) % len(self.players) 

    def aiChooseCorp(self, corps):
        random.shuffle(corps)
        return corps[0]

    def aiChooseTile(self,player):
        random.shuffle(player.hand)
        return player.hand.pop()

    def determineStartingPlayer(self, arr, start=0, current=1):
        if current >= len(arr):
            return start

        if arr[start][1] < arr[current][1]:
            return self.determineStartingPlayer(arr, start, current +1)
        elif arr[start][1] > arr[current][1]:
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

    def inactiveCorps(self):
        a = []
        for corp in self.corporations:
            if not self.corporations[corp].isActive():
                a.append(corp)
        return a

    def initiate_corps(self):
        a = {}
        for name in self.corpNames:
            a[name] = Corp(name)
        return a

    def initiate_tiles(self):
        tiles = []
        for i in string.ascii_uppercase[:9]:
            for j in range(1,13):
                tiles.append( (j,i) )
        random.shuffle(tiles)
        return tiles

    def isAdjoining(self,tile,group):
        if (tile[0],str(ord(tile[1])+1)) in group:
            return True
        if (tile[0],str(ord(tile[1])-1)) in group:
            return True
        if (tile[0]+1,tile[1]) in group:
            return True
        if (tile[0]-1,tile[1]) in group:
            return True
        return False

    def placeTile(self, tile, starters = True):
        groups = self.adjoiningGroups(tile)
        if len(groups) > 0:
            groups[0].append(tile)
            while len(groups) > 1:
                self.tilegroups[groups[0]] += self.tilegroups[groups[1]] 
                del self.tilegroups[self.tilegroups.index(groups[1])] 
            self.tilegroups[groups[0]].append(tile)
        else:
            self.tilegroups.append([tile])

    def setActive(self, corp, player, tile):
        self.corporations[corp].setActive(True)
        self.corporations[corp].setAnchorTile(tile)

    def setStarters(self):
        starters = []
        for i in range(len(self.players)):
            starters.append(self.tiles.pop())

        for tile in starters:
            self.placeTile(tile, True)

        self.currentPlayerNumber = self.determineStartingPlayer(starters)
        return starters

    def tileToStr(self, tile):
        return str(tile[0]) + "-" + tile[1]

players = []
players.append(Player('Bender', 'Robot'))
players.append(Player('C3P0', 'Robot'))
players.append(Player('Bender', 'Robot'))
players.append(Player('Puny Human', 'Human'))

def play():
    game = Game()
    starters = []
    hand = []
#-------->    while(len( <----------------------------
    sys.exit(game.app.exec_())



