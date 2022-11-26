import numpy as np
from PIL import Image
from gltf_loader import GltfLoader
from camera import Camera
from util import PBRMaterial, Vertice, Triangle
from depth_manager import DepthManager

class Rasterizer:
    def __init__(self, width: int, height: int, scale: int, camera: Camera, file: str) -> None:
        self.width = width
        self.height = height
        self.scale = scale
        self.camera = camera
        loader = GltfLoader()
        self.meshes = loader.load(file)
        self.color_map = np.zeros((self.height, self.width, 3), np.uint8)
        self.depth_manager = DepthManager(width, height)

    def draw_meshes(self) -> Image:
        for mesh in self.meshes:
            for primitive in mesh.primitives:
                self.draw_primitive(primitive, mesh.translation, mesh.scale)

        return Image.fromarray(self.color_map, 'RGB')

    def draw_primitive(self, primitive, translation: list, scale: list) -> list:
        vertices = [[v[i] * scale[i] + translation[i] for i in range(3)] for v in primitive.vertices]
        positions = self.generate_pixel_positions(vertices)
        indices = primitive.indices
        uvs = primitive.uvs
        self.draw_triangles(positions, indices, uvs, primitive.material)

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

        return pixel_positions

    def draw_triangles(self, positions: list, indices: list, uvs: list, material: PBRMaterial) -> None:
        for indice in [indices[i:i+3] for i in range(0, len(indices), 3)]:
            # use barycentric coordinates
            triangle = Triangle(positions, indice, uvs, material)
            step = 1.0/triangle.max_edge
            for p in np.arange(0, 1, step):
                # handle boundary
                self.draw_triangle_pixel(triangle, p, 1 - p)
                for q in np.arange(0, 1 - p, step):
                    self.draw_triangle_pixel(triangle, p, q)

    def draw_triangle_pixel(self, triangle: Triangle, p: float, q: float) -> None:
        point, color = triangle.get_vertice(p, q)
        if self.depth_manager.override(point):
            self.draw_pixel(point.x, point.y, color)

    def draw_pixel(self, x: int, y: int, color: tuple) -> None:
        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return

        self.color_map[y][x] = color
