import math

def get_distance(n1, n2):
    return math.sqrt((n1[0]-n2[0])**2 + (n1[1]-n2[1])**2)

def ccw(a, b, c):
    return (c[1] - a[1]) * (b[0]-a[0]) > (b[1] - a[1]) * (c[0] - a[0])

def orientation(a, b, c, d):
    return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)

def overlap1d(seg1, seg2):
    return seg1[1] > seg2[0] and seg2[1] > seg1[0]

def overlap2d(p1, q1, p2, q2):
    b1 = [(min(p1[0], q1[0]), max(p1[0], q1[0])), (min(p1[1], q1[1]), max(p1[1], q1[1]))]
    b2 = [(min(p2[0], q2[0]), max(p2[0], q2[0])), (min(p2[1], q2[1]), max(p2[1], q2[1]))]
    return overlap1d(b1[0], b2[0]) and overlap1d(b1[1], b2[1])

def intersect(e1, e2):
    p1, q1 = e1[0], e1[1]
    p2, q2 = e2[0], e2[1]
    return overlap2d(p1, q1, p2, q2) and orientation(p1, q1, p2, q2)

def inside_polygon(p, poly):
    # Ray casting algorithm
    # https://en.wikipedia.org/wiki/Point_in_polygon
    x, y = p[0], p[1]
    n = len(poly)
    count = 0
    p1x, p1y = poly[0]
    for i in range(n+1):
        p2x, p2y = poly[i % n]
        y_min = min(p1y, p2y)
        y_max = max(p1y, p2y)
        x_max = max(p1x, p2x)
        if (y_min < y < y_max) and x < x_max:
            if p1y != p2y:
                x_int = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
            if p1x == p2x or x == x_int:
                count += 1
        p1x, p1y = p2x, p2y
    return (count % 2) == 1

def get_obstacle_edges(obstacles):
    edges = []
    for vertices in obstacles:
        for i in range(len(vertices)-1):
            edges.append((vertices[i], vertices[i+1]))
        edges.append((vertices[-1], vertices[0]))
    return edges