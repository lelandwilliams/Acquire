from featureExtractor import *
import random, subprocess, sys, math
import model, rules

f = open('weights.gam')
tile_growth_weights = defaultdict(float)
turns_remaining_weights = defaultdict(float)
f.close()

def reconstruct_states(game):
    state, history = eval(game)
    history.append(state['Turn'])
    players = [p for p in state['Players'] if p != 'Bank']
    seed = state['Seed']
    s, hand = rules.new_game(players, True, seed)
    states = [s]

    for turn in history:
        step(states, turn)

    return states, history

def step(states, turn):
    s = states[-1]
    if type(turn['Tile']) is tuple:
        result = rules.succ(s, None, turn['Tile'])
        if result is None:
            print(turn['Tile'])
        s, _ = result
    if not turn['NewCorp'] is None and turn['NewCorp']:
        s, _ = rules.succ(s, None, turn['NewCorp'])
    if not turn['Merger'] is None:
        if rules.getActions(s, None)[0] == 'Choose Survivor':
            s, _ = rules.succ(s, None, turn['Merger']['NewCorps'][0], None)
        for p in turn['Merger']['Sales']:
            for action in p['Types']:
                s, _ = rules.succ(s, None, action)
    for share in turn['Buy']:
        if rules.getActions(s, None)[0] == 'Buy':
            s, _ = rules.succ(s, None, share)
    if turn['Call Game']:
        s, _ = rules.succ(s, None, turn['Call Game'])
    states.append(s)


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

def train(states, growth_weight, duration_weight, eta = 0.01):
    idx = 0
    while idx < len(states):
        results = corp_outlook(states, idx)
        for corp in results:
            features = feature_extractor(states[idx], corp)
            if len(states[idx]['Group'][corp]) < 11:
                revise(features, growth_weight, results[corp]['Tiles'], eta)
            revise(features, duration_weight, results[corp]['Turns'], eta)
        idx += 1
    return growth_weight, duration_weight

def revise(phi, w, y, eta):
    train_loss = (dot_product(phi, w) - y) 
    for el in w:
        w[el] -= eta * 2 * train_loss * phi[el]

def run(gw = defaultdict(float), dw = defaultdict(float)):
#   f = open('randomTrainingExamples.gam')
    f = open('examples.gam')
    i = 0
    for game in f:
        i += 1
        print("Game # {}".format(i))
        states, history = reconstruct_states(game)
        gw, dw = train(states, gw, dw, 1/math.sqrt(i))
    f.close()
    return gw, dw

if __name__ == '__main__':
    f = open('examples.gam')
    game = f.readline()
    game = f.readline()
    test = reconstruct_states(game)
    f.close()
