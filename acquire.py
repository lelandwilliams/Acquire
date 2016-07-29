import sys, string, random

class Player:
    def __init__(self, name, playerType):
        self.name = name
        self.playerType = playerType
        self.playerSubtype = None
        self.hand = []
        self.money = 6000
        self.stock = {}
        self.lastPlacement = None
        self.stockAcquired = []
        for name in Acquire.corpNames:
            self.stock[name] = 0


    def __repr__(self):
        s = "\t"
        s += self.name.ljust(20)
        s += (" $")
        s += (str(self.money))
        s += (" ")
        for i in self.hand:
            s += (str(i))
        s += "\n\t\t"
        s += str(self.stock) + "\n"
        return s

class Corp:
    def __init__(self, name, index, model):
        self.game = model
        self.name = name
        self.shares_available = 25
        self.price_modifier = self.setInitialPrice()
        self.active = False
        self.groupIndex = index

    def __repr__(self):
        s = "\t"
        s += self.name.ljust(12)
        if self.active:
            s += "     active, "
        else:
            s += " not active, "
        s += str(self.size()).rjust(2) + (" tiles, ")
        s += str(self.shares_available).rjust(2) + (" shares outstanding,")
        s += (" price: $ ")
        s += str(self.price())
        s += ('\n')
        return s

    def isActive(self):
        return self.active

    def isSafe(self):
        return self.isActive() and (self.size() >= 6)

    def setActive(self, b):
        self.active = b

    def setInitialPrice(self):
        if self.name in ["Worldwide", "American", "Festival"]:
            return 100
        if self.name in ["Imperial", "Continental"]:
            return 200
        return 0

    def size(self):
        return len(self.game.tilegroups[self.groupIndex])

    def price(self):
        price = self.price_modifier
        if self.size() > 40:
            price += 1000
        elif self.size() > 30:
            price += 900
        elif self.size() > 20:
            price += 800
        elif self.size() > 10:
            price += 700
        elif self.size() > 5:
            price += 600
        else:
            price += self.size() * 100
        return price

class Acquire:
    corpNames = ["Tower","Luxor","Worldwide","Festival","American", "Continental","Imperial"]

    def __init__(self, players):
        self.game_over = False
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
        s = "Players\n"
        for p in self.players:
            s += str(p)
        s += "Corporations\n"
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
        self.players[self.currentPlayerNumber].stockAcquired = []

    def aiChooseCorp(self, corps):
        random.shuffle(corps)
        return corps[0]

    def aiChooseGameOver(self):
        return True

    def aiChooseMergerStockAction(self, actions):
        return actions[random.randrange(len(actions))]

    def aiChooseStock(self, available):
        corps = list(available)
        return corps[random.randrange(len(corps))]

    def aiChooseMerger(self, corps):
        return corps[random.randrange(len(corps))]

    def aiChooseTile(self,player):
        random.shuffle(player.hand)
        return player.hand[0]

    def corpSize(self, corp):
        return len(self.tilegroups[self.corporations[corp].groupIndex])

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

    def endGameConditionsMet(self):
        activecorps = []
        for corp in self.corporations:
            if self.corporations[corp].isActive():
                activecorps.append(corp)
        if len(activecorps) == 0:
            return False

        allSafe = True
        for corp in activecorps:
            allSafe = allSafe and self.corporations[corp].isSafe()

        if allSafe:
            return True

        for corp in activecorps:
            if self.corporations[corp].size() >= 41:
                return true

        return False

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
        #return len(self.tiles) <= 1
        return self.game_over

    def getCurrentPlayer(self):
        return self.players[self.currentPlayerNumber]

    def getLargestCorps(self, tile):
        corps = self.adjoiningCorps(tile)
        sizes = []
        largest = []
        for corp in corps:
            sizes.append(self.corpSize(corp))
        for corp in corps:
            if self.corpSize(corp) == max(sizes):
                largest.append(corp)
        return largest

    def getLargestCorpsi(self, tile):
        corps = self.adjoiningCorps(tile)
        maxSize = 0
        largestCorp = [] 

        for corp in corps:
            if len(largestCorp) == 0:
                largestCorp.append(corp)
            elif self.corpSize(corp) > self.corpSize(largestCorp[0]):
                while len(largestCorp) > 0:
                    largestCorp.pop()
                largestCorp.append(corp)
            elif self.corpSize(corp) ==  self.corpSize(largestCorp[0]):
                largestCorp.append(corp)

        return largestCorp

    def getMergerPlayers(self):
        return self.players[self.currentPlayerNumber:] + self.players[:self.currentPlayerNumber]

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
            a[name] = Corp(name,idx,self)
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

    def playerBoughtStock(self, player, stock):
        player.stockAcquired.append(stock)
        player.money -= self.corporations[stock].price()
        self.corporations[stock].shares_available -= 1
        player.stock[stock] += 1

    def primaryHolders(self, corp):
        holders = []
        maxshares = 0
        for player in self.players:
            if player.stock[corp] > maxshares:
                holders = [player]
                maxshares = player.stock[corp]
            elif player.stock[corp] == maxshares:
                holders.append(player)
            
        return holders

    def secondaryHolders(self, corp):
        primaries = self.primaryHolders(corp)
        possibles = []
        secondaries = []
        for player in self.players:
            if player.stock[corp] > 0:
                possibles.append(player)

        for player in primaries:
            if player in possibles:
                possibles.remove(player)

        maxshares = 0
        for player in possibles:
            if player.stock[corp] > maxshares:
                maxshares = player.stock[corp]
                secondaries = [player]
            elif player.stock[corp] == maxshares:
                secondaries.append(player)

        return secondaries

    def setActive(self, corp, player, tile):
        self.corporations[corp].setActive(True)
        groupindices = self.adjoiningGroups(tile)
        while len(groupindices) > 1:
            self.addGrouptoGroup(groupindices[0], groupindices[-1])
            groupindices = self.adjoiningGroups(tile)
        self.addGrouptoGroup(groupindices[0], self.corporations[corp].groupIndex)
        self.addTiletoCorp(tile, corp)
        if self.corporations[corp].shares_available > 0:
            self.corporations[corp].shares_available -= 1
            player.stock[corp] += 1
            player.stockAcquired.append(corp)

    def setGameOver(self):
        self.game_over = True

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
players.append(Player('Hal 9000', 'Robot'))
players.append(Player('Puny Human', 'Human'))

def play():
    game = Game()
    starters = []
    hand = []
#-------->    while(len( <----------------------------
    sys.exit(game.app.exec_())



