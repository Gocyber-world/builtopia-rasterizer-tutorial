import numpy as np
import struct
from PIL import Image
from pygltflib import GLTF2

I_WIDTH = 800
I_HEIGHT = 600
RGBS = np.zeros(I_WIDTH * I_HEIGHT * 3, np.uint8).reshape(I_HEIGHT, I_WIDTH, 3)

def drawPixels():

    i = Image.fromarray(RGBS, 'RGB')
    i.show()

def loadGltf(path):
    gltf = GLTF2().load(path)
    mesh = gltf.meshes[gltf.scenes[gltf.scene].nodes[0]]
    primitives = []

    # get the vertices for each primitive in the mesh (in this example there is only one)
    for primitive in mesh.primitives:

        # get all vertices
        # get the binary data for this mesh primitive from the buffer
        accessor = gltf.accessors[primitive.attributes.POSITION]
        bufferView = gltf.bufferViews[accessor.bufferView]
        buffer = gltf.buffers[bufferView.buffer]
        data = gltf.get_data_from_buffer_uri(buffer.uri)
        dataLength = (int)(bufferView.byteLength / accessor.count)
        
        # pull each vertex from the binary buffer and convert it into a tuple of python floats
        vertices = []
        for i in range(accessor.count):
            index = bufferView.byteOffset + accessor.byteOffset + i * dataLength  # the location in the buffer of this vertex
            d = data[index:index + dataLength]  # the vertex data
            v = struct.unpack("<fff", d)   # convert from base64 to three floats
            vertices.append(v)

        # get all normals
        # get the binary data for this mesh primitive from the buffer
        accessor = gltf.accessors[primitive.attributes.NORMAL]
        bufferView = gltf.bufferViews[accessor.bufferView]
        buffer = gltf.buffers[bufferView.buffer]
        data = gltf.get_data_from_buffer_uri(buffer.uri)
        dataLength = (int)(bufferView.byteLength / accessor.count)

        # pull each vertex from the binary buffer and convert it into a tuple of python floats
        normals = []
        for i in range(accessor.count):
            index = bufferView.byteOffset + accessor.byteOffset + i * dataLength  # the location in the buffer of this vertex
            d = data[index:index + dataLength]
            v = struct.unpack("<fff", d)   # convert from base64 to three floats
            normals.append(v)

        # get all uvs
        # get the binary data for this mesh primitive from the buffer
        accessor = gltf.accessors[primitive.attributes.TEXCOORD_0]
        bufferView = gltf.bufferViews[accessor.bufferView]
        buffer = gltf.buffers[bufferView.buffer]
        data = gltf.get_data_from_buffer_uri(buffer.uri)
        dataLength = (int)(bufferView.byteLength / accessor.count)

        # pull each vertex from the binary buffer and convert it into a tuple of python floats
        uvs = []
        for i in range(accessor.count):
            index = bufferView.byteOffset + accessor.byteOffset + i * dataLength  # the location in the buffer of this vertex
            uv = data[index:index + dataLength]
            value = struct.unpack("ff", uv)   # convert from base64 to two floats
            uvs.append(value)

        # get all indices
        # get the binary data for this mesh primitive from the buffer
        accessor = gltf.accessors[primitive.indices]
        bufferView = gltf.bufferViews[accessor.bufferView]
        buffer = gltf.buffers[bufferView.buffer]
        data = gltf.get_data_from_buffer_uri(buffer.uri)
        dataLength = (int)(bufferView.byteLength / accessor.count)

        # pull each vertex from the binary buffer and convert it into a tuple of python floats
        indices = []
        for i in range(accessor.count):
            index = bufferView.byteOffset + accessor.byteOffset + i * dataLength  # the location in the buffer of this vertex
            indice = data[index:index + dataLength]
            val = struct.unpack("h", indice)
            indices.append(val)

        primitives.append({'vertices':vertices,
            'normals': normals,
            'uvs': uvs,
            'indices': indices
        })
    return primitives

for i in range(200):
    RGBS[i][100][0] = 0
    RGBS[i][100][1] = 255
    RGBS[i][100][2] = 255
data = loadGltf("box.gltf")
print(data)
drawPixels()