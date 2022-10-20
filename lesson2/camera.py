from matrix.vec3 import Vec3
from matrix.mat4 import Mat4

class PerspectiveCamera:

    def __init__(self, fov=45, aspect=1, near=5, far=1000):
        self.fov = fov
        self.aspect= aspect
        self.near = near
        self.far = far
        self.target = Vec3()
        self.position = Vec3(z=3)
        self.up = Vec3(z=1)
        self.worldMatrix = Mat4()
        self.updateMatrix()

    def lookat(self, x, y, z):
        self.target.set(x=x, y=y, z=x)
        self.updateMatrix()

    def setUp(self, x, y, z):
        self.up.set(x=x, y=y, z=x)
        self.updateMatrix()

    def setPosition(self, x, y, z):
        self.position.set(x=x, y=y, z=x)
        self.updateMatrix()

    def updateMatrix(self):
        viewMatrix = Mat4().setLookAt(self.position, self.target, self.up)
        projection = Mat4().setPerspective(self.fov, self.aspect, self.near, self.far)
        self.worldMatrix = projection.mul(viewMatrix)

class OrthographicCamera:

    def __init__(self, left=-1, right=1, top=1, bottom=-1, near=1, far=1000) -> None:
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.near = near
        self.far = far
        self.target = Vec3()
        self.position = Vec3(z=3)
        self.up = Vec3(z=1)
        self.worldMatrix = Mat4()

    def lookat(self, x, y, z):
        self.target.set(x=x, y=y, z=x)
        self.updateMatrix()

    def setUp(self, x, y, z):
        self.up.set(x=x, y=y, z=x)
        self.updateMatrix()

    def updateMatrix(self):
        viewMatrix = Mat4().setLookAt(self.position, self.target, self.up)
        projection = Mat4().setOrtho(self.left, self.right, self.top, self.bottom, self.near, self.far)
        self.worldMatrix = projection.mul(viewMatrix)

    def setPosition(self, x, y, z):
        self.position.set(x=x, y=y, z=x)
        self.updateMatrix()