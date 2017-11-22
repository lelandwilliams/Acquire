import random, string

corporations = ["Tower","Luxor","Worldwide","Festival","American", "Continental","Imperial"]

def new_player(bank = False):
    p_dict = dict()
    p_dict['money'] = 6000
    for corp in corporations:
        p_dict[corp] = 25 if bank else 0
    p_dict['Last Play'] = None

    return p_dict

def new_game(playerNames):
    """
    Produces the initial game state
    This is a partial state, showing the public information:
        player money and stock holdings
        tiles that have been played, and to which companies they
            have been assigned

    Player Hands and the order of the tile stack are private information
    Anon is for groups that are started by placing a non-adjacent tile.
    """
    state = dict()
    state['Players'] = dict()
    state['Group'] = dict()
    state['Phase'] = 'Place Starters'
    state['Turn'] = new_turn(playerNames[0])

    for player in playerNames + ['Bank']:
        state['Players'][player] = new_player(player == 'Bank')
    for corp in corporations:
        state['Group'][corp] = []
    for i in range(1, len(playerNames) + 1):
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
    sale['Trade'] = 0
    sale['Sell'] = 0
    sale['Done']= False
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
    print(state['Turn'])
    print()

def print_turn(turn):
    player_line = "{} placed {} ".format(turn['Player'], turn['Tile'])

    if turn['Merger'] is None and not turn['NewCorp']:
        if len(turn['Buy']) > 0:
            player_line += "and bought "
            if turn['Buy'][0] != 'Done':
                player_line += "{}".format(turn['Buy'][0])
                for c in turn['Buy'][1:]:
                    if c != 'Done':
                        player_line += ", {}".format(c)
        print(player_line)
        return None

    if turn['NewCorp']:
        player_line += "\n{} founded {}".format(turn['Player'], turn['NewCorp'])
    if type(turn['Merger']) is dict:
        player_line += "A MERGER"
        for sale in turn['Merger']['Sales']:
            if sale['Trade'] > 0:
                player_line += "\n{:3}{:10} Traded in {:2d} shares of {:12} for {:2d} {}"\
                        .format(sale['Player'],
                        sale['Trade'],
                        sale['Corporation'],
                        (sale['Trade']/2),
                        turn['Merger']['NewCorps'][0])
            if sale['Sell'] > 0:
                player_line += "\n{:3}{:10} Sold {:2d} shares of {:12}".format(\
                        sale['Player'],
                        sale['Sell'],
                        sale['Corporation'])
    if turn['Buy'][0] != 'Done':
        player_line += "\n{} bought {}".format(turn['Player'], turn['Buy'][0])
        for c in turn['Buy'][1:]:
            if c != 'Done':
                player_line += ", {}".format(c)
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
