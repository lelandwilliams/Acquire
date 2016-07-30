import acquire

class Controller:
    def __init__(self):
        self.gui = False

    def liquidate(self):
        for corp in self.game.corporations:
            if self.game.corporations[corp].isActive():
                self.rewardPrimaries(corp)
                for player in self.game.players:
                    if player.stock[corp] > 0:
                        reward = player.stock[corp] * self.game.corporations[corp].price()
                        player.money += reward
                        self.pb.updatePlayerMoney(player)
                        if self.debug:
                            print(player.name, "recieves $", reward, "for shares in ", corp)

    def liquidateMergerStock(self, player, corp, largestCorp):
        for player in self.game.getMergerPlayers():
            result = ""
            while(player.stock[corp] > 0 and result != "Keep"):
                actions = ["Sell","Keep"]
                if player.stock[corp] > 1 and self.game.corporations[largestCorp].shares_available > 0:
                    actions.append("Trade")
                if player.playerType == "Human":
                    result = self.chooseMergerStockAction(player, corp, largestCorp, actions)
                else:
                    result =  self.game.aiChooseMergerStockAction(actions)
                self.resolveMergerAction(player, corp, largestCorp, result)

    def pickCorp(self,player,tile): 
        corp = None
        corps = self.game.inactiveCorps()
        if(player.playerType == 'Human'):
            available = {}
            for c in corps:
                available[c] = self.game.corporations[c].price() 
            corp = self.chooseNewCorp(available)
        else:
            corp = self.game.aiChooseCorp(corps)
        
        return corp

    def pickMerger(self, player, corps):
        if self.game.getCurrentPlayer().playerType == "Human":
            return self.chooseMerger(corps)
        else:
            return self.game.aiChooseMerger(corps)

    def pickStock(self):
        player = self.game.getCurrentPlayer()
        for idx in range(1,4):
            available = {}
            for corp in self.game.corporations:
                if (self.game.corporations[corp].isActive() and 
                        self.game.corporations[corp].shares_available > 0 and
                        self.game.corporations[corp].price() <= player.money):
                    available[corp] = self.game.corporations[corp].price() 
            if len(available) > 0:
                if player.playerType == 'Human':
                    stock = self.chooseStock(available, idx)
                else:
                    stock = self.game.aiChooseStock(available)
                self.game.playerBoughtStock(player,stock)
                self.pb.updatePlayerMoney(player)

    def playTile(self):
        player = self.game.getCurrentPlayer()
        tile = self.chooseTile(player)
        outcome = self.game.evaluatePlay(tile)
        if outcome == "Regular":
            self.game.placeTile(tile)
            self.changeTileColor(tile, 'None')
        elif outcome == "NewCorp":
            newcorp = self.pickCorp(player,tile)
            self.game.setActive(newcorp,player,tile)
            self.changeGroupColor(newcorp)
        elif outcome == "Addon":
            self.game.placeTile(tile)
            self.changeGroupColor(self.game.adjoiningCorps(tile)[0])
        elif outcome == "Merger":
            self.resolveMerger(player, tile)
            self.game.placeTile(tile)
            self.changeGroupColor(self.game.adjoiningCorps(tile)[0])
        player.lastPlacement = tile
        player.hand.remove(tile)
        player.hand.append(self.game.tiles.pop())
        player.hand.sort()


    def newGame(self):
        self.setup()
        while(not self.game.gameOver()):
            if self.debug:
                print(str(self.game))
            self.playTile()
            self.pickStock()
            if self.game.endGameConditionsMet():
                self.offerGameOver()
            self.game.advanceCurrentPlayer()

        self.liquidate()

    def offerGameOver(self):
        player = self.game.getCurrentPlayer()
        if player.playerType == "Human":
            result = self.ChooseGameOver()
        else:
            result = self.game.aiChooseGameOver()

        if result:
            if self.gui: self.announceGameOver(self.game.getCurrentPlayer().playerName)
            self.game.setGameOver()

    def resolveMerger(self, player, tile):
        mergingCorps = self.game.adjoiningCorps(tile)
        largestCorps = self.game.getLargestCorps(tile)
        largestCorp = None
        for bigcorp in largestCorps: mergingCorps.remove(bigcorp)
        if self.debug:
            print(str(mergingCorps), "will be merged.")
            print(str(largestCorps), "are the largest corporations")
        if len(largestCorps) == 1:
            largestCorp = largestCorps[0]
        else:
            largestCorp = self.pickMerger(player, largestCorps)

        for corp in mergingCorps:
            self.rewardPrimaries(corp)
            self.liquidateMergerStock(player, corp, largestCorp)
            self.game.addGrouptoGroup(self.game.corporations[corp].groupIndex,
                self.game.corporations[largestCorp].groupIndex)
            self.game.corporations[corp].setActive(False)

        self.game.addTiletoCorp(tile, largestCorp)
                

    def resolveMergerAction(self, player, corp, largestCorp, result):
        if result == "Trade":
            player.stock[corp] -= 2
            player.stock[largestCorp] += 1
            self.game.corporations[corp].shares_available +=2
            self.game.corporations[largestCorp].shares_available -=1
        elif result == "Sell":
            player.stock[corp] -= 1
            self.game.corporations[corp].shares_available += 1
            player.money += self.game.corporations[corp].price()
        elif result == "Trade All:"
            while stock[corp] >= 2 and stock[largestCorp. >= 1:
                player.stock[corp] -= 2
                player.stock[largestCorp] += 1
                self.game.corporations[corp].shares_available +=2
                self.game.corporations[largestCorp].shares_available -=1
        elif result == "Sell":
            while stock[corp] >= 1:
                player.stock[corp] -= 1
                self.game.corporations[corp].shares_available += 1
                player.money += self.game.corporations[corp].price()


    def rewardPrimaries(self, corp):
        primaries = self.game.primaryHolders(corp)
        secondaries = []
        if len(primaries) == 1:
            secondaries = self.game.secondaryHolders(corp)

        if len(secondaries) == 0:
            bonus = self.game.corporations[corp].price() * 15 // len(primaries)
        else:
            bonus = self.game.corporations[corp].price() * 10 // len(primaries)

        if bonus % 100 > 0:
            bonux = bonus - (bonus % 100) + 100

        for player in primaries:
            player.money += bonus
            self.pb.updatePlayerMoney(player)
            if self.debug:
                print(player.name, "is a primary holder of ", corp, "and recieves $", str(bonus))

        if len(secondaries) > 0:
            bonus = self.game.corporations[corp].price() * 5 // len(secondaries)
            if bonus % 100 > 0:
                bonux = bonus - (bonus % 100) + 100
            for player in secondaries:
                player.money += bonus
                self.pb.updatePlayerMoney(player)
                if self.debug:
                    print(player.name, "is a secondary holder of", corp, "and recieves $", str(bonus))

    def setup(self):
        players = self.setPlayers()
        self.game = acquire.Acquire(players)
        self.addPlayers(self.game.players)

        starters = self.game.setStarters()
        for tile in starters:
            self.changeTileColor(tile, 'None')
        self.game.fillHands()


