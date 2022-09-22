import numpy as np
import struct
from PIL import Image
from pygltflib import GLTF2

I_WIDTH = 800
I_HEIGHT = 600
I_SCALE = 200
RGBS = np.zeros(I_WIDTH * I_HEIGHT * 3, np.uint8).reshape(I_HEIGHT, I_WIDTH, 3)
WHITE = (255,255,255)
CAMERA_MATRIX = np.array([
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,0],
    [0,0,0,1]
])


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

def rasterizeLine(startf, endf):
    start = np.matmul(startf, CAMERA_MATRIX)
    end = np.matmul(endf, CAMERA_MATRIX)
    drawLine(positionToPixelPos(start), positionToPixelPos(end))

def drawPixel(position, color):
    x = position[0]
    y = position[1]
    if x>=I_WIDTH or x<0 or y>=I_HEIGHT or y<0:
        return

    RGBS[y][x][0] = color[0]
    RGBS[y][x][1] = color[1]
    RGBS[y][x][2] = color[2]

def positionToPixelPos(position):
    x = position[0]
    y = position[1]
    x1 = (int)(x * I_SCALE + I_WIDTH/2)
    y1 = (int)(-1 * y * I_SCALE + I_HEIGHT/2)
    return (x1, y1)

def drawLine(start, end):
    
    startx = start[0]
    starty = start[1]
    endx = end[0]
    endy = end[1]

    step = 1
    if(startx > endx):
        step = -1
    if endx!=startx:
        for x in range(startx, endx, step):
            y = starty + (int)((endy - starty)*(x - startx)/(endx - startx))
            drawPixel((x,y), WHITE)

    step = 1
    if(starty > endy):
        step = -1
    if endy!=starty:
        for y in range(starty, endy, step):
            x = startx + (int)((endx - startx)*(y - starty)/(endy - starty))
            drawPixel((x,y), WHITE)
    drawPixel((endx,endy), WHITE)

def norm(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

def genCamMatrixByCamPos(position):
    z = norm(position)
    x = norm(np.cross((0,1,0), z))
    y = norm(np.cross(z, x))
    return np.array([x,y,z]).transpose()
    

data = loadGltf("monkey.gltf")
CAMERA_MATRIX = genCamMatrixByCamPos((1,5,1))
print(CAMERA_MATRIX)
for p in data:
    positions = p["vertices"]
    indices = p["indices"]
    
    for i in range(0, len(indices), 3):
        a = positions[indices[i][0]]
        b = positions[indices[i + 1][0]]
        c = positions[indices[i + 2][0]]
        rasterizeLine(a, b)
        rasterizeLine(b, c)
        rasterizeLine(c, a)

drawPixels()