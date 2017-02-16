import random

def randomchoice(choices):
    if not isinstance(choices, list) and not isinstance(choices, tuple):
        return -1

    if len(choices) == 0:
        return -1

    if isinstance(choices, int):
        return random.choice(choices)
    
    total = 0
    for c in choices:
        if len(c) != 2:
            return -1
        total += c[0]

    v = random.uniform(0, total)
    for c in choices:
        v -= c[0]
        if v < 0:
            return c[1]

    # failsafe
    return choices[-1][1]
