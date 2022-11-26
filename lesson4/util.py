import math

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

    def set_texture(self, texture) -> None:
        self.texture_width, self.texture_height = texture.size
        self.texture = texture.load()

class Vertice:
    def __init__(self, x, y, depth) -> None:
        self.x, self.y, self.depth = x, y, depth
        self.u = self.v = None

    def __add__(self, other):
        vertice = Vertice(self.x + other.x, self.y + other.y, self.depth + other.depth)
        if self.u is not None and other.u is not None:
            vertice.u, vertice.v = self.u + other.u, self.v + other.v
        return vertice

    def __mul__(self, other):
        vertice = Vertice(self.x*other, self.y*other, self.depth*other)
        if self.u is not None:
            vertice.u, vertice.v = self.u*other, self.v*other
        return vertice

    def set_uv(self, uv: list, material: PBRMaterial) -> None:
        self.u = uv[0] * (material.texture_width - 1)
        self.v = uv[1] * (material.texture_height - 1)

    def round(self) -> None:
        self.x, self.y = int(self.x), int(self.y)
        if self.u is not None:
            self.u, self.v = int(self.u), int(self.v)

class Triangle:
    def __init__(self, positions: list, indice: list, uvs: list, material: PBRMaterial) -> None:
        i, j, k = indice
        self.a, self.b, self.c = positions[i], positions[j], positions[k]
        self.calc_max_edge(self.a, self.b, self.c)
        self.material = material
        if material.texture is not None:
            self.a.set_uv(uvs[i], material)
            self.b.set_uv(uvs[j], material)
            self.c.set_uv(uvs[k], material)

    def calc_max_edge(self, a: Vertice, b: Vertice, c: Vertice) -> None:
        self.max_edge = max(self.length(a, b), self.length(b, c), self.length(c, a))

    def length(self, start: Vertice, end: Vertice) -> float:
        vec = (end.x - start.x, end.y - start.y)
        return math.sqrt(vec[0]*vec[0] + vec[1]*vec[1])

    def get_vertice(self, p: float, q: float) -> Vertice:
        vertice = self.get_pos_interp(p, q)
        if self.material.texture is not None:
            self.get_uv_interp(p, q, vertice)
        vertice.round()
        return vertice, self.get_color(vertice)

    def get_pos_interp(self, p: float, q: float) -> Vertice:
        x = self.interpolation(p, q, self.a.x, self.b.x, self.c.x)
        y = self.interpolation(p, q, self.a.y, self.b.y, self.c.y)
        depth = self.interpolation(p, q, self.a.depth, self.b.depth, self.c.depth)
        return Vertice(x, y, depth)

    def get_uv_interp(self, p: float, q: float, vertice: Vertice) -> None:
        vertice.u = self.interpolation(p, q, self.a.u, self.b.u, self.c.u)
        vertice.v = self.interpolation(p, q, self.a.v, self.b.v, self.c.v)

    def interpolation(self, p: float, q: float, i: float, j: float, k: float) -> float:
        return i*p + j*q + k*(1 - p - q)

    def get_color(self, vertice: Vertice) -> list:
        texture = self.material.texture
        if texture is not None:
            return texture[vertice.u, vertice.v]
        return self.material.color