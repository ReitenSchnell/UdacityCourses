def successors(x, y, X, Y):
    if (x > X) or (y > Y):
        raise BaseException('Too much for the glass')
    return {((0, y + x) if y + x <= Y else (x - (Y-y), Y)):'X->Y',
            ((x + y, 0) if y + x <= X else (X, y - (X-x))):'Y->X',
            (x, Y):'Fill Y',
            (X, y):'Fill X',
            (x, 0):'Empty Y',
            (0, y):'Empty X',
    }

def pour_problem(X, Y, goal, start = (0,0)):
    if goal in start:
        return start
    explored = set()
    frontier = [[start]]
    while frontier:
        path = frontier.pop(0)
        (x, y) = path[-1]
        for (state, action) in successors(x, y, X, Y).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if goal in state:
                    return path2
                else:
                    frontier.append(path2)
    return Fail

Fail = []

print pour_problem(5, 9, 8)
