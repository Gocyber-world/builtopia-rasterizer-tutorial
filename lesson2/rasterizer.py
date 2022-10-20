import numpy as np
from PIL import Image
from load.loader import Loader
from matrix.vec3 import Vec3
from matrix.mat4 import Mat4
from enum import Enum

class Color(Enum):
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

class Rasterizer:
    def __init__(self, width, height, scale, camera, file):
        self.width = width
        self.height = height
        self.scale = scale
        self.camera = camera
        loader = Loader.create('gltf')
        self.primitives = loader.load(file)
        self.rgbs = np.zeros(self.width * self.height * 3, np.uint8).reshape(self.height, self.width, 3)

    def draw_primitives(self):
        for primitive in self.primitives:
            positions = self.generate_pixel_positions(primitive["vertices"])
            indices = primitive["indices"]
            self.draw_triangles(positions, indices)

        return Image.fromarray(self.rgbs, 'RGB')

    def generate_pixel_positions(self, positions):
        pixel_positions = []
        # projection_matrix = self.camera.get_perspective().transpose()
        for pos in positions:
            x,y,z = pos
            point = Vec3(x, y, z)
            newPoint = point.applyMat4(self.camera.worldMatrix)
            # pos.append(1)   # [x, y, z] -> [x, y, z, 1]
            # camera_pos = np.matmul(pos, projection_matrix)

            # fit points to canvas
            # x, y = camera_pos[0]/camera_pos[3], camera_pos[1]/camera_pos[3]
            x = newPoint.x
            y = newPoint.y
            px = (int)(x * self.scale + self.width/2)
            py = (int)(-1 * y * self.scale + self.height/2)
            # print(px, py)
            # viewport = Mat4().setViewport(0, 0, self.width, self.height)
            # newPoint = newPoint.applyMat4(viewport).floor()
            # px = newPoint.x
            # py = newPoint.y
            pixel_positions.append((px, py))

        return pixel_positions

    def draw_triangles(self, positions, indices):
        for i in range(0, len(indices), 3):
            a = positions[indices[i]]
            b = positions[indices[i + 1]]
            c = positions[indices[i + 2]]
            self.draw_line(a, b)
            self.draw_line(b, c)
            self.draw_line(c, a)

    def draw_line(self, start, end):
        startx, starty = start
        endx, endy = end

        if endx != startx:
            step = 1 if startx < endx else -1
            k = (endy - starty)/(endx - startx)
            for x in range(startx, endx, step):
                y = starty + (int)(k*(x - startx))
                self.draw_pixel((x, y), Color.white.value)

        if endy != starty:
            step = 1 if starty < endy else -1
            k = (endx - startx)/(endy - starty)
            for y in range(starty, endy, step):
                x = startx + (int)(k*(y - starty))
                self.draw_pixel((x, y), Color.white.value)

        self.draw_pixel((endx, endy), Color.white.value)

    def draw_pixel(self, position, color):
        x, y = position
        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return

        self.rgbs[y][x] = color
