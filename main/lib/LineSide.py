from .FindLineEq import line_equation


def DiagonalSide(p1, p2, p3):
    a, b = line_equation(p1, p2)
    projection = a*p3['x']+b
    residual = p3['y']-projection

    if residual > 0:
        return 1
    if residual < 0:
        return -1
    return 0
    # return [(a*x)+b for x in range((p1['x']-10), (p2['x']+10))]


def HorizontalSide(line, price):
    if line < price:
        return 1
    if line > price:
        return -1
    return 0
