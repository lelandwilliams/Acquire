from featureExtractor import *
import random, subprocess, sys, math
import model, rules


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

def test(states, growth_weight, duration_weight ):
    growth_tests = 0
    duration_tests = 0
    duration_error = 0
    growth_error = 0
    for idx in range(len(states)):
        results = corp_outlook(states, idx)
        for corp in results:
            growth_tests += 1
            features = feature_extractor(states[idx], corp)
            if len(states[idx]['Group'][corp]) < 11:
                duration_tests += 1
                duration_error += (dot_product(features, duration_weight) - results[corp]['Turns']) **2
            growth_error += (dot_product(features, growth_weight) - results[corp]['Tiles']) **2
        idx += 1
    return growth_error/growth_tests, duration_error/duration_tests

def train(states, growth_weight, duration_weight, eta = 0.0001):
    idx = 0
    while idx < len(states):
        results = corp_outlook(states, idx)
        for corp in results:
            features = feature_extractor(states[idx], corp)
            if len(states[idx]['Group'][corp]) < 11:
                revise(features, duration_weight, results[corp]['Turns'], eta)
            revise(features, growth_weight, results[corp]['Tiles'], eta)
        idx += 1
    return growth_weight, duration_weight

def revise(phi, w, y, eta):
    train_loss = (dot_product(phi, w) - y) 
    for el in w:
        w[el] -= eta * 2 * train_loss * phi[el]

def run(gw = defaultdict(float), dw = defaultdict(float)):
    f = open('randomTrainingExamples1.gam')
    total_training_sets = 0
    training_runs = 0
    testing_runs = 0
    growth_error_sum = 0
    duration_error_sum = 0
    for game in f:
        states, history = reconstruct_states(game)
        print("\rGame # {}".format(training_runs + testing_runs), end = "")
        if training_runs < 700:
            total_training_sets += 1
            training_runs += 1
            gw, dw = train(states, gw, dw)
        else:
            testing_runs += 1
            results= test(states, gw, dw)
            growth_error_sum += results[0]
            duration_error_sum += results[1]
    f.close()
    print("\ngrowth_error = {}, duration_error = {}".format(growth_error_sum, duration_error_sum)) 
    return gw, dw, growth_error_sum, duration_error_sum

if __name__ == '__main__':
    f = open('weights.gam','r')
    gw = eval(f.readline())
    dw = eval(f.readline())
    f.close()

    gw, dw, ge, de = run(gw, dw)

    f = open('weights.gam','w')
    f.write("{}\n{}\n".format(dict(gw), dict(dw)))
    f.close()
