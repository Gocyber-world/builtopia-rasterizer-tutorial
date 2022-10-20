import math

class Vec3:

    def __str__(self):
        return f'Vec3(x:{self.x},y:{self.y},z:{self.z})'

    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z
        self.isVec3 = True

    def set(self, **kwargs):
        self.x = kwargs.get('x') or self.x
        self.y = kwargs.get('y') or self.y
        self.z = kwargs.get('z') or self.z
        return self

    def add(self, v):
        self.x += v.x
        self.y += v.y
        self.z += v.z
        return self

    def addS(self, s):
        self.x += s
        self.y += s
        self.z += s
        return self
    
    def sub(self, v):
        self.x -= v.x
        self.y -= v.y
        self.z -= v.z
        return self

    def subS(self, s):
        self.x -= s
        self.y -= s
        self.z -= s
        return self

    def mul(self, v):
        self.x *= v.x
        self.y *= v.y
        self.z *= v.z
        return self

    def mulS(self, s):
        self.x *= s
        self.y *= s
        self.z *= s
        return self

    def div(self, v):
        self.x /= v.x
        self.y /= v.y
        self.z /= v.z
        return self

    def divS(self, s):
        self.x /= s
        self.y /= s
        self.z /= s
        return self

    def copy(self, v):
        self.x = v.x
        self.y = v.y
        self.z = v.z
        return self

    def clone(self):
        return Vec3(self.x, self.y, self.z)

    def dot(self, v):
        return self.x * v.x + self.y * v.y + self.z * v.z

    def cross(self, v):
        lx = self.x
        ly = self.y
        lz = self.z
        rx = v.x
        ry = v.y
        rz = v.z
        x = ly * rz - ry * lz
        y = lz * rx - rz * lx
        z = lx * ry - rx * ly
        return Vec3(x, y, z)

    def distance(self, v):
        x = self.x - v.x
        y = self.y - v.y
        z = self.z - v.z
        return math.sqrt(x*x + y*y + z*z)

    def __add__(self, v):
        if isinstance(v, Vec3):
            x = self.x + v.x
            y = self.y + v.y
            z = self.z + v.z
            return Vec3(x, y, z)
        elif isinstance(v, int) or isinstance(v, float):
            x = self.x + v
            y = self.y + v
            z = self.z + v
            return Vec3(x, y, z)
        

    def __sub__(self, v):
        if isinstance(v, Vec3):
            x = self.x - v.x
            y = self.y - v.y
            z = self.z - v.z
            return Vec3(x, y, z)
        elif isinstance(v, int) or isinstance(v, float):
            x = self.x - v
            y = self.y - v
            z = self.z - v
            return Vec3(x, y, z)

    def toList(self):
        return [self.x, self.y, self.z]

    def length(self):
        x = self.x
        y = self.y
        z = self.z
        return math.sqrt(x*x + y*y + z*z)

    def normalize(self):
        l = self.length()
        l = 1 if l == 0 else l
        return self.divS(l)

    def floor(self):
        self.x = math.floor(self.x)
        self.y = math.floor(self.y)
        self.z = math.floor(self.z)
        return self

    def applyMat4(self, m):
        d = m.data
        x = self.x
        y = self.y
        z = self.z
        w = (d[3]*x + d[7]*y + d[11]*z + d[15])
        self.x = (d[0]*x + d[4]*y + d[8]*z + d[12]) / w
        self.y = (d[1]*x + d[5]*y + d[9]*z + d[13]) / w
        self.z = (d[2]*x + d[6]*y + d[10]*z + d[14]) / w
        return self