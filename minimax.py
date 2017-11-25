from rules import *
import random


def new_node(a, s, h):
    node = dict()
    node['s'] = s
    node['h'] = h
    node['Type'] = 'max'
    if a is None :
        node['action'] = None
        node['actions'] = []
    else:
        node['action'] = a[-1][0]
        node['actions'] = a[-1]
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
    timeline.append(new_node(a, s, h))

def bore(timeline):
    while not timeline[-1]['action'] is None:
        step(timeline)
    timeline[-1]['scores'].append(model.netWorth('Max',timeline[-1]['s']))
    print("{}: $ {}".format('Max', model.netWorth('Max',timeline[-1]['s'])))

def backtrack(timeline):
    if len(timeline) < 2:
        return
    node = timeline[-2]
    if timeline[-1]['Type'] == 'max':
        node['scores'].append(max(timeline[-1]['scores']))
    else:
        node['scores'].append(min(timeline[-1]['scores']))
    del(timeline[-1])
    if len(node['actions']):
        node['action'] = node['actions'].pop()
        if node['action'] == 'No':
            backtrack(timeline)
        else:
            bore(timeline)
        
players = ['Max', 'Min1', 'Min2', 'Min3']
s,h = new_game(players, shuffle = True)
timeline = []

timeline.append(new_node(getActions(s,h), s, h))
bore(timeline)
while len(timeline[0]['actions']) > 1:
    backtrack(timeline)
