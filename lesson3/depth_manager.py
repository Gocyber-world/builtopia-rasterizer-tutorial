import numpy as np

class DepthManager:
    def __init__(self, width, height):
        self.depth_map = np.full((height, width), float("-inf"), np.float32)
        self.min_depth = float('inf')
        self.max_depth = float('-inf')
        self.depth_ratio = 1

    def add_depth(self, depth):
        self.min_depth = min(self.min_depth, depth)
        self.max_depth = max(self.max_depth, depth)

    def calc_depth_ratio(self):
        if (self.max_depth == self.min_depth):
            # all vertices on the same depth plane
            self.depth_ratio = 1
        else:
            self.depth_ratio = 255/abs(self.max_depth - self.min_depth)

    def get_color(self, depth):
        # reutrn normalized color value
        return int(255 + (depth - self.max_depth) * self.depth_ratio)

    def override(self, x, y, depth):
        old_depth = self.depth_map[y][x]
        if depth > old_depth:
            self.depth_map[y][x] = depth
            return True
        else:
            return False
