import numpy as np
from PIL import Image
from gltfLoader import GltfLoader
from camera import Camera
import random

COLOR_WHITE = (255,255,255)

class Rasterizer:
    def __init__(self, width, height, scale, camera: Camera, file):
        self.width = width
        self.height = height
        self.scale = scale
        self.camera = camera
        loader = GltfLoader()
        self.max_depth = float('-inf')
        self.min_depth = float('-inf')
        self.depth_points = list()
        self.primitives = loader.load(file)
        self.rgbs = np.zeros(self.width * self.height * 3, np.uint8).reshape(self.height, self.width, 3)
        self.depth_map = np.zeros(self.width * self.height, np.float32).reshape(self.height, self.width)
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.depth_map[y][x] = 1000

    def draw_primitives(self):
        for primitive in self.primitives:
            positions = self.generate_pixel_positions(primitive["vertices"])
            indices = primitive["indices"]
            self.draw_triangles(positions, indices)
        for pos in self.depth_points:
            color = int(255 + (pos[2] - self.max_depth) * 255/abs(self.max_depth - self.min_depth))
            self.draw_pixel((pos[0], pos[1]), color)
        return Image.fromarray(self.rgbs, 'RGB')

    def generate_pixel_positions(self, positions):
        pixel_positions = []
        projection_matrix = self.camera.get_perspective().transpose()
        for pos in positions:
            pos.append(1)   # [x, y, z] -> [x, y, z, 1]
            camera_pos = np.matmul(pos, projection_matrix)

            # fit points to canvas
            x, y = camera_pos[0]/camera_pos[3], camera_pos[1]/camera_pos[3]
            depth = camera_pos[2]

            px = (int)(x * self.scale + self.width/2)
            py = (int)(-1 * y * self.scale + self.height/2)
            pixel_positions.append((px, py, depth))

        return pixel_positions

    def draw_triangles(self, positions, indices):
        for i in range(0, len(indices), 3):
            a = positions[indices[i]]
            b = positions[indices[i + 1]]
            c = positions[indices[i + 2]]
            #self.draw_line(a, b)
            #self.draw_line(b, c)
            #self.draw_line(c, a)
            avg_depth = (a[2] + b[2] + c[2])/3
            color_value = int(255 + avg_depth * 30)
            color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            self.draw_triangle(a, b, c, color, avg_depth)

    def find_min(self, a, b, c):
        x = min(a[0], b[0], c[0])
        y = min(a[1], b[1], c[1])
        return (x,y)
    
    def find_max(self, a, b, c):
        x = max(a[0], b[0], c[0])
        y = max(a[1], b[1], c[1])
        return (x,y)

    def sign(self, t, a, b):
        # TODO: Optimize!!
        # axis z
        z = np.array([0,0,1])
        # vector ab
        v1 = np.array([b[0] - a[0], b[1] - a[1], 0])
        # vector at
        v2 = np.array([t[0] - a[0], t[1] - a[1], 0])

        return np.dot(z, np.cross(v1, v2)) > 0

    def is_inside_triangle(self, t, a, b, c):
        sign1 = self.sign(t, a, b)
        sign2 = self.sign(t, b, c)
        sign3 = self.sign(t, c, a)

        return (sign3 == sign2) and (sign2 == sign1)
        
    def barycentric(self, t, a, b, c):
        v1 = np.array([c[0] - a[0], b[0] - a[0], a[0] - t[0]])
        v2 = np.array([c[1] - a[1], b[1] - a[1], a[1] - t[1]])
        u = np.cross(v1, v2)
        if (u[2] < 1):
            return (-1, 1, 1)
        return (1 - (u[0] + u[1])/u[2], u[1]/u[2], u[0]/u[2])


    def draw_triangle(self, a, b, c, color, depth):
        # TODO: Optimize!!
        minbox = self.find_min(a, b, c)
        maxbox = self.find_max(a, b, c)
        for x in range(minbox[0], maxbox[0]):
            for y in range(minbox[1], maxbox[1]):
                pos = self.barycentric((x, y), a, b, c)
                if (pos[0] < 0 or pos[1] < 0 or pos[2] < 0):
                    continue
                old_depth = self.depth_map[y][x]
                if -depth < old_depth:
                    self.max_depth = max(self.max_depth, -depth)
                    self.min_depth = min(self.min_depth, -depth)
                    self.depth_points.append((x, y, -depth))
                    self.depth_map[y][x] = -depth

    def draw_line(self, start, end):
        startx, starty = start
        endx, endy = end

        if endx != startx:
            step = 1 if startx < endx else -1
            k = (endy - starty)/(endx - startx)
            for x in range(startx, endx, step):
                y = starty + (int)(k*(x - startx))
                self.draw_pixel((x, y), COLOR_WHITE)

        if endy != starty:
            step = 1 if starty < endy else -1
            k = (endx - startx)/(endy - starty)
            for y in range(starty, endy, step):
                x = startx + (int)(k*(y - starty))
                self.draw_pixel((x, y), COLOR_WHITE)

        self.draw_pixel((endx, endy), COLOR_WHITE)

    def draw_pixel(self, position, color):
        x, y = position
        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return

        self.rgbs[y][x] = color
