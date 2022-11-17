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
            self.draw_triangle(a, b, c)

    def find_min(self, a, b, c):
        x = min(a[0], b[0], c[0])
        y = min(a[1], b[1], c[1])
        return (x,y)
    
    def find_max(self, a, b, c):
        x = max(a[0], b[0], c[0])
        y = max(a[1], b[1], c[1])
        return (x,y)


    def is_inside_triangle(self, t, a, b, c):
        massCenter = self.calc_mass_center(a,b,c,t)
        return (massCenter[0] >= 0) and (massCenter[1] >= 0) and (massCenter[2] >= 0)
        
    
    def draw_triangle(self, a, b, c):
        # TODO: Optimize!!
        min = self.find_min(a, b, c)
        max = self.find_max(a, b, c)
        for x in range(min[0], max[0]):
            for y in range(min[1], max[1]):
                if self.is_inside_triangle((x, y), a, b, c):
                    old_depth = self.depth_map[y][x]
                    w = self.calc_mass_center(a,b,c,(x, y))
                    depth = w[0] * a[2] + w[1] * b[2] + w[2] * c[2]
                    colorValue = 255 + depth * 50
                    color = [colorValue,colorValue,colorValue]
                    if -depth < old_depth:
                        self.draw_pixel((x,y), color)
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

    # 质心方程
    def calc_mass_center(self,p1,p2,p3,p):
      if(((p2[1] - p3[1]) * (p1[0] - p3[0]) + (p3[0] - p2[0]) * (p1[1] - p3[1]) )):
        w1 = ( (p2[1] - p3[1]) * (p[0] - p3[0]) + (p3[0] - p2[0]) * (p[1] - p3[1]))/ ((p2[1] - p3[1]) * (p1[0] - p3[0]) + (p3[0] - p2[0]) * (p1[1] - p3[1]) )
        w2 = ( (p3[1] - p1[1]) * (p[0] - p3[0]) + (p1[0] - p3[0]) * (p[1] - p3[1]))/ ((p2[1] - p3[1]) * (p1[0] - p3[0]) + (p3[0] - p2[0]) * (p1[1] - p3[1]) )
        w3 = 1 - w1 - w2
      else:
        # TODO: 三角形一条边垂直平面的权重
        return [1/3,1/3,1/3]
      return [w1,w2,w3]
    
    