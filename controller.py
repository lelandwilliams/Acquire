import acquire

class Controller:
    def __init__(self):
        pass

    def pickStock(self):
        player = self.game.getCurrentPlayer()


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


