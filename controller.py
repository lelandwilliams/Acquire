import acquire

class Controller:
    def __init__(self):
        pass

    def pickStock(self):
        player = self.game.getCurrentPlayer()
        for idx in range(1,4):
            available = []
            for corp in self.game.corporations:
                if (self.game.corporations[corp].isActive() and 
                        self.game.corporations[corp].shares_available > 0 and
                        self.game.corporations[corp].price() <= player.money):
                    available.append(corp)
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
            newcorp = self.chooseNewCorp(player,tile)
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

    def setup(self):
        players = self.setPlayers()
        self.game = acquire.Acquire(players)
        self.addPlayers(self.game.players)

        starters = self.game.setStarters()
        for tile in starters:
            self.changeTileColor(tile, 'None')
        self.game.fillHands()


