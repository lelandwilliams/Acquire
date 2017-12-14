from featureExtractor import *
import random, subprocess, sys, math
import model, rules

f = open('weights.gam')
tile_growth_weights = eval(f.readline())
turns_remaining_weights = eval(f.readline())
f.close()

#subprocess.call('./exampleMaker.py')

def reconstruct_states():
    f = open('example.gam')
    state, history = eval(f.read())
    history.append(state['Turn'])
    f.close()
    players = [p for p in state['Players'] if p != 'Bank']
    seed = state['Seed']
    s, hand = rules.new_game(players, True, seed)
    states = [s]

    for turn in history:
        s = states[-1]
        if type(turn['Tile']) is tuple:
            s, hand = rules.succ(s, hand, turn['Tile'], None)
        if not turn['NewCorp'] is None and turn['NewCorp']:
            s, hand = rules.succ(s, hand, turn['NewCorp'])
        if not turn['Merger'] is None:
            if rules.getActions(s, hand)[0] == 'Choose Survivor':
                s, hand = rules.succ(s, hand, turn['Merger']['NewCorps'][0], None)
            for p in turn['Merger']['Sales']:
                for action in p['Types']:
                    s, hand = rules.succ(s, hand, action)
        for share in turn['Buy']:
            if rules.getActions(s, hand)[0] == 'Buy':
                s, hand = rules.succ(s, hand, share, None)
        if turn['Call Game']:
            s, hand = rules.succ(s, hand, turn['Call Game'], None)
        states.append(s)

    return states, history

def corp_outlook(states, turn_num):
    results = dict()
    for corp in [c for c in model.corporations if len(states[turn_num]['Group'][c])]:
        cur_size = len(states[turn_num]['Group'][corp])
        corp_end = turn_num + 1
        while corp_end < len(states) and len(states[corp_end]['Group'][corp]):
            corp_end += 1
        corp_end -= 1
        end_size = len(states[corp_end]['Group'][corp])
        results[corp] = dict()
        results[corp]['Turns'] = corp_end - turn_num
        results[corp]['Tiles'] = end_size - cur_size
#       print("{}: {} more turns, {} more tiles".format(corp, corp_end - turn_num, end_size - cur_size))
    return results

def train(states, eta = 0.01):
    idx = 0
    while idx < len(states):
        results = corp_outlook(states, idx)
        for corp in results:
            features = feature_extractor(states[idx], corp)
            revise(features, tile_growth_weights, results[corp]['Tiles'], eta)
            revise(features, turns_remaining_weights, results[corp]['Turns'], eta)
        idx += 1

def revise(phi, w, y, eta):
    train_loss = (dot_product(phi, w) - y) 
    for el in w:
        w[el] -= eta * 2 * train_loss * phi[el]

def run():
    for i in range(1,3):
        subprocess.call('./exampleMaker.py')
        states, history = reconstruct_states()
        train(states, 1/math.sqrt(i))
#   train(states)

states, history = reconstruct_states()
