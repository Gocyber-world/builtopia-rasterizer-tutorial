import random
import numpy as np
from PIL import Image
from gltfLoader import GltfLoader
from camera import Camera
from triangle import Vertice, Triangle

class Rasterizer:
    def __init__(self, width, height, scale, camera: Camera, file):
        self.width = width
        self.height = height
        self.scale = scale
        self.camera = camera
        loader = GltfLoader()
        self.primitives = loader.load(file)
        self.color_map = np.zeros((self.height, self.width, 3), np.uint8)
        self.depth_map = np.full((self.height, self.width), float("inf"), np.float32)

    def draw_primitives(self):
        for primitive in self.primitives:
            positions = self.generate_pixel_positions(primitive["vertices"])
            indices = primitive["indices"]
            self.draw_triangles(positions, indices)

        return Image.fromarray(self.color_map, 'RGB')

    def generate_pixel_positions(self, positions):
        pixel_positions = list()
        projection_matrix = self.camera.get_perspective().transpose()
        for pos in positions:
            pos.append(1)   # [x, y, z] -> [x, y, z, 1]
            camera_pos = np.matmul(pos, projection_matrix)   # [x', y', z', -z']

            # fit points to canvas
            x, y = camera_pos[0]/camera_pos[3], camera_pos[1]/camera_pos[3]
            px = (int)(x * self.scale + self.width/2)
            py = (int)(-1 * y * self.scale + self.height/2)

            depth = camera_pos[2]
            pixel_positions.append(Vertice(px, py, depth))

        return pixel_positions

    def draw_triangles(self, positions, indices):
        for i in range(0, len(indices), 3):
            a = positions[indices[i]]
            b = positions[indices[i + 1]]
            c = positions[indices[i + 2]]
            # self.draw_triangle_outline(Triangle(a, b, c))
            avg_depth = (a.depth + b.depth + c.depth)/3
            color_value = int(255 + avg_depth * 30)
            color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            self.draw_triangle(Triangle(a, b, c), color, avg_depth)

    def draw_triangle(self, triangle: Triangle, color, depth):
        for x in range(triangle.minx, triangle.maxx):
            for y in range(triangle.miny, triangle.maxy):
                if triangle.contains(Vertice(x, y)):
                    old_depth = self.depth_map[y][x]
                    if -depth < old_depth:
                        self.draw_pixel((x,y), color)
                        self.depth_map[y][x] = -depth

    def draw_triangle_outline(self, triangle: Triangle):
        color_white = (255, 255, 255)
        self.draw_line(triangle.a, triangle.b, color_white)
        self.draw_line(triangle.b, triangle.c, color_white)
        self.draw_line(triangle.c, triangle.a, color_white)

    def draw_line(self, start: Vertice, end: Vertice, color: Vertice):
        if end.x != start.x:
            step = 1 if start.x < end.x else -1
            k = (end.y - start.y)/(end.x - start.x)
            for x in range(start.x, end.x, step):
                y = start.y + (int)(k*(x - start.x))
                self.draw_pixel((x, y), color)

        if end.y != start.y:
            step = 1 if start.y < end.y else -1
            k = (end.x - start.x)/(end.y - start.y)
            for y in range(start.y, end.y, step):
                x = start.x + (int)(k*(y - start.y))
                self.draw_pixel((x, y), color)

        self.draw_pixel((end.x, end.y), color)

    def draw_pixel(self, position, color):
        x, y = position
        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return

        self.color_map[y][x] = color
