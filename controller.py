import acquire

class Controller:
    def __init__(self):
        pass
 
    def newGame(self):
        players = self.setPlayers()
        self.game = acquire.Acquire(players)
        self.addPlayers(self.game.players)

        starters = self.game.setStarters()
        for tile in starters:
            self.changeTileColor(tile, 'None')
        self.game.fillHands()
        while(not self.game.gameOver()):
            player = self.game.getCurrentPlayer()
            if self.debug:
                print(str(self.game))
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
            self.game.advanceCurrentPlayer()


