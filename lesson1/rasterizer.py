import numpy as np
import struct
from PIL import Image
from pygltflib import GLTF2

I_WIDTH = 800
I_HEIGHT = 600
I_SCALE = 200
RGBS = np.zeros(I_WIDTH * I_HEIGHT * 3, np.uint8).reshape(I_HEIGHT, I_WIDTH, 3)
WHITE = (255,255,255)
CAMERA_TRANSFORM_MATRIX = np.array([
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,0],
    [0,0,0,1]
])
CAMERA_CLIP_MATRIX = np.array([
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
    x = np.array([startf[0], startf[1], startf[2], 1])
    y = np.array([endf[0], endf[1], endf[2], 1])
    transformClipMat = np.matmul(CAMERA_CLIP_MATRIX, CAMERA_TRANSFORM_MATRIX)
    startCam = np.matmul(transformClipMat, x)
    endCam = np.matmul(transformClipMat, y)
    drawLine(positionToPixelPos(startCam), positionToPixelPos(endCam))

def drawPixel(position, color):
    x = position[0]
    y = position[1]
    if x>=I_WIDTH or x<0 or y>=I_HEIGHT or y<0:
        return

    RGBS[y][x][0] = color[0]
    RGBS[y][x][1] = color[1]
    RGBS[y][x][2] = color[2]

def positionToPixelPos(position):
    x = position[0] / position[3]
    y = position[1] / position[3]
    u = (int)((x * I_SCALE + I_WIDTH/2) )
    v = (int)((-1 * y * I_SCALE + I_HEIGHT/2))
    return (u, v)

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


def genCamTransformMatrix(position, lookat, up):
    # 1. position & lookat => transformVector
    # 2. up + transformVector => forwardCamera, upCamera, rightCamera
    # 3. calTransformMatrix
    transformVector = (position[0] - lookat[0], position[1] - lookat[1], position[2] - lookat[2])
    forwardCamera = norm(transformVector)
    tmpUp = up
    if (abs(np.dot(forwardCamera, norm(up))) == 1):
        tmpUp = (up[1], up[0], up[2])

    rightCamera = norm(np.cross(tmpUp, forwardCamera))
    upCamera = norm(np.cross(forwardCamera, rightCamera))

    return np.array([
        [rightCamera[0], rightCamera[1], rightCamera[2], 0],
        [upCamera[0], upCamera[1], upCamera[2], 0],
        [forwardCamera[0], forwardCamera[1], forwardCamera[2], 0],
        [transformVector[0], transformVector[1], transformVector[2], 1]
    ]).transpose()


def genCamClipMatrix(fov, nearClip, farClip):
    aspect = I_WIDTH / I_HEIGHT
    fov = np.radians(fov)
    E = np.cos(fov / 2)
    A = (nearClip + farClip)/(nearClip - farClip)
    B = -(2 *farClip * nearClip) / (nearClip - farClip)
    return np.array([[E/(aspect *nearClip), 0, 0, 0], [0, E/nearClip, 0, 0], [0 ,0, A, B],[0 ,0, 1, 0]])

data = loadGltf("monkey.gltf")
CAMERA_TRANSFORM_MATRIX = genCamTransformMatrix((0, 0, 2), (0,0,0), (0,1,0))
print(CAMERA_TRANSFORM_MATRIX)
CAMERA_CLIP_MATRIX = genCamClipMatrix(45, 1, 1000)
print(CAMERA_CLIP_MATRIX)

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