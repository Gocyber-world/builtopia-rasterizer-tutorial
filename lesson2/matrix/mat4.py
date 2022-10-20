import math


class Mat4:

    def __str__(self):
        d = self.data
        return f'''
            Mat4([{d[0]},{d[4]},{d[8]},{d[12]},
                  {d[1]},{d[5]},{d[9]},{d[13]},
                  {d[2]},{d[6]},{d[10]},{d[14]},
                  {d[3]},{d[7]},{d[11]},{d[15]}])
        '''

    def __init__(self, d = None):
        if not d:
            d = [0] * 16
            d[0],d[4],d[8],d[12] = 1, 0, 0, 0
            d[1],d[5],d[9],d[13] = 0, 1, 0, 0
            d[2],d[6],d[10],d[14] = 0, 0, 1, 0
            d[3],d[7],d[11],d[15] = 0, 0, 0, 1
        self.data = d
        
    def round(self):
        for i in range(0, len(self.data)):
            self.data[i] = round(self.data[i], 2)

    def clone(self):
        data = self.data[::]
        return Mat4(data)

    def copy(self, m):
        self.data= m.data[::]
        return self

    def set(self, data):
        self.data= data[::]
        return self

    def setIdentity(self):
        d = self.data
        d[0],d[4],d[8],d[12] = 1, 0, 0, 0
        d[1],d[5],d[9],d[13] = 0, 1, 0, 0
        d[2],d[6],d[10],d[14] = 0, 0, 1, 0
        d[3],d[7],d[11],d[15] = 0, 0, 0, 1
        return self

    def transpose(self):
        d = self.data
        n = self.data[::]
        d[0],d[4],d[8],d[12] = n[0],n[1],n[2],n[3]
        d[1],d[5],d[9],d[13] = n[4],n[5],n[6],n[7]
        d[2],d[6],d[10],d[14] = n[8],n[9],n[10],n[11]
        d[3],d[7],d[11],d[15] = n[12],n[13],n[14],n[15]

    def mul(self, m):
        sd = self.data[::]
        md = m.data
        td = self.data
        a11,a12,a13,a14 = sd[0],sd[4],sd[8],sd[12]
        a21,a22,a23,a24 = sd[1],sd[5],sd[9],sd[13]
        a31,a32,a33,a34 = sd[2],sd[6],sd[10],sd[14]
        a41,a42,a43,a44 = sd[3],sd[7],sd[11],sd[15]

        b11,b12,b13,b14 = md[0],md[4],md[8],md[12]
        b21,b22,b23,b24 = md[1],md[5],md[9],md[13]
        b31,b32,b33,b34 = md[2],md[6],md[10],md[14]
        b41,b42,b43,b44 = md[3],md[7],md[11],md[15]

        td[0] = a11 * b11 + a12 * b21 + a13 * b31 + a14 * b41
        td[4] = a11 * b12 + a12 * b22 + a13 * b32 + a14 * b42
        td[8] = a11 * b13 + a12 * b23 + a13 * b33 + a14 * b43
        td[12] = a11 * b14 + a12 * b24 + a13 * b34 + a14 * b44

        td[1] = a21 * b11 + a22 * b21 + a23 * b31 + a24 * b41
        td[5] = a21 * b12 + a22 * b22 + a23 * b32 + a24 * b42
        td[9] = a21 * b13 + a22 * b23 + a23 * b33 + a24 * b43
        td[13] = a21 * b14 + a22 * b24 + a23 * b34 + a24 * b44

        td[2] = a31 * b11 + a32 * b21 + a33 * b31 + a34 * b41
        td[6] = a31 * b12 + a32 * b22 + a33 * b32 + a34 * b42
        td[10] = a31 * b13 + a32 * b23 + a33 * b33 + a34 * b43
        td[14] = a31 * b14 + a32 * b24 + a33 * b34 + a34 * b44

        td[3] = a41 * b11 + a42 * b21 + a43 * b31 + a44 * b41
        td[7] = a41 * b12 + a42 * b22 + a43 * b32 + a44 * b42
        td[11] = a41 * b13 + a42 * b23 + a43 * b33 + a44 * b43
        td[15] = a41 * b14 + a42 * b24 + a43 * b34 + a44 * b44
        self.round()
        return self
        
    def mulS(self, s):
        for i in range(0, len(self.data)):
            self.data[i] *= s
        return self

    def setLookAt(self, position, target, up):
        z = (position - target).normalize()
        y = up.clone().normalize()
        x = y.cross(z).normalize()
        y = z.cross(x)

        d = self.data
        d[0],d[4],d[8],d[12] = x.x, x.y, x.z, 0
        d[1],d[5],d[9],d[13] = y.x, y.y, y.z, 0
        d[2],d[6],d[10],d[14] = z.x, z.y, z.z, 0
        d[3],d[7],d[11],d[15] =  0,   0,   0,   1
        
        mt = Mat4()
        md = mt.data
        md[12] = -position.x
        md[13] = -position.y
        md[14] = -position.z
        self.mul(mt)
        return self


    def setOrtho(self, left, right, top, bottom, near, far):
        d = self.data
        d[0],d[4],d[8],d[12] = 2/(right-left), 0,          0,          -(right+left)/(right-left)
        d[1],d[5],d[9],d[13] =     0,    2/(top -bottom),  0,          -(top + bottom)/(top - bottom)
        d[2],d[6],d[10],d[14] =    0,          0,      -2/(far -near), -(far + near)/(far - near)
        d[3],d[7],d[11],d[15] =    0,          0,          0,                      1
        self.round()
        return self

    def setTranslate(self, x, y, z):
        d = self.data
        d[12] = x
        d[13] = y
        d[14] = z
        return self

    def setScale(self, x, y, z):
        d = self.data
        d[0] = x
        d[5] = y
        d[10] = z
        return self

    def setViewport(self, x, y, width, height):
        d = self.data

        d[0] = width * 0.5
        d[5] = height * 0.5
        d[12] = x + width * 0.5
        d[13] = y + height * 0.5
        d[14] = 0.5
        return self

    def setFrustum(self, left, right, top, bottom, znear, zfar):
        t1 = 2 * znear
        t2 = right - left
        t3 = top - bottom
        t4 = zfar - znear

        d = self.data
        d[0],d[4],d[8],d[12] = t1/t2, 0,  (right+left)/t2,   0
        d[1],d[5],d[9],d[13] =  0,  t1/t3,(top+bottom)/t3,   0
        d[2],d[6],d[10],d[14] = 0,    0,   (-zfar-znear)/t4, (-t1 * zfar)/t4,
        d[3],d[7],d[11],d[15] = 0,    0,       -1,           0
        self.round()
        return self
    
    def setPerspective(self, fov, aspect, znear, zfar):
        top = znear * math.tan(fov * math.pi / 360)
        height = 2 * top
        width = aspect * height
        left = -0.5 * width
        right = left + width
        bottom = top - height
        
        x = 2 * znear / (right - left)
        y = 2 * znear / (top - bottom)
        
        a = (right + left) / (right - left)
        b = (top + bottom) / (top - bottom)
        c = -(zfar + znear) / (zfar - znear)
        d = -2 * zfar * znear / (zfar - znear)
        
        dd = self.data
        dd[0] = x
        dd[5] = y
        dd[8] = a
        dd[9] = b
        dd[10] = c
        dd[11] = -1
        dd[14] = d
        self.round()
        return self