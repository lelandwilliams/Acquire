import random, sys
sys.path.append("..") # Allow import of rules 
from rules import *

players = ['Fluffy', 'Poo-Poo', 'Bender', 'Clyde']
s,h = new_game(players, shuffle = True)
history = []

def step(s,h,print_moves = False, history = None):
    a = getActions(s,h)
    move = random.choice(a[-1])

    s, h = succ(s, h, a[-1][0], history)
    if s['Turn']['Tile'] is None:
        model.print_turn(history[-1])
    return s,h

while not type(s['Turn']['Call Game']) is str or s['Turn']['Call Game'] == 'No':
    s,h = step(s,h,False, history)

model.print_turn(s['Turn'])
model.print_state(s,h)
for p in [p for p in s['Players'] if p != 'Bank']:
    print("{}: $ {}".format(p, model.netWorth(p,s)))

