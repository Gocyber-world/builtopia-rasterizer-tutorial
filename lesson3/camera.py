import numpy as np

UP_Y = [0, 1, 0]
UP_Z = [0, 0, 1]

class Camera:
    def __init__(self) -> None:
        self.position = [0, 0, 3]
        self.look_at = [0, 0, 0]
        self.up = [0, 1, 0]
        self.fovy = 45
        self.near = 1
        self.aspect = 1
        self.height = 1
        self.width = 1

    def set(self, position: list, look_at: list, up: list, fovy: float, near: float) -> None:
        if (np.array_equal(position, look_at)):
            print ("failed: position is equal to look_at")
            return

        if (fovy <= 0 or fovy >= 180):
            print ("failed: fov exceeds limit")
            return

        self.position = position
        self.look_at = look_at
        self.up = self.norm(up)
        self.fovy = fovy
        self.near = near
        self.height = self.near*np.tan(self.fovy*np.pi/360)*2
        self.width = self.height*self.aspect

    def get_perspective(self) -> np.ndarray:
        perspective_matrix = np.array([
            [self.near*2/self.width, 0, 0, 0],
            [0, self.near*2/self.height, 0, 0],
            [0, 0, 1, 0],
            [0, 0, -1, 0]
        ])
        return np.matmul(perspective_matrix, self.get_orthographic())

    def get_orthographic(self) -> np.ndarray:
        z = self.norm(np.subtract(self.position, self.look_at))
        # use default up, if z & up is parallel
        if np.array_equal(z, self.up) or (np.array_equal(z, [-i for i in self.up])):
            self.up = UP_Z if np.array_equal(self.up, UP_Y) else UP_Y

        x = self.norm(np.cross(self.up, z))
        y = self.norm(np.cross(z, x))
        return np.array([
            np.append(x, -self.look_at[0]),
            np.append(y, -self.look_at[1]),
            np.append(z, -np.linalg.norm(np.subtract(self.position, self.look_at))),
            [0, 0, 0, 1]
        ])

    def norm(self, v: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(v)
        if norm == 0:
            return v
        return v / norm