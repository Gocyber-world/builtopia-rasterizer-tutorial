import numpy as np
from triangle import Vertice

class DepthManager:
    def __init__(self, width: int, height: int) -> None:
        self.width, self.height = width, height
        self.depth_map = np.full((height, width), float("-inf"), np.float32)

    def override(self, point: Vertice) -> bool:
        if point.x >= self.width or point.x < 0 or point.y >= self.height or point.y < 0:
            return False

        old_depth = self.depth_map[point.y][point.x]
        if point.depth < old_depth:
            return False

        self.depth_map[point.y][point.x] = point.depth
        return True
