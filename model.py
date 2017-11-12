import random, string

corporations = ["Tower","Luxor","Worldwide","Festival","American", "Continental","Imperial"]

def new_player(bank = False):
    p_dict = dict()
    p_dict['money'] = 6000
    for corp in corporations:
        p_dict[corp] = 25 if bank else 0
    p_dict['last play'] = None

    return p_dict

def new_game(playerNames):
    """
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
    for phase in ['Player', 'Play', 'Merger', 'Buy', 'NewCorp', 'Result']:
        turn[phase] = None
    turn['Player'] = current_player
    return turn

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
            state['Players'][p]['last play'],
            playerHand))
        for c in corporations:
            if state['Players'][p][c] > 0:
                print("{:>15} : {:2d}".format(c, state['Players'][p][c]))
    for g in state['Group']:
        if len(state['Group'][g]):
            print("{} {}".format(g, state['Group'][g]))
    print("Phase = {}".format(state['Phase']))
    print(state['Turn'])


