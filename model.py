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

def tiletostr(t):
    return "{}-{}".format(t[0],t[1])

def print_state(state, hands= None):
    for p in state['Players']:
        if not hands is None:
            playerHand = [tiletostr(t) for t in hands[p]]
        else:
            playerHand = ""
        print("{:20} ${:5d} {:7} {} {}".format( p, 
            state['Players'][p]['money'],
            "",
            state['Players'][p]['Last Play'],
            playerHand))
        for c in corporations:
            if state['Players'][p][c] > 0:
                print("{:>15} : {:2d}".format(c, state['Players'][p][c]))
    for g in state['Group']:
        if len(state['Group'][g]):
            print("{} {}".format(g, state['Group'][g]))
    print("Phase = {}".format(state['Phase']))
    print(state['Turn'])
    print()


