from .FindLineEq import line_equation
from math import ceil


def cross_size(p1, p2, p3, p4):
    a, b = line_equation(p1, p2)
    c, d = line_equation(p3, p4)
    x = (d-b)/(a-c)
    if x > p3['x'] and x < p4['x']:
        y2 = c*x+d
        return ceil(x), abs(p3['y']-y2), abs(p4['y']-y2)
    return False
