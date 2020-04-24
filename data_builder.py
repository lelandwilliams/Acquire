from featureExtractor import *
import random, subprocess, sys, math
import model, rules
import pandas as pd


def reconstruct_states(game):
    state, history = eval(game)
    history.append(state['Turn'])
    players = [p for p in state['Players'] if p != 'Bank']
    seed = state['Seed']
    cur_state, hand = rules.new_game(players, True, seed)

    states = [cur_state]

    for turn in history[:2]:
        cur_state = step(cur_state, turn)
#       print(cur_state)
        for player in players:
            p = cur_state['Players'][player]
            turns = pd.DataFrame(columns=["GameNum", "Turn", "Player", "Player_Type", "Is_Turn", "Money", "Hand", "Tower", "Luxor", "American", "Worldwide", "Festival", "Continental", "Imperial"])

#   return states, history

def step(state, turn):
    """ step() is the heavy lifter of game data analysis.
    It takes in the current game state, and a turn from history. It replays a
    game turn, and returns the games state after all the actions have been accounted for.

    Currently, it ignores changes in hands, but that might be worth changing later.
    """
    s = state
    print(s)
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
    return s


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

def setup():
    fname = "data/randomTrainingExamples1.gam"
    column_list = ["GameNum", "Turn", "Player", \
                   "Player_Type", "Is_Turn", \
                   "Money", "Hand", "Tower", \
                   "Luxor", "American", "Worldwide", \
                   "Festival", "Continental", "Imperial"]
#   turns = pd.DataFrame(columns=column_list)
    game_num = 0
    turn_num = 0
    turn_table = None

    f = open(fname)
#   for _ in range(1):
    game = f.readline()
    for game in f:
        state, history = eval(game)
        history.append(state['Turn'])
        players = [p for p in state['Players'] if p != 'Bank']
        seed = state['Seed']
        cur_state, hand = rules.new_game(players, True, seed)
        turns = []
        states = [cur_state]

        for turn in history[:15]:
            cur_state = step(cur_state, turn)
            for player in players:
                turn = {}
                turn["GameNum"] = game_num
                turn["Turn"] = turn_num
                turn["Player"] = player
                turn["money"] = cur_state['Players'][player]['money']
                turn["Player_Type"] = cur_state['Players'][player]['playerType']
                turn["Tower"] = cur_state['Players'][player]['Tower']
                turn["Luxor"] = cur_state['Players'][player]['Luxor']
                turn["American"] = cur_state['Players'][player]['American']
                turn["Worldwide"] = cur_state['Players'][player]['Worldwide']
                turn["Festival"] = cur_state['Players'][player]['Festival']
                turn["Continental"] = cur_state['Players'][player]['Continental']
                turn["Imperial"] = cur_state['Players'][player]['Imperial']
                turn["Is_Turn"] = (player == cur_state['Turn']['Player'])
                turn["Hand"] = None
                turns.append(turn)
            turn_num += 1

        if turn_table is None:
            turn_table = pd.DataFrame(turns)

        print(turn_table)



if __name__ == '__main__':
    setup()
#   f = open('weights.gam','r')
#   gw = eval(f.readline())
#   dw = eval(f.readline())
#   f.close()

#   gw, dw, ge, de = run(gw, dw)

#   f = open('weights.gam','w')
#   f.write("{}\n{}\n".format(dict(gw), dict(dw)))
#   f.close()
