import math

class Vertice:
    def __init__(self, x, y, depth=None):
        self.x = x
        self.y = y
        self.depth = depth

class Triangle:
    def __init__(self, a: Vertice, b: Vertice, c: Vertice) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.calc_max_edge(a, b, c)

    def calc_max_edge(self, a: Vertice, b: Vertice, c: Vertice) -> None:
        self.max_edge = max(self.length(a, b), self.length(b, c), self.length(c, a))

    def length(self, start: Vertice, end: Vertice):
        vec = (end.x - start.x, end.y - start.y)
        return math.sqrt(vec[0]*vec[0] + vec[1]*vec[1])

    def get_vertice(self, p, q):
        x = int(p*self.a.x + q*self.b.x + (1 - p - q)*self.c.x)
        y = int(p*self.a.y + q*self.b.y + (1 - p - q)*self.c.y)
        depth = p*self.a.depth + q*self.b.depth + (1 - p - q)*self.c.depth
        return Vertice(x, y, depth)