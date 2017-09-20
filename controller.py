import sys, uuid
import acquire_model
from network import AcquireServer, DEFAULTPORT
from PyQt5.QtCore import pyqtSlot, QTimer, QCoreApplication

class Controller(AcquireServer):
    def __init__(self, port = DEFAULTPORT):
        self.game = acquire_model.Acquire()
        super().__init__(port)

    @pyqtSlot()
    def parse_message(self, m):
        print("Controller.parse_message received: " + m)
        clientid, command,  parameter = m.split(';')
        if command == "REGISTER":
            if len(self.game.players) > 6:
                self.outgoing_message_q.put("ERROR;" + parameter + ";CAN'T JOIN - GAME IS FULL;")
            elif self.game.state != "SETUP":
                self.outgoing_message_q.put("ERROR;" + parameter + ";CAN'T JOIN - GAME HAS STARTED;")
            elif parameter in self.name.players:
                self.outgoing_message_q.put("ERROR;" + parameter + ";NAME UNAVAILABLE;")
            elif self.get_name_of_id(clientid) != None:
                self.outgoing_message_q.put("ERROR;" + parameter + ";PLAYER ALREADY NAMED;")
            else:
                self.outgoing_message_q.put("NOTICE;" + parameter + ";ADDED;")
                self.send_private_message('PRIVATE;;', parameter)
        elif command == "KILL":
            self.outgoing_message_q.put('DISCONNECT;;;')
            self.game.gameState = 'DONE'
        elif command == "BEGIN":
            if len(self.game.players) < 3:
                self.outgoing_message_q.put("ERROR;" + parameter + ";CAN'T START - NOT ENOUGH PLAYERS;")
            else:
                self.outgoing_message_q.put('BEGIN;;;')
                self.gameState = 'PLACESTARTERS'
                self.outgoing_message_q.put(self.build_request(self.starterPlayer),'PLACESTARTER')
        elif command == "PLACESTARTER":
            if self.gameState != 'PLACESTARTERS':
                self.outgoing_message_q.put("ERROR;" + parameter + ";NOT STARTER PHASE;")
            elif clientid != self.get_id_of_name(self.game.players[self.starterPlayer].name):
                self.outgoing_message_q.put("ERROR;" + parameter + ";PLAYER ID != NAME;")
            elif parameter not in self.game.players[self.starterPlayer].hand:
                self.outgoing_message_q.put("ERROR;" + parameter + ";YOU DON'T HAVE THAT TILE;")
            else:
                self.game.placeStarter(parameter)
                self.game.players[self.starterPlayer].hand.remove(tile)
                self.game.players[self.starterPlayer].lastPlay = tile
                self.outgoing_message_q.put("PLAY;" + self.get_name_of_id(clientid)
                        + ";PLACESTARTER" + parameter)
                self.starterPlayer += 1
                if self.starterPlayer >= len(self.game.players):
                    start = self.determineStartingPlayer()
                    self.game.currentPlayerNumber = start
                    self.outgoing_message_q.put("INFO;" + self.game.players[start].name + ";STARTS")
                    self.build_request(start, 'PLACETILE')
                    self.game.gameState = 'DONE'
                    self.outgoing_message_q.put('DISCONNECT;;')

    def build_request(self, player_num, request_type):
        message = 'REQUEST;'
        message += self.game.players[player_num].name
        messsage += ';' + request_type + ';'
        return message

    def get_name_of_id(self, clientid):
        for client in self.clients:
            if client.client_id == clientid:
                return client.name
        sys.exit("Error: (get_name_of_id) uuid does not match any client")

    def get_id_of_name(self, name):
        for client in self.clients:
            if client.name == name:
                return client.client_id
        sys.exit("Error: (get_id_of_name) name does not match any client")

    def set_name_of_id(self, clientid, name):
        for client in self.clients:
            if client.client_id == clientid:
                client.name = name

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
                actions = ["Sell","Sell All"]
                if player.stock[corp] > 1 and self.game.corporations[largestCorp].shares_available > 0:
                    actions.append("Trade All")
                    actions.append("Trade")
                actions.append("Keep")
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
                self.pb.updatePlayerStock(player)

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
            self.pb.updatePlayerStock(player) #gui related
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


    def oldMainLoop(self):
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
            result = self.chooseGameOver()
        else:
            result = self.game.aiChooseGameOver()

        if result:
            if self.gui: self.announceGameOver(self.game.getCurrentPlayer().name)
            self.game.setGameOver()

    def resolveMerger(self, player, tile):
        mergingCorps = self.game.adjoiningCorps(tile)
        largestCorps = self.game.getLargestCorps(tile)
        largestCorp = None
#       for bigcorp in largestCorps: 
#           mergingCorps.remove(bigcorp)
        if self.debug:
            print(str(mergingCorps), "will be merged.")
            print(str(largestCorps), "are the largest corporations")
        if len(largestCorps) == 1:
            largestCorp = largestCorps[0]
        else:
            largestCorp = self.pickMerger(player, largestCorps)
        mergingCorps.remove(largestCorp)

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
        elif result == "Trade All":
            while player.stock[corp] >= 2 and player.stock[largestCorp] >= 1:
                player.stock[corp] -= 2
                player.stock[largestCorp] += 1
                self.game.corporations[corp].shares_available +=2
                self.game.corporations[largestCorp].shares_available -=1
        elif result == "Sell All":
            while player.stock[corp] >= 1:
                player.stock[corp] -= 1
                self.game.corporations[corp].shares_available += 1
                player.money += self.game.corporations[corp].price()


    def rewardPrimaries(self, corp):
        primaries = self.game.primaryHolders(corp)
        secondaries = []
        if len(primaries) == 1:
            secondaries = self.game.secondaryHolders(corp)

        if len(secondaries) == 0:
            primary_bonus = self.game.corporations[corp].price() * 15 // len(primaries)
        else:
            primary_bonus = self.game.corporations[corp].price() * 10 // len(primaries)

        if primary_bonus % 100 > 0:
            primary_bonus = primary_bonus - (primary_bonus % 100) + 100

        for player in primaries:
            player.money += primary_bonus
            self.pb.updatePlayerMoney(player)
            if self.debug:
                print(player.name, "is a primary holder of ", corp, "and recieves $", str(primary_bonus))

        if len(secondaries) > 0:
            secondary_bonus = self.game.corporations[corp].price() * 5 // len(secondaries)
            if secondary_bonus % 100 > 0:
                secondary_bonus = secondary_bonus - (secondary_bonus % 100) + 100
            for player in secondaries:
                player.money += secondary_bonus
                self.pb.updatePlayerMoney(player)
                if self.debug:
                    print(player.name, "is a secondary holder of", corp, "and recieves $", str(secondary_bonus))


    def setup(self):
        players = self.setPlayers()
        self.game = acquire_model.Acquire(players)
        self.addPlayers(self.game.players)

        starters = self.game.setStarters()
        for tile in starters:
            self.changeTileColor(tile, 'None')
        self.game.fillHands()


