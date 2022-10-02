from unittest.mock import DEFAULT
import numpy as np

UP_Y = [0, 1, 0]
UP_Z = [0, 0, 1]
DEFAULT_MATRIX = np.array([
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,0],
    [0,0,0,1]
])

class Camera:
    def __init__(self):
        self.position = [0, 0, 1]
        self.look_at = [0, 0, 0]
        self.up = self.norm([0, 1, 0])
        self.camera_matrix = DEFAULT_MATRIX
        self.generate_matrix()

    def set(self, position, look_at, up):
        if (np.array_equal(position, look_at)):
            print ("failed: position is equal to look_at")

        self.position = position
        self.look_at = look_at
        self.up = self.norm(up)
        self.generate_matrix()

    def get_matrix(self):
        return self.camera_matrix.transpose()

    def generate_matrix(self):
        z = self.norm(np.subtract(self.position, self.look_at))
        # use default up, if z & up is parallel
        if np.array_equal(z, self.up) or (np.array_equal(z, [-i for i in self.up])):
            self.up = UP_Z if np.array_equal(self.up, UP_Y) else UP_Y

        x = self.norm(np.cross(self.up, z))
        y = self.norm(np.cross(z, x))
        self.camera_matrix = np.array([
            np.append(x, -self.look_at[0]),
            np.append(y, -self.look_at[1]),
            np.append(z, -self.look_at[2]),
            [0, 0, 0, 1]
        ])

    def norm(self, v):
        norm = np.linalg.norm(v)
        if norm == 0:
            return v
        return v / norm