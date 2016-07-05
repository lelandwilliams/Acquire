import acquire

class Controller:
    def __init__(self):
        pass

    def liquidate(self):
        for corp in self.game.corporations:
            if self.game.corporations[corp].isActive():
                self.rewardPrimaries(corp)

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
            self.game.advanceCurrentPlayer()

        self.liquidate()

    def rewardPrimaries(self, corp):
        primaries = []
        secondaries = []

        for player in self.game.players:
            if player.stock[corp] > 0:
                if len(primaries) == 0 or player.stock[corp] > primaries[0].stock[corp]:
                    primaries = [player]
                elif player.stock[corp] == primaries[0].stock[corp]:
                    primaries.append(player)

        for idx in self.game.players:
            if self.game.players[idx].stock[corp] > 0 and idx not in primaries and len(primaries) == 1:
                if len(secondaries) == 0 or self.game.players[idx].stock[corp] > self.game.players[secondaries[0]].stock[corp]:
                    secondaries = [idx]
                elif self.game.players[idx].stock[corp] == self.game.players[secondaries[0]].stock[corp]:
                    secondaries.append(idx)

        if len(secondaries) == 0:
            bonus = self.game.corporations[corp].price() * 15 / len(primaries)
        else:
            bonus = self.game.corporations[corp].price() * 10 / len(primaries)

        if bonus % 100 > 0:
            bonux = bonus - (bonus % 100) + 100

        for idx in primaries:
            self.game.players[idx].money += bonus
            self.pb.updatePlayerMoney(self.game.players[idx])
            if self.debug:
                print(self.game.players[idx].name, "is a primary holder and recieves $", str(bonus))

        if len(secondaries) > 0:
            bonus = self.game.corporations[corp].price() * 5 / len(secondaries)
            if bonus % 100 > 0:
                bonux = bonus - (bonus % 100) + 100
            for idx in secondaries:
                self.game.players[idx].money += bonus
                self.pb.updatePlayerMoney(self.game.players[idx])
                if self.debug:
                    print(self.game.players[idx].name, "is a secondary holder and recieves $", str(bonus))

    def setup(self):
        players = self.setPlayers()
        self.game = acquire.Acquire(players)
        self.addPlayers(self.game.players)

        starters = self.game.setStarters()
        for tile in starters:
            self.changeTileColor(tile, 'None')
        self.game.fillHands()


