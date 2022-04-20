def line_equation(p1, p2):
    a = (p2['y']-p1['y'])/(p2['x']-p1['x'])
    b = p1['y'] - a*p1['x']
    return a, b
