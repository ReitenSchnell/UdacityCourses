import itertools
import doctest

def bsuccessors_mine(state):
    here, there, t = state
    result = {}
    light = 'light'
    light_set, current_action = (here, '->') if light in here else (there, '<-')
    people = [p for p in light_set if p!=light]
    for c in itertools.combinations(people, 1):
        if light_set == here:
            result[(frozenset([p for p in here if p not in c and p!=light]), frozenset([p for p in there]+list(c) + [light]), sum(c)+t)] = (c[0], c[0], current_action)
        if light_set == there:
            result[(frozenset([p for p in here] + list(c) + [light]), frozenset([p for p in there if p not in c and p!=light]), sum(c)+t)] = (c[0], c[0], current_action)
    return result

def bsuccessors(state):
    here, there, t = state
    light = 'light'
    if light in here:
        return dict(((here - frozenset([a,b,light]),
                    there | frozenset([a,b,light]),
                    t + max(a, b)),
                    (a,b,'->'))
                    for a in here if a is not light
                    for b in here if b is not light)
    else:
        return dict(((here | frozenset([a,b,light]),
                      there - frozenset([a,b,light]),
                      t + max(a, b)),
                     (a,b,'<-'))
                      for a in there if a is not light
                      for b in there if b is not light)


def test():
    assert bsuccessors((frozenset([1, 'light']), frozenset([]), 3)) == {
        (frozenset([]), frozenset([1, 'light']), 4): (1, 1, '->')}

    assert bsuccessors((frozenset([]), frozenset([2, 'light']), 0)) =={
        (frozenset([2, 'light']), frozenset([]), 2): (2, 2, '<-')}

    return 'tests pass'

def path_states(path):
    return path[0::2]

def path_actions(path):
    return path[1::2]

def test_path():
    testpath = [(frozenset([1, 10]), frozenset(['light', 2, 5]), 5), # state 1
        (5, 2, '->'),                                        # action 1
        (frozenset([10, 5]), frozenset([1, 2, 'light']), 2), # state 2
        (2, 1, '->'),                                        # action 2
        (frozenset([1, 2, 10]), frozenset(['light', 5]), 5),
        (5, 5, '->'),
        (frozenset([1, 2]), frozenset(['light', 10, 5]), 10),
        (5, 10, '->'),
        (frozenset([1, 10, 5]), frozenset(['light', 2]), 2),
        (2, 2, '->'),
        (frozenset([2, 5]), frozenset([1, 10, 'light']), 10),
        (10, 1, '->'),
        (frozenset([1, 2, 5]), frozenset(['light', 10]), 10),
        (10, 10, '->'),
        (frozenset([1, 5]), frozenset(['light', 2, 10]), 10),
        (10, 2, '->'),
        (frozenset([2, 10]), frozenset([1, 5, 'light']), 5),
        (5, 1, '->'),
        (frozenset([2, 10, 5]), frozenset([1, 'light']), 1),
        (1, 1, '->')]
    assert path_states(testpath) == [(frozenset([1, 10]), frozenset(['light', 2, 5]), 5), # state 1
        (frozenset([10, 5]), frozenset([1, 2, 'light']), 2), # state 2
        (frozenset([1, 2, 10]), frozenset(['light', 5]), 5),
        (frozenset([1, 2]), frozenset(['light', 10, 5]), 10),
        (frozenset([1, 10, 5]), frozenset(['light', 2]), 2),
        (frozenset([2, 5]), frozenset([1, 10, 'light']), 10),
        (frozenset([1, 2, 5]), frozenset(['light', 10]), 10),
        (frozenset([1, 5]), frozenset(['light', 2, 10]), 10),
        (frozenset([2, 10]), frozenset([1, 5, 'light']), 5),
        (frozenset([2, 10, 5]), frozenset([1, 'light']), 1)]
    assert path_actions(testpath) == [(5, 2, '->'), # action 1
        (2, 1, '->'), # action 2
        (5, 5, '->'),
        (5, 10, '->'),
        (2, 2, '->'),
        (10, 1, '->'),
        (10, 10, '->'),
        (10, 2, '->'),
        (5, 1, '->'),
        (1, 1, '->')]
    return 'tests pass'


def elapsed_time(path):
    return path[-1][2]


def bridge_problem(here):
    light = 'light'
    here = frozenset(here)|frozenset([light])
    explored = set()
    frontier = [[(here, frozenset(), 0)]]
    if not here:
        return frontier[0]
    while frontier:
        path = frontier.pop(0)
        if not path[-1][0]:
            return path
        for (state, action) in bsuccessors(path[-1]).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                frontier.append(path2)
                frontier.sort(key = elapsed_time)

    return []

def test_bridge():
    assert bridge_problem(frozenset((1, 2),))[-1][-1] == 2 # the [-1][-1] grabs the total elapsed time
    assert bridge_problem(frozenset((1, 2, 5, 10),))[-1][-1] == 17
    return 'tests pass'


