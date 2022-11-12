import numpy as np

class Vertice:
    def __init__(self, x, y, depth=None):
        self.x = x
        self.y = y
        self.depth = depth

class Triangle:
    def __init__(self, a: Vertice, b: Vertice, c: Vertice):
        self.a = a
        self.b = b
        self.c = c
        self.calc_bbox(a, b, c)
        self.calc_loop_vec(a, b, c)

    def calc_bbox(self, a: Vertice, b: Vertice, c: Vertice):
        self.minx = min(a.x, b.x, c.x)
        self.miny = min(a.y, b.y, c.y)
        self.maxx = max(a.x, b.x, c.x)
        self.maxy = max(a.y, b.y, c.y)

    def calc_loop_vec(self, a: Vertice, b: Vertice, c: Vertice):
        self.ab = self.vec(a, b)
        self.bc = self.vec(b, c)
        self.ca = self.vec(c, a)

    def contains(self, point: Vertice):
        sign1 = self.cross(self.ab, self.vec(self.a, point)) > 0
        sign2 = self.cross(self.bc, self.vec(self.b, point)) > 0
        sign3 = self.cross(self.ca, self.vec(self.c, point)) > 0

        return (sign3 == sign2) and (sign2 == sign1)

    def vec(self, start: Vertice, end: Vertice):
        return (end.x - start.x, end.y - start.y)

    def cross(self, left, right):
        return (left[0] * right[1]) - (left[1] * right[0])