import model
import copy, string, random

"""
Rules: knows the rules of the acquire board game, and
provides the new_game(), getActions() and succ() methods
"""


def new_game(playerNames, shuffle = True, seed = None):
    state = model.new_game(playerNames)
    state['Seed'] = seed
    hands = build_hands(state, shuffle = shuffle, seed = seed)
    return state,hands

def getActions(state, hand):
    if state['Turn']['Tile'] is None:
        options = []
        if not hand is None:
            options =  [t for t in hand[state['Turn']['Player']] if isLegal(state, t)]
        if len(options) == 0:
            options = ['Nothing']
        return ('Place', options)
    elif state['Turn']['NewCorp'] == 'Choose':
        return ('Found',[c for c in model.corporations if len(state['Group'][c]) == 0])
    elif type(state['Turn']['Merger']) is dict and len(state['Turn']['Merger']['NewCorps'])>1:
        return ('Choose Survivor', state['Turn']['Merger']['NewCorps'])
    elif type(state['Turn']['Merger']) is dict\
            and len(state['Turn']['Merger']['NewCorps'])==1\
            and len(state['Turn']['Merger']['Sales']) > 0\
            and not state['Turn']['Merger']['Sales'][-1]['Done']:
        actions = ['Sell', 'Keep']
        idx = 0
        while state['Turn']['Merger']['Sales'][idx]['Done']:
            idx += 1
        sale = state['Turn']['Merger']['Sales'][idx]
        if state['Players'][sale['Player']][sale['Corporation']] > 1 and\
                state['Players']['Bank'][state['Turn']['Merger']['NewCorps'][0]] > 0:
            actions.append('Trade')
        return('Liquidate', sale['Player'], actions) #Note that this is a triple
    elif len(state['Turn']['Buy']) < 3:
        possibles = [c for c in model.corporations\
                if len(state['Group'][c]) != 0\
                and state['Players']['Bank'][c] > 0\
                and model.stockPrice(state, c) <= state['Players'][state['Turn']['Player']]['money']]
#       return ('Buy', possibles + ['Done']) if len(possibles) else None
        return ('Buy', possibles + ['Done'])
    elif state['Turn']['Call Game'] and type(state['Turn']['Call Game']) is bool:
        return('Call', ['Yes', 'No'])
    else:
        return None

def getFullActions(state, hand):
    """
    DEPRECATED. DO NOT USE
    """
    actions = list()
    player = state['Turn']['Player']
    for tile in hand[player]:
        pass

def succ(state, hands, action, history = None):
    """
    param @history: either None, in which case it is ignored,
        or a reference to a list, to be added onto if a new turn is created
    """
    actions = getActions(state,hands)
    if not action in actions[-1] and not hands is None:
        return None
    s = copy.deepcopy(state)
    h = copy.deepcopy(hands)

    # Below we resolve the possible actions

# --- Place a tile on the board ---------------------
    if actions[0] == 'Place' and action == 'Nothing': 
        # This happens in the rare case that a player has no valid move
        # necessary to push the turn forward.
        s['Turn']['Tile'] = action

    elif actions[0] == 'Place' and action != 'Nothing': 
        s['Turn']['Tile'] = action
        if not hands is None:
            h[s['Turn']['Player']].remove(action)
        s['Players'][s['Turn']['Player']]['Last Play'] = action

        # First assign the tile to an Anon group
        # see if there are any existing Anon groups to merge/attach
        t_group = None # the 'Group' key that the tile is being added to
        anons = getAdjacentAnons(state,action)
        if len(anons) > 0:
            t_group = anons[0]
            s['Group'][anons[0]].append(action)
            for a in anons[1:]:
                while len(s['Group'][a]):
                    s['Group'][anons[0]].append(s['Group'][a].pop())
            # If we have merged some anon tiles and playing starters is over,
            # then set 'NewCorp' so that actions will be to choose a new Corp
            s['Turn']['NewCorp'] = 'Choose' if (s['Phase'] == 'Place') else None
        else:
            # create a new Anon group for the tile
            t_group = assignAnon(s, action)

        # Now add the tiles from an Anon group to
        # a corporation adjacent to the placed tile.
        # This handles the case that a tile connects other unconneted tiles
        # to a corporation, as well as the tile is a simple addition to an
        # existing corporation
        adj_c = getAdjacentCorps(state, action) 
        if len(adj_c) == 1:
            s['Turn']['NewCorp'] = False
            s['Turn']['Merger'] = None
            while len(s['Group'][t_group]) > 0:
                s['Group'][adj_c[0]].append(s['Group'][t_group].pop())

        # OR, if the newly placed tile connects corporations to each other,
        # then a merger occurs
        # So create a new merger structure. The largest corporations are
        # added to 'NewCorps' and the smalles to 'OldCorps'
        # If len(NewCorps) > 1 then the succ action will be to choose one to stay
        elif len(adj_c) > 1:
            s['Turn']['NewCorp'] = False
            s['Turn']['Merger'] = model.new_merger()
            largest_corp_size = max([len(s['Group'][corp]) for corp in adj_c])
            # Determine which corporations are dissolved, and which lives on
            for corp in adj_c:
                if len(s['Group'][corp]) < largest_corp_size:
                    s['Turn']['Merger']['OldCorps'].append(corp)
                else:
                    s['Turn']['Merger']['NewCorps'].append(corp)
            # If survivor fully determined, then assign bonuses, start sales
            if len(s['Turn']['Merger']['NewCorps']) == 1:
                resolveMerger(s)


# --------- Create a New Corporation ---------------------
    elif actions[0] == 'Found':
        s['Turn']['NewCorp'] = action
        # Find the tile group that contains the last played tile
        group = [g for g in s['Group'] if s['Turn']['Tile'] in s['Group'][g]][0]
        # Move all tiles from that group to the new corporation
        while len(s['Group'][group]) > 0:
            s['Group'][action].append(s['Group'][group].pop())
        # Award the founder a free share of stock
        s['Players'][s['Turn']['Player']][action] +=1
        s['Players']['Bank'][action] -= 1

# ---------- Choose Which Corporation survives a Merger -----------------
    elif actions[0] == 'Choose Survivor':
        for corp in s['Turn']['Merger']['NewCorps']:
            if corp != action:
                s['Turn']['Merger']['OldCorps'].append(corp)
        for corp in s['Turn']['Merger']['OldCorps']:
            if corp in s['Turn']['Merger']['NewCorps']:
               s['Turn']['Merger']['NewCorps'].remove(corp) 
#       print(s['Turn']['Merger']['NewCorps'])
        resolveMerger(s)

# ---------- After a merger, shareholders choose what to do with stock -----------------
    elif actions[0] == 'Liquidate':
        idx = 0
        while s['Turn']['Merger']['Sales'][idx]['Done']:
           idx += 1 
        sale  = s['Turn']['Merger']['Sales'][idx]
        if action == 'Keep':
            sale['Done'] = True
            sale['Types'].append('Keep')
        elif action == 'Trade':
#           sale['Trade'] += 2
            sale['Types'].append('Trade')
            s['Players'][sale['Player']][sale['Corporation']] -= 2
            s['Players']['Bank'][sale['Corporation']] += 2
            s['Players'][sale['Player']][s['Turn']['Merger']['NewCorps'][0]] +=1
            s['Players']['Bank'][s['Turn']['Merger']['NewCorps'][0]] -=1
            if s['Players'][sale['Player']][sale['Corporation']] <= 0:
                sale['Done'] = True
    
        elif action == 'Sell':
#           sale['Sell'] += 1
            sale['Types'].append('Sell')
            s['Players'][sale['Player']][sale['Corporation']] -= 1
            s['Players']['Bank'][sale['Corporation']] += 1
            s['Players'][sale['Player']]['money'] += model.stockPrice(s, sale['Corporation'])
            if s['Players'][sale['Player']][sale['Corporation']] <= 0:
                sale['Done'] = True
        # Finally, if all sales are Done, lump all the tiles together into one group
        if sale == s['Turn']['Merger']['Sales'][-1] and sale['Done']:
            mergeGroups(s)

# ------------- Buy A Share of Stock --------------------

    elif actions[0] == 'Buy':
        if action == 'Done':
            while len(s['Turn']['Buy']) < 3:
                s['Turn']['Buy'].append('Done')
        else:
            s['Turn']['Buy'].append(action)
            s['Players']['Bank'][action] -= 1
            s['Players'][s['Turn']['Player']][action] +=1

# ---------- Determine whether to end the game -----------------
    elif actions[0] == 'Call':
        s['Turn']['Call Game'] = action

# ---------- Final Housekeepng of the succ state ------------------
    # Fill hand at end of turn
    if not hands is None:
        while len(h[s['Turn']['Player']]) < 6 and len(h['Bank']) > 0:
            h[s['Turn']['Player']].append(h['Bank'].pop())

    if s['Turn']['Call Game'] is None: 
        s['Turn']['Call Game'] = endGameConditionsMet(s)

    if getActions(s,h) is None and not s['Turn']['Call Game'] == 'Yes': 
        # None signals the end of a turn
        # so we should create a new Turn dict() with the next player

        # first append current turn to history, if history is given
        if not history is None:
            history.append(s['Turn'])

        # Now figure out who the next player should be
        players = list(s['Players'].keys())
        players.remove('Bank')
        if s['Turn']['Player'] == players[-1] and s['Phase']=='Place Starters':
            # Last turn of placing starters, time to move to regular play
            # Next Player is the player who placed the lowest tile
            s['Phase'] = 'Place'
            start_player = None
            for p in players:
                if start_player is None:
                    start_player = p
                elif s['Players'][p]['Last Play'][1] > s['Players'][start_player]['Last Play'][1]:
                    continue
                elif s['Players'][p]['Last Play'][1] < s['Players'][start_player]['Last Play'][1]:
                    start_player = p
                elif s['Players'][p]['Last Play'][0] < s['Players'][start_player]['Last Play'][0]:
                    start_player = p
            s['Turn'] = model.new_turn(start_player)
        elif s['Turn']['Player'] == players[-1]:
            s['Turn'] = model.new_turn(players[0])
        else:
            cur_player = players.index(s['Turn']['Player'])
            s['Turn'] = model.new_turn(players[cur_player + 1])

    return s,h
    
# ------------------------ Helper Functions --------------------

def assignAnon(state, t):
    anons = [g for g in state['Group'] if g not in model.corporations]
    for a in anons:
        if state['Group'][a] == []:
            state['Group'][a].append(t)
            return a

    new_name = "Anon{}".format(int(anons[-1][-1]) + 1)
    state['Group'][new_name] = [t]
    return new_name

def build_hands(state, shuffle = False, seed = None):
    hands= dict()
    for p in state['Players']:
        hands[p] = []
    hands['Bank'] = [(j,i) for i in string.ascii_uppercase[:9] for j in range(1,13)]
    if shuffle and not seed is None:
        random.seed(seed)
    if shuffle:
        random.shuffle(hands['Bank'])
    for p in state['Players']:
        hands[p].append(hands['Bank'].pop())
    return hands

def endGameConditionsMet(state):
    sizes = [len(state['Group'][c]) for c in model.corporations if len(state['Group'][c]) > 0]
    if len(sizes) == 0:
        return False
    if max(sizes) > 40 or min(sizes) > 10:
        return True
    return False

def getAdjacentAnons(state, t):
    anons = [g for g in state['Group'] if g not in model.corporations]
    return [a for a in anons if isAdjacent(t, state['Group'][a])]

def getAdjacentCorps(state, t):
    return [c for c in model.corporations if isAdjacent(t,state['Group'][c])]

def isLegal(state, t):
    """ Method to see if a tile is legal to lay
    Acquire stipulates that a tile may not be placed when
    A) It would merge two safe corporations
     - or -
    B) It would create a new corporation when there are already seven
    on the board
    """
    # These rules don't apply when placing starter tiles
    if state['Phase'] == 'Place Starters':
        return True
    if len(getAdjacentCorps(state, t)) == 1:
        return True

    # Test for condition A
    if len( [c for c in getAdjacentCorps(state,t) if len(state['Group'][c]) >= 11]) > 1:
        return False
    # Test for condition B
    numActive =  len([c for c in model.corporations if len(state['Group'][c]) > 0]) 
    if numActive == len(model.corporations) and len(getAdjacentAnons(state, t)) > 0:
        return False
    # Passed Tests, so return True
    return True

def isAdjacent(tile, group):
    if (tile[0],chr(ord(tile[1])+1)) in group:
        return True
    if (tile[0],chr(ord(tile[1])-1)) in group:
        return True
    if (tile[0]+1,tile[1]) in group:
        return True
    if (tile[0]-1,tile[1]) in group:
        return True
    return False

def isSafe(state, corp):
    return len(state['Group'][corp]) >= 11

def mergeGroups(state):
    for corp in state['Turn']['Merger']['OldCorps']:
        while len(state['Group'][corp]) > 0:
            state['Group'][state['Turn']['Merger']['NewCorps'][0]].append(
                state['Group'][corp].pop())
    for group in state['Group']:
        if group not in model.corporations and state['Turn']['Tile'] in state['Group'][group]:
            while len(state['Group'][group]) > 0:
                state['Group'][state['Turn']['Merger']['NewCorps'][0]].append(
                    state['Group'][group].pop())


def resolveMerger(state):
    bonuses = model.getBonuses(state)
    for bonus in bonuses:
        state['Players'][bonus['Player']]['money'] += bonus['Bonus']
    state['Turn']['Merger']['Bonus'] = bonuses

    # generate Merger Sales: 
    # append to the list all players that have stock in a merged company
    for corp in state['Turn']['Merger']['OldCorps']:
        for player in list(state['Players'].keys()):
            if state['Players'][player][corp] > 0 and player != 'Bank':
                state['Turn']['Merger']['Sales'].append(model.new_mergerSale(player,corp))
    if len(state['Turn']['Merger']['Sales']) == 0:
        mergeGroups(state)


