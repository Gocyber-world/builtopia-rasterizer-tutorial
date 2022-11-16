import numpy as np
from PIL import Image
from gltf_loader import GltfLoader
from camera import Camera
from triangle import Vertice, Triangle
from depth_manager import DepthManager

class Rasterizer:
    def __init__(self, width: int, height: int, scale: int, camera: Camera, file: str) -> None:
        self.width = width
        self.height = height
        self.scale = scale
        self.camera = camera
        loader = GltfLoader()
        self.primitives = loader.load(file)
        self.color_map = np.zeros((self.height, self.width, 3), np.uint8)
        self.depth_manager = DepthManager(width, height)

    def draw_primitives(self) -> Image:
        for primitive in self.primitives:
            positions = self.generate_pixel_positions(primitive["vertices"])
            self.depth_manager.calc_depth_ratio()
            indices = primitive["indices"]
            self.draw_triangles(positions, indices)

        return Image.fromarray(self.color_map, 'RGB')

    def generate_pixel_positions(self, positions: list) -> list:
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
            self.depth_manager.add_depth(depth)

        return pixel_positions

    def draw_triangles(self, positions: list, indices: list) -> None:
        for i in range(0, len(indices), 3):
            a = positions[indices[i]]
            b = positions[indices[i + 1]]
            c = positions[indices[i + 2]]
            # self.draw_triangle_outline(Triangle(a, b, c))
            self.draw_triangle(Triangle(a, b, c))

    def draw_triangle(self, triangle: Triangle) -> None:
        # use barycentric coordinates
        step = 1.0/triangle.max_edge
        for p in np.arange(0, 1, step):
            # handle boundary
            self.draw_triangle_pixel(triangle, p, 1 - p)
            for q in np.arange(0, 1 - p, step):
                self.draw_triangle_pixel(triangle, p, q)

    def draw_triangle_pixel(self, triangle: Triangle, p: float, q: float) -> None:
        point = triangle.get_vertice(p, q)
        if self.depth_manager.override(point):
            color = self.depth_manager.get_color(point)
            self.draw_pixel(point.x, point.y, color)

    def draw_triangle_outline(self, triangle: Triangle) -> None:
        color_white = (255, 255, 255)
        self.draw_line(triangle.a, triangle.b, color_white)
        self.draw_line(triangle.b, triangle.c, color_white)
        self.draw_line(triangle.c, triangle.a, color_white)

    def draw_line(self, start: Vertice, end: Vertice, color: tuple) -> None:
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

    def draw_pixel(self, x: int, y: int, color: tuple) -> None:
        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return

        self.color_map[y][x] = color
