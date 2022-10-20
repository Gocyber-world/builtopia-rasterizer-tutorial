
from camera import PerspectiveCamera
from camera import OrthographicCamera
from rasterizer import Rasterizer
from enum import Enum

class Size(Enum):
    width = 800
    height = 800
    scale = 200

def main():
    camera = PerspectiveCamera()
    camera.setUp(3, 3, 3)
    rasterizer = Rasterizer(Size.width.value, Size.height.value, Size.scale.value, camera, "./model/monkey.gltf")
    rasterizer.draw_primitives().show()
if __name__ == "__main__":
    main()