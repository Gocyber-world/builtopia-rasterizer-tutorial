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
        self.z = np.array([0, 0, 1])
        self.calc_bbox(a, b, c)
        self.calc_loop_vec(a, b, c)

    def calc_bbox(self, a: Vertice, b: Vertice, c: Vertice):
        self.minx = min(a.x, b.x, c.x)
        self.miny = min(a.y, b.y, c.y)
        self.maxx = max(a.x, b.x, c.x)
        self.maxy = max(a.y, b.y, c.y)

    def calc_loop_vec(self, a: Vertice, b: Vertice, c: Vertice):
        self.ab = self.vec3(a, b)
        self.bc = self.vec3(b, c)
        self.ca = self.vec3(c, a)

    def vec3(self, start: Vertice, end: Vertice):
        return (end.x - start.x, end.y - start.y, 0)

    def contains(self, point: Vertice):
        sign1 = np.dot(self.z, self.cross3(self.ab, self.vec3(self.a, point))) > 0
        sign2 = np.dot(self.z, self.cross3(self.bc, self.vec3(self.b, point))) > 0
        sign3 = np.dot(self.z, self.cross3(self.ca, self.vec3(self.c, point))) > 0

        return (sign3 == sign2) and (sign2 == sign1)

    def cross3(self, left, right):
        x = (left[1] * right[2]) - (left[2] * right[1])
        y = (left[2] * right[0]) - (left[0] * right[2])
        z = (left[0] * right[1]) - (left[1] * right[0])
        return (x, y, z)