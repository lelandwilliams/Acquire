import random, string
""" Provides the basic game state.
Some more complex state manipulation actions are found in rules.py

The state comes in two parts, one providing the public information
of the game, the other the hidden information.

The hidden information are the player hands.

The code throughout refers to the public information as 'state', and
the hidden information as 'hands'

The state dictionary has the following keys:
    "Players", "Group", "Phase", "Turn", "Seed"


Here is a breakdown of the values given to each key:
"Players": -> dict: player_name (str) -> player_dictionary



"Group", "Phase", "Turn", "Seed"

"""

corporations = ["Tower","Luxor","Worldwide","Festival","American", "Continental","Imperial"]

def dummy_hand(state, hand):
    """ This function allows a player to create a hands
    data structrure to be used in succ() only from the state
    and from knowing the player's own hand, which is given
    via get_actions(). """
    h = dict()
    cur_player = state['Turn']['Player']
    for p in state['Players']:
        if p == cur_player:
            h[cur_player] = hand
        else:
            h[p] = []
    return p

def getBonusPlayers(state, corp):
    """
    Provides some syntactic sugar. Returns a list of players
    that stand to currently earn holder bonuses """
    b_list = getBonus(state, corp)
    p_list = [p[0] for p in b_list]
    return p_list


def getBonuses(state):
    bonuses = list()
    players = list(state['Players'].keys())
    players.remove('Bank')
    for corp in state['Turn']['Merger']['OldCorps']:
        bonuses += getBonus(state, corp)
    return bonuses

def getBonus(state, corp):
    bonuses = list()
    players = list(state['Players'].keys())
    players.remove('Bank')
    holdings = [state['Players'][p][corp] for p in players]
    if len([x for x in holdings if x > 0]) == 1:
        for p in players:
            if state['Players'][p][corp] > 0:
                bonuses.append(new_bonus(p, 'Primary', corp, stockPrice(state,corp) * 10))
                bonuses.append(new_bonus(p, 'Secondary', corp, stockPrice(state,corp) * 5))
    elif holdings.count(max(holdings)) == 1:
        for p in players:
            if state['Players'][p][corp] == max(holdings) and max(holdings) > 0:
                bonuses.append(new_bonus(p, 'Primary', corp, stockPrice(state,corp) * 10))
        holdings.remove(max(holdings))
        for p in players:
            if state['Players'][p][corp] == max(holdings):
                bonuses.append(new_bonus(p, 'Secondary', corp, 
                        stockPrice(state,corp) * 5 // holdings.count(max(holdings))\
                                // 100 * 100))
    else:
        for p in players:
            if state['Players'][p][corp] == max(holdings):
                bonuses.append(new_bonus(p, 'Primary', corp, 
                        stockPrice(state,corp) * 10 // holdings.count(max(holdings))\
                                //100 * 100))
    return bonuses

def stockPrice(state, corp):
    """ Determines the current price of a share for a given corporation.

    Paremeters:
    ___________
    state: dict
        the current game state

    corp: str
        the name of the corporation for which a price is desired

    Returns:
    int
        the price of a share of stock in the specified corporation
    """
    corp_size = len(state['Group'][corp])
    price = 0
    if corp in ["Worldwide", "American", "Festival"]:
        price += 100
    if corp in ["Imperial", "Continental"]:
        price += 200
    if corp_size > 40:
        price += 1000
    elif corp_size > 30:
        price += 900
    elif corp_size > 20:
        price += 800
    elif corp_size > 10:
        price += 700
    elif corp_size > 5:
        price += 600
    else:
        price += corp_size * 100

    return price

def netWorth(player, s):
    """ Returns the calculated sum of a player's money, stock holdings value, and shareholder bonuses.
    """
    networth = s['Players'][player]['money']
    for corp in corporations:
        networth += s['Players'][player][corp] * stockPrice(s, corp)
        for bonus in getBonus(s, corp):
            if bonus['Player'] == player:
                networth += bonus['Bonus']
    return networth

#def new_player(playerType = 'Unspecified'):
def new_player(playerType):
    p_dict = dict()
    p_dict['money'] = 6000
    p_dict['playerType'] = playerType
    for corp in corporations:
        p_dict[corp] = 25 if playerType == 'Bank' else 0
    p_dict['Last Play'] = None

    return p_dict

def new_game(playerInfo):
    """ Produces the initial game state

    The games state is a dictionary.
    This is a partial state, showing the public information:
        player money and stock holdings
        tiles that have been played, and to which companies they
            have been assigned

    Player Hands and the order of the tile stack are private information
    Anon is for groups that are started by placing a non-adjacent tile.
    """
#   print(playerInfo)
#   return
    if type(playerInfo) is list:
        player_types_dict = {p : 'Unspecified' for p in playerInfo}
    elif type(playerInfo) is dict:
        player_types_dict = playerInfo

    state = dict()
    state['Players'] = dict()
    state['Group'] = dict()
    state['Phase'] = 'Place Starters'
    state['Turn'] = new_turn(list(player_types_dict)[0])
    state['Seed'] = None

    for player, ptype in player_types_dict.items():
        state['Players'][player] = new_player(ptype)
    state['Players']['Bank'] = new_player('Bank')

    for corp in corporations:
        state['Group'][corp] = []
    for i in range(1, len(player_types_dict) + 1):
        state['Group']["Anon{}".format(i)] = []

    return state

def new_turn(current_player = None):
    turn = dict()
    for phase in ['Player', 'Tile', 'Merger', 'Buy', 'NewCorp', 'Call Game']:
        turn[phase] = None if phase != 'Buy' else list()
    turn['Player'] = current_player
    return turn

def new_merger():
    merger = dict()
    merger['OldCorps'] = list()
    merger['NewCorps'] = list()
    merger['Bonus'] = list()
    merger['Sales'] = list()
    return merger

def new_mergerSale(player = None, corp = None):
    sale = dict()
    sale['Player'] = player
    sale['Corporation'] = corp
#   sale['Trade'] = 0
#   sale['Sell'] = 0
    sale['Done']= False
    sale['Types'] = [] # New feature !!
    return sale

def new_bonus(player = None, bonusType = None, corp = None, amount = 0):
    bonus = dict()
    bonus['Player'] = player
    bonus['Type'] = bonusType
    bonus['Corp'] = corp
    bonus['Bonus'] = amount
    return bonus

def tiletostr(t):
    return "{}-{}".format(t[0],t[1])

def print_state(state, hands= None):
    print()
    print('-' * 80)
    print()
    for p in state['Players']:
        corp_str = ""
        for c in corporations:
            if c == 'American':
                corp_str += '\n'
            corp_str += "  {:12} : {:2d}".format(c, state['Players'][p][c])
        if not hands is None and p != 'Bank':
            playerHand = [tiletostr(t) for t in hands[p]]
        else:
            playerHand = ""
        print("{:10} ${:5d} {:3} {} {}".format( p, 
            state['Players'][p]['money'],
            "",
            state['Players'][p]['Last Play'],
            playerHand))
        print("{}\n".format(corp_str))
#       for c in corporations:
#           if state['Players'][p][c] > 0:
#               print("{:>15} : {:2d}".format(c, state['Players'][p][c]))
    for g in state['Group']:
        if len(state['Group'][g]):
            print("{} {}".format(g, state['Group'][g]))
    print("Phase = {}".format(state['Phase']))
#   print(state['Turn'])
    print()
    print('-' * 80)
    print()

def print_turn(turn):
    if turn['Tile'] is None:
        player_line =  str("{}'s turn".format(turn['Player']))
        return player_line
    player_line = "{} placed {} ".format(turn['Player'], turn['Tile'])

    if turn['Merger'] is None and not turn['NewCorp']:
        if len(turn['Buy']) and turn['Buy'][0] !=  'Done':
            player_line += "and bought "
            if turn['Buy'][0] != 'Done':
                player_line += "{}".format(turn['Buy'][0])
                for c in turn['Buy'][1:]:
                    if c != 'Done':
                        player_line += ", {}".format(c)
        if type(turn['Call Game']) is str and turn['Call Game'] == 'No':
            player_line += "\n{} chose not to end the game".format(turn['Player'])
        if type(turn['Call Game']) is str and turn['Call Game'] == 'Yes':
            player_line += "\n{} called the game".format(turn['Player'])
        print(player_line)
        return None

    if turn['NewCorp']:
        player_line += "\n{} founded {}".format(turn['Player'], turn['NewCorp'])
    if type(turn['Merger']) is dict:
        player_line += "A MERGER\n"
        player_line += turn['Merger']['OldCorps'][0]
        for corp in turn['Merger']['OldCorps'][1:]:
            player_line += ", {}".format(corp)
        player_line += " merger into {}".format(turn['Merger']['NewCorps'][0])
        for bonus in turn['Merger']['Bonus']:
            player_line += "\n{} was the {} holder of {} and recieved $ {}".format(
                    bonus['Player'],
                    bonus['Type'],
                    bonus['Corp'],
                    bonus['Bonus'])
        for sale in turn['Merger']['Sales']:
            for sale_type in sale['Types']:
                if sale_type == 'Trade':
                    player_line += "\n{:3}{:10} Traded in two shares of {} for one {}"\
                            .format("", sale['Player'],
                            sale['Corporation'],
                            turn['Merger']['NewCorps'][0])
                elif sale_type == 'Sell':
                    player_line += "\n{:3}{:10} Sold a share of {:12}".format(\
                            "",
                            sale['Player'],
                        sale['Corporation'])
                elif sale_type == 'Keep':
                    player_line += "\n{:3}{:10} Kept the rest".format(\
                            "", sale['Player'])
    if len(turn['Buy']) > 0 and turn['Buy'][0] != 'Done':
        player_line += "\n{} bought {}".format(turn['Player'], turn['Buy'][0])
        for c in turn['Buy'][1:]:
            if c != 'Done':
                player_line += ", {}".format(c)

    if type(turn['Call Game']) is str and turn['Call Game'] == 'No':
        player_line += "\n{} chose not to end the game".format(turn['Player'])
    if type(turn['Call Game']) is str and turn['Call Game'] == 'Yes':
        player_line += "\n{} called the game".format(turn['Player'])

    print(player_line)


def save_state(s,h):
    of = open('savegame.txt', 'w')
    of.write(str((s,h)))
    of.close()

def read_state():
    f = open('savegame.txt', 'r')
    stuff = f.read()
    f.close()
    return eval(stuff)
