import math
from model import *
from collections import defaultdict

def dot_product(phi, w):
    for i in w:
        _ = phi[i]
    s = 0
    for i in phi:
        s += phi[i] * w[i]
    return s

def feature_extractor(state, corpname, f_rational = True):
    cur_player = state['Turn']['Player']
    phi = defaultdict(float)
    corp_size = len(state['Group'][corpname])

    # Find nearby larger or smaller/equal corporations
    gn = neighborDistances(state, corpname)
    for i in range(1, len(gn)):
        for g in gn[i]:
            if g in corporations and state['Group'][g] > state['Group'][corpname]\
                    and corp_size < 11:
                phi["dist{}largercorp".format(i)] += 1
            elif g in corporations and state['Group'][g] <= state['Group'][corpname]:
                phi["dist{}smallercorp".format(i)] += 1
            elif g not in corporations:
                phi["AnonDist{}".format(i)] += 1

    # Add in the number of tiles that could potentially
    # (if improbably) be added onto the company
    fn = freeNeighbors(state, state['Group'][corpname])
    for i in range(1, len(fn)):
        if len(fn[i]):
            phi["dist{}freetiles".format(i)] = len(fn[1])

    # The size of the corporation
    phi['Size{}'.format(corp_size)] = 1
    if f_rational:
        phi['Safety'] = min(11, corp_size)/11.0
    else:
        phi['Size{}'.format(corp_size)] = 1

    phi['GameLeft'] = (80-num_turns(state))/80.0

    return phi

def placementOutcome(state, tiles):
    outcomes = dict()
    for tile in tiles:
        outcomes[tile] = 'None' # Indicates the tile causes no effects
        nb = neighbors(tile)
        for n in nb:
            for g in state['Group']:
                if n in state['Group'][g] and g in corporations and outcomes[tile] == 'add':
                    outcomes[tile] = 'merger'
                elif tile in state['Group'][g] and g in corporations and outcomes[tile] == 'None':
                    outcomes[tile] = 'add'
                elif tile in state['Group'][g] and g in corporations and outcomes[tile] == 'merger':
                    outcomes[tile] = 'merger'
                elif tile in state['Group'][g] and g in corporations and outcomes[tile] == 'illegal':
                    outcomes[tile] = 'add'
                elif tile in state['Group'][g] and g in corporations and outcomes[tile] == 'found':
                    outcomes[tile] = 'add'
                elif tile in state['Group'][g] and outcomes[tile] == 'None'\
                        and sum([int(len(state['Group'][c]) > 0) for c in corporations]) == 7:
                    outcomes[tile] = 'illegal'
                elif tile in state['Group'][g] and outcomes[tile] == 'None':
                    outcomes[tile] = 'found'
    return outcomes


def neighbors(tile):
    if not type(tile) is tuple:
        print(tile)
    assert(type(tile) is tuple)
    n = list()
    num = int(tile[0])
    let = tile[1]
    if num + 1 <= 12:
        n.append((num+1, let))
    if num -1 > 0:
        n.append((num -1, let))
    if chr(ord(let) +1) <= 'I':
        n.append((num, chr(ord(let) +1)))
    if chr(ord(let) -1) >= 'A':
        n.append((num, chr(ord(let) -1)))
    return n

def allneighbors(tile):
    """ returns all the tiles that are n-distance away from tile,
    where n is the index of the resulting array """
    return allGroupNeighbors({tile})

def allGroupNeighbors(g):
    """ returns a list of possible n-dist neighbors 
    of a group on an otherwise empty board """
    n = [set(g)]
    i = 0
    while len(n[-1]) > 0:
        new_neighbors = set()
        for t in n[i]:
            for neighbor in neighbors(t):
                new_neighbors.add(neighbor)
        new_neighbors -= n[i]
        if i >= 1:
            new_neighbors -= n[i-1]
        n.append(new_neighbors)
        i += 1
    return n

def groupNeighbors(state, g_name):
    """ provides all the immediate neighbors of a group """
    n = set()
    for tile in state['Group'][g_name]:
        for nb in neighbors(tile):
            n.add(nb)
    return n.difference(set(state['Group'][g_name]))

def neighborDistances(state, c_name):
    """ Provides a list of lists, with each list a set of corporations
    whose minimum distance to this one is the index of the list
    For example, c_name itself will end up in a list at index 0 """
    n = list()
    corps = dict()
    for c in state['Group']:
        if len(state['Group'][c]):
            corps[c] = groupNeighbors(state, c).union(set(state['Group'][c]))

    an = allGroupNeighbors(state['Group'][c_name])
    i = 0
    while len(corps.keys()) > 0:
        clist = list()
        for c in corps:
            if len(corps[c].intersection(an[i])):
                clist.append(c)
        for c in clist:
            corps.pop(c)
        n.append(clist)
        i += 1
    return n

def freeNeighbors(state, g):
    """This function provides a list of the neighbors of a
    group  at various distances that do not have a member 
    of a corporate tile group as a neighbor"""
    n = [set(g)]
    c_tiles = set()
    for c in corporations:
        c_tiles = c_tiles.union(set(state['Group'][c]))
        c_tiles = c_tiles.union(groupNeighbors(state, c))

    while len(n[-1]) > 0:
        n1_set = set()
        for t in n[-1]:
            for n1 in neighbors(t):
                if not (n1 in c_tiles):
                    n1_set.add(n1)
        for innerset in n[:-1]:
            n1_set -= innerset
        n.append(n1_set)
    return n


def num_turns(state):
    return sum([len(state['Group'][x]) for x in state['Group']])

def num_rounds(state):
    return math.ceil(num_turns(state)/(len(state['Players']) -1))


if __name__ == "__main__":
    tile = (4, 'D')
    s,h, = read_state()
