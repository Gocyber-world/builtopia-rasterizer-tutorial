import numpy as np
from PIL import Image
from gltfLoader import GltfLoader
from camera import Camera

I_WIDTH = 800
I_HEIGHT = 600
I_SCALE = 200
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

    def draw_primitives(self):
        for primitive in self.primitives:
            positions = self.generate_pixel_positions(primitive["vertices"])
            indices = primitive["indices"]
            self.draw_triangles(positions, indices)

        return Image.fromarray(self.rgbs, 'RGB')

    def generate_pixel_positions(self, positions):
        pixel_positions = []
        camera_matrix = self.camera.get_matrix()
        for pos in positions:
            pos.append(1)   # [x, y, z] -> [x, y, z, 1]
            camera_pos = np.matmul(pos, camera_matrix) # translate, rotate, scale

            # fit points to canvas
            x, y = camera_pos[0], camera_pos[1]
            px = (int)(x * self.scale + self.width/2)
            py = (int)(-1 * y * self.scale + self.height/2)
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

camera = Camera()
rasterizer = Rasterizer(I_WIDTH, I_HEIGHT, I_SCALE, camera, "monkey.gltf")
rasterizer.draw_primitives().show()