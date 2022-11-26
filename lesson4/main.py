from camera import Camera
from rasterizer import Rasterizer
import cProfile

I_WIDTH = 800
I_HEIGHT = 600
I_SCALE = 200

camera = Camera()
camera.set(
    position=[1, 2, 3],
    look_at=[0, 0, 0],
    up=[0, 1, 0],
    fovy=45,
    near=1
)

rasterizer = Rasterizer(I_WIDTH, I_HEIGHT, I_SCALE, camera, "data/shapes.gltf")
# rasterizer.draw_meshes().show()
cProfile.run("rasterizer.draw_meshes()")