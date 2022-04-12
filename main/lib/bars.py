def bar_direction(bar):
    diff = bar['close']-bar['open']
    if diff > 0:
        return 1
    elif diff < 0:
        return -1
    else:
        return 0


def doji(bar):
    if abs(bar['close']-bar['open'])/(bar['high']-bar['low']) <= .25:
        return True
    return False


def between(value, bar, body=True):
    direction = bar_direction(bar)
    if body:
        if direction > 0:
            if bar['close'] > value and bar['open'] < value:
                return True
        if direction < 0:
            if bar['close'] < value and bar['open'] > value:
                return True
    else:
        if bar['high'] > value and bar['low'] < value:
            return True
    return False


def inside_bar(outside, inside, inside_body=False):
    if not inside_body:
        if outside['high'] >= inside['high'] and outside['low'] <= inside['low']:
            return True
    else:
        direction = bar_direction(inside)
        if direction > 0:
            if outside['high'] >= inside['close'] and outside['low'] <= inside['open']:
                return True
        if direction < 0:
            if outside['high'] >= inside['open'] and outside['low'] <= inside['close']:
                return True
    return False


def gap(bar1, bar2):
    mean1 = (bar1["high"]+bar1["low"])/2
    mean2 = (bar2["high"]+bar2["low"])/2

    if mean1 <= mean2:
        if bar1["high"] < bar2["low"]:
            return True
    else:
        if bar1["low"] > bar2["high"]:
            return True

    return False
