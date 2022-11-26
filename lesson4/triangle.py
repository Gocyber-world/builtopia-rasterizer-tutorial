import math

class Vertice:
    def __init__(self, x, y, depth=None):
        self.x = x
        self.y = y
        self.depth = depth

    def __add__(self, other):
        if isinstance(other, Vertice):
            return Vertice(self.x + other.x, self.y + other.y, self.depth + other.depth)

    def __mul__(self, other):
        if isinstance(other, float):
            return Vertice(self.x*other, self.y*other, self.depth*other)

    def round(self):
        self.x, self.y = int(self.x), int(self.y)

class Triangle:
    def __init__(self, a: Vertice, b: Vertice, c: Vertice) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.calc_max_edge(a, b, c)

    def calc_max_edge(self, a: Vertice, b: Vertice, c: Vertice) -> None:
        self.max_edge = max(self.length(a, b), self.length(b, c), self.length(c, a))

    def length(self, start: Vertice, end: Vertice) -> float:
        vec = (end.x - start.x, end.y - start.y)
        return math.sqrt(vec[0]*vec[0] + vec[1]*vec[1])

    def get_vertice(self, p: float, q: float) -> Vertice:
        vertice = self.a*p + self.b*q + self.c*(1 - p - q)
        vertice.round()
        return vertice

class Mesh:
    def __init__(self, name: str, primitives: list, translation: list, scale: list) -> None:
        self.name = name
        self.primitives = primitives
        self.translation = [0, 0, 0] if translation is None else translation
        self.scale = [1, 1, 1] if scale is None else scale

class Primitive:
    def __init__(self) -> None:
        self.vertices = []
        self.normals = []
        self.uvs = []
        self.indices = []
        self.material = PBRMaterial()

class PBRMaterial:
    def __init__(self) -> None:
        self.color = [255, 255, 255]
        self.texture = None
