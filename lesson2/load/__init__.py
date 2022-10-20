from .loader import Loader
from .gltfloader import GltfLoader

Loader.register('gltf', GltfLoader)