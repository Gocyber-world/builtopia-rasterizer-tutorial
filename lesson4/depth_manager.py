import numpy as np
from triangle import Vertice

class DepthManager:
    def __init__(self, width: int, height: int) -> None:
        self.depth_map = np.full((height, width), float("-inf"), np.float32)
        self.min_depth = float('inf')
        self.max_depth = float('-inf')
        self.depth_ratio = 1.0

    def add_depth(self, depth: float) -> None:
        self.min_depth = min(self.min_depth, depth)
        self.max_depth = max(self.max_depth, depth)

    def calc_depth_ratio(self) -> None:
        if (self.max_depth != self.min_depth):
            self.depth_ratio = 255/abs(self.max_depth - self.min_depth)

    def get_color(self, point: Vertice) -> tuple:
        # reutrn normalized color(0-255)
        color_value = int(255 + (point.depth - self.max_depth) * self.depth_ratio)
        return (color_value, color_value, color_value)

    def override(self, point: Vertice) -> bool:
        old_depth = self.depth_map[point.y][point.x]
        if point.depth > old_depth:
            self.depth_map[point.y][point.x] = point.depth
            return True
        else:
            return False
