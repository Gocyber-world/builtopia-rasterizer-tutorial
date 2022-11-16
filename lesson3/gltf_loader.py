import struct
from pygltflib import GLTF2

class GltfLoader:
    def load(self, path: str) -> list:
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
                vertices.append(list(v))

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
                indices.append(val[0])

            primitives.append({
                'vertices':vertices,
                'normals': normals,
                'uvs': uvs,
                'indices': indices
            })

        return primitives
