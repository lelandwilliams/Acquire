import sys, string, random

class Player:
    def __init__(self, name, playerType):
        self.name = name
        self.playerType = playerType
        self.hand = []
        self.money = 6000

    def __repr__(self):
        s = (self.name)
        s += (" $")
        s += (str(self.money))
        s += (" ")
        for i in self.hand:
            s += (str(i))
        return s

class Corp:
    def __init__(self, name, index):
        self.name = name
        self.shares_available = 25
        self.share_price = self.setInitialPrice()
        self.active = False
        self.groupIndex = index

    def __repr__(self):
        s = "\t"
        s += (self.name)
        s += (" active: ")
        if self.active and self.shares_available > 0:
            s += str(self.shares_available) + ("shares outstanding")
        else:
            s += ("No shares outstanding: ")
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
        while len(self.tilegroups) < 7:
            self.tilegroups.append([])
        self.corporations = self.initiate_corps()

        self.fillHands()
        random.shuffle(self.players)

    def __repr__(self):
        s = "Corporations\n"
        for corp in self.corporations:
            s += str(self.corporations[corp])
        return s

    def addGrouptoGroup(self,oldgroup,newgroup):
        while(len(self.tilegroups[oldgroup]) > 0):
            self.tilegroups[newgroup].append(self.tilegroups[oldgroup].pop()) 
        if oldgroup > 6:
            del self.tilegroups[oldgroup]

    def addTiletoCorp(self, tile, corp):
        self.tilegroups[self.corporations[corp].groupIndex].append(tile)

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
        groupindices = self.adjoiningGroups(tile)
        for corp in self.corporations:
                if self.corporations[corp].groupIndex in groupindices:
                    corps.append(corp)
        return corps
                
    def advanceCurrentPlayer(self):
        self.currentPlayerNumber = (self.currentPlayerNumber + 1 ) % len(self.players) 

    def aiChooseCorp(self, corps):
        random.shuffle(corps)
        return corps[0]

    def aiChooseTile(self,player):
        random.shuffle(player.hand)
        return player.hand[0]

    def corpSize(self, corp):
        for group in self.tilegroups:
            if self.corporations[corp].anchor_tile in group:
                return len(group)
        return 0

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

    def evaluatePlay(self, tile):
        if len(self.adjoiningGroups(tile)) == 0:
            return "Regular"
        if len(self.adjoiningCorps(tile)) == 0:
            if len(self.inactiveCorps()) == 0:
                return "Illegal"
            return "NewCorp"
        if len(self.adjoiningCorps(tile)) == 1:
            return "Addon"
        safe_corps = 0
        for corp in self.adjoiningCorps(tile):
            if self.corpSize(corp) > 10:
                safe_corps += 1
        if safe_corps > 1:
            return "Illegal"
        return "Merger"

    def fillHands(self):
        for player in self.players:
            while len(player.hand) < 6:
                player.hand.append(self.tiles.pop())
            player.hand.sort()

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
        idx = 0
        for name in self.corpNames:
            a[name] = Corp(name,idx)
            idx += 1
        return a

    def initiate_tiles(self):
        tiles = []
        for i in string.ascii_uppercase[:9]:
            for j in range(1,13):
                tiles.append( (j,i) )
        random.shuffle(tiles)
        return tiles

    def isAdjoining(self,tile,group):
        if (tile[0],chr(ord(tile[1])+1)) in group:
            return True
        if (tile[0],chr(ord(tile[1])-1)) in group:
            return True
        if (tile[0]+1,tile[1]) in group:
            return True
        if (tile[0]-1,tile[1]) in group:
            return True
        return False

    def placeStarter(self, tile):
        groupindices = self.adjoiningGroups(tile)
        if len(groupindices) == 0:
            self.tilegroups.append([tile])
        else:
            while len(groupindices) > 1:
                self.addGroupToGroup(groupindices[-1], groupindices[0])
                groupindices = self.adjoiningGroups(tile)
            self.tilegroups[groupindices[0]].append(tile)

    def placeTile(self, tile):
        playtype =  self.evaluatePlay(tile)
        if playtype == "Regular":
            self.tilegroups.append([tile])
        elif playtype == "Addon":
            groupindices = self.adjoiningGroups(tile)
            while len(groupindices) > 1:
                self.addGrouptoGroup(groupindices[-1],groupindices[0])
                groupindices = self.adjoiningGroups(tile)
            self.addTiletoCorp(tile, self.adjoiningCorps(tile)[0]) 
        else:
            print("improper call to Acquire.placeTile()")

    def setActive(self, corp, player, tile):
        self.corporations[corp].setActive(True)
        groupindices = self.adjoiningGroups(tile)
        while len(groupindices) > 1:
            self.addGrouptoGroup(groupindices[0], groupindices[-1])
            groupindices = self.adjoiningGroups(tile)
        self.addGrouptoGroup(groupindices[0], self.corporations[corp].groupIndex)
        self.addTiletoCorp(tile, corp)

    def setStarters(self):
        starters = []
        for i in range(len(self.players)):
            starters.append(self.tiles.pop())

        for tile in starters:
            self.placeStarter(tile)

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



