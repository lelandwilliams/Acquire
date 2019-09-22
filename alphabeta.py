from rules import *
import random

num_created = 0

def new_node(a, s, h, d, alpha = float('-inf'), beta = float('inf')):
    global num_created
    num_created += 1
    node = dict()
    node['s'] = s
    node['h'] = h
    node['depth'] = d
    node['alpha'] = alpha
    node['beta'] = beta
    node['Type'] = 'max'
    if a is None :
        node['action'] = None
        node['actions'] = []
    elif a[0] == 'Call': # make sure that calling the game is the only option.
        node['action'] = a[-1][0]
        node['actions'] = []
    else:
        node['action'] = a[-1][0]
        node['actions'] = a[-1][1:]
        if (len(a) == 3 and a[1] != 'Max') or (len(a) ==2\
                and s['Turn']['Player'] != 'Max'):
            node['Type'] = 'min'
    node['scores'] = list()
    return node

def sanityCheck(original, timeline):
    """ This function is mostly a test on the integrity
    of the s,h path from node to node through timeline"""
    s,h = original
    for node in timeline:
        s,h = succ(s,h,node['action'])
    return s,h

def step(timeline):
    node = timeline[-1]
    s,h = succ(node['s'], node['h'], node['action'])
    a = getActions(s,h)
    timeline.append(new_node(a, s, h, node['depth'] + 1, node['alpha'], node['beta']))

def bore(timeline):
    while not timeline[-1]['action'] is None:
        step(timeline)
    timeline[-1]['scores'].append(model.netWorth('Max',timeline[-1]['s']))
#   print("{}: $ {}".format('Max', model.netWorth('Max',timeline[-1]['s']), end=""))
    depths = depthReport(timeline)
    for d in depths:
        print(" {}: {}".format(d, depths[d]), end = "")
    print(" depth : {}".format(timeline[-1]['depth']), end = "")
    print(" visited: {}".format(num_created))


def backtrack(timeline):
    if len(timeline) < 2:
        return False
    node = timeline[-2]

    if timeline[-1]['Type'] == 'max':
        score = max(timeline[-1]['scores'])
        del(timeline[-1])
        node['scores'].append(score)
    else:
        score = min(timeline[-1]['scores'])
        del(timeline[-1])
        node['scores'].append(score)

    if node['Type'] == 'max' and score > node['alpha']:
        node['alpha'] = score
    if node['Type'] == 'min' and score < node['beta']:
        node['beta'] = score
    if node['Type'] == 'max' and score > node['beta']:
        return backtrack(timeline)
    if node['Type'] == 'min' and score < node['alpha']:
        return backtrack(timeline)

    if len(node['actions']) == 0:
        return backtrack(timeline)
    node['action'] = node['actions'].pop()
    if node['action'] == 'No':
        return backtrack(timeline)


    return True
        
def depthReport(timeline):
    depths = dict()
    for i in [8,50,96,153,236,294,344]:
        if len(timeline) > i:
            depths[i] = len(timeline[i]['actions'])
    return depths

if __name__ == "__main__":
    players = ['Max', 'Min1', 'Min2', 'Min3']
    s,h = new_game(players, shuffle = True, seed = 27)
    timeline = []

    timeline.append(new_node(getActions(s,h), s, h, 1))
    bore(timeline)
    while backtrack(timeline):
        bore(timeline)

