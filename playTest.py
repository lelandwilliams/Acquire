from rules import *
import random

players = ['Fluffy', 'Poo-Poo', 'Bender', 'Clyde']
s,h = new_game(players, shuffle = True)
history = []

def step(s,h,print_moves = False, history = None):
    a = getActions(s,h)
    move = random.choice(a[-1])

    if print_moves and len(a) == 2:
        print("{:12} {:5} {}".format(s['Turn']['Player'], a[0], a[-1][0]))
    elif print_moves:
        print("{:12} {:5} {}".format(a[1], a[0], a[-1][0]))

    s, h = succ(s, h, a[-1][0], history)
    if s['Turn']['Tile'] is None:
        model.print_turn(history[-1])
    return s,h

for _ in range(80):
    s,h = step(s,h,False, history)

model.print_state(s,h)
    
def foo():
    a = getActions(s,h)
    if len(a) == 2:
        print("{:12} {:5} {}".format(s['Turn']['Player'], a[0], a[-1][0]))
    else:
        print("{:12} {:5} {}".format(a[1], a[0], a[-1][0]))
    s, h = succ(s, h, a[-1][0])

    return succ(s, h, a[1][0])
