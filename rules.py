import model
import copy, string, random

"""
Rules: knows the rules of the acquire board game, and
provides the new_game(), getActions() and succ() methods
"""


def new_game(playerNames, shuffle = True, seed = None):
    state = model.new_game(playerNames)
    hands = build_hands(state, shuffle = shuffle, seed = seed)
    return state,hands

def getActions(state, hand):
    if state['Turn']['Action'] is None:
        return ('Place',[t for t in hand[state['Turn']['Player']] if isLegal(state, t)])
    elif state['Turn']['NewCorp']:
        return ('Found',[c for c in state['Group'] if len(state['Group']) == 0])
    elif state['Turn']['Merger']:
        raise('Not Yet Implemented')
    elif len(state['Turn']['Buy']) < 3:
        possibles = [c for c in model.corporations\
                if len(state['Group'][c]) != 0\
                and state['Player']['Bank'][c] > 0\
                and stockPrice(c) <= state['Player'][state['Turn']['Player']]['money']]
        return ('Buy', possibles + ['Done']) if len(possibles) else None
    elif state['Turn']['Call Game']:
        return('Call', ['Yes', 'No'])
    else:
        return None

def getFullActions(state, hand):
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
    if not action in actions[1]:
        return None
    s = copy.deepcopy(state)
    h = copy.deepcopy(hands)
    s['Turn']['Action'] = action
    h[s['Turn']['Player']].remove(action)

    # Below we resolve the possible actions

    # Place a tile on the board
    if actions[0] == 'Place': 
        s['Players'][s['Turn']['Player']]['Last Play'] = action
        # first see if there are any Anon groups to merge/attach
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
            s['Turn']['NewCorp'] = (s['Phase'] == 'Place')
        else:
            t_group = assignAnon(s, action)

        # Now add tiles to an adjacent corporation
        adj_c = getAdjacentCorps(state, action) 
        if len(adj_c) == 1:
            s['Turn']['NewCorp'] = False
            while len(h['Group'][t_group]):
                s[adj_c[0]].append(h['Group'][t_group].pop())
        if len(adj_c) > 1:
            s['Turn']['NewCorp'] = False
            pass ## Not Implemented Yet

        # Fill hand
        while len(h[s['Turn']['Player']]) < 6 and len(h['Bank']) > 0:
            h[s['Turn']['Player']].append(h['Bank'].pop())


    # some final evaluation of the successor state
    if s['Turn']['Call Game'] is None: 
        s['Turn']['Call Game'] = endGameConditionsMet(s)
    if getActions(s,h) is None: 
        # None signals the end of a turn
        # so we should create a new one with the next player
        if not history is None:
            history.append(s['Turn'])
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
    
# ------------------------------------------------------------

def assignAnon(state, t):
    anons = [g for g in state['Group'] if g not in model.corporations]
    for a in anons:
        if state['Group'][a] == []:
            state['Group'][a].append(t)
            return a

    new_name = "Anon{}".format(int(anons[-1][-1]) + 1)
    state['Group'][new_name] = [t]

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
    print ('endGameConditionsMet is undefined !!!')
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
    # Test for condition A
    if len( [c for c in getAdjacentCorps(state,t) if len(state['Group'][c] >= 11)]) > 1:
        return False
    # Test for condition B
    numActive =  len([c for c in model.corporations if len(state['Group'][c]) > 0]) 
    if numActive == len(model.corporations) and getAdjacentAnons(state, t) > 0:
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

