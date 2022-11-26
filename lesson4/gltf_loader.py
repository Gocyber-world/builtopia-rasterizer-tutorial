import struct
from pygltflib import GLTF2
from PIL import Image
from util import Mesh, PBRMaterial, Primitive

class GltfLoader:
    def load(self, path: str) -> list:
        gltf = GLTF2().load(path)
        textures = self.load_images(gltf)
        materials = self.load_materials(gltf, textures)
        meshes = self.load_meshes(gltf, materials)
        return meshes

    def load_images(self, gltf) -> list:
        # read all the images
        textures = []
        for image in gltf.images:
            textures.append(Image.open('data/' + image.uri))

        return textures

    def load_materials(self, gltf, textures: list) -> list:
        # read all the materials
        materials = []
        for mat in gltf.materials:
            m = PBRMaterial()
            if mat.pbrMetallicRoughness.baseColorTexture == None:
                factor = mat.pbrMetallicRoughness.baseColorFactor
                m.color = [int(255 * f) for f in factor[:3]]
            else:
                m.texture =  textures[mat.pbrMetallicRoughness.baseColorTexture.index]
            materials.append(m)

        return materials

    def load_meshes(self, gltf, materials: list) -> list:
        # read all the meshes
        meshes = []
        for node in gltf.nodes:
            if node.mesh == None:
                continue

            mesh = gltf.meshes[node.mesh]
            primitives = self.load_primitives(gltf, materials, mesh)
            meshes.append(Mesh(mesh.name, primitives, node.translation, node.scale))

        return meshes

    def load_primitives(self, gltf, materials, mesh) -> list:
        # get the vertices for each primitive in the mesh
        primitives = []
        for primitive in mesh.primitives:
            p = Primitive()
            p.vertices = self.load_vertices(gltf, primitive)
            p.normals = self.load_normals(gltf, primitive)
            p.uvs = self.load_uvs(gltf, primitive)
            p.indices = self.load_indices(gltf, primitive)
            if primitive.material != None:
                p.material = materials[primitive.material]
            primitives.append(p)

        return primitives

    def load_vertices(self, gltf, primitive) -> list:
        # get all vertices
        # get the binary data for this mesh primitive from the buffer
        accessor = gltf.accessors[primitive.attributes.POSITION]
        bufferView = gltf.bufferViews[accessor.bufferView]
        buffer = gltf.buffers[bufferView.buffer]
        data = gltf.get_data_from_buffer_uri(buffer.uri)
        dataLength = int(bufferView.byteLength / accessor.count)

        # pull each vertex from the binary buffer and convert it into a tuple of python floats
        vertices = []
        for i in range(accessor.count):
            index = bufferView.byteOffset + accessor.byteOffset + i * dataLength  # the location in the buffer of this vertex
            d = data[index:index + dataLength]  # the vertex data
            v = struct.unpack("<fff", d)   # convert from base64 to three floats
            vertices.append(list(v))

        return vertices

    def load_normals(self, gltf, primitive) -> list:
        # get all normals
        # get the binary data for this mesh primitive from the buffer
        accessor = gltf.accessors[primitive.attributes.NORMAL]
        bufferView = gltf.bufferViews[accessor.bufferView]
        buffer = gltf.buffers[bufferView.buffer]
        data = gltf.get_data_from_buffer_uri(buffer.uri)
        dataLength = int(bufferView.byteLength / accessor.count)

        # pull each vertex from the binary buffer and convert it into a tuple of python floats
        normals = []
        for i in range(accessor.count):
            index = bufferView.byteOffset + accessor.byteOffset + i * dataLength  # the location in the buffer of this vertex
            d = data[index:index + dataLength]
            v = struct.unpack("<fff", d)   # convert from base64 to three floats
            normals.append(v)

        return normals

    def load_uvs(self, gltf, primitive) -> list:
        # get all uvs
        # get the binary data for this mesh primitive from the buffer
        accessor = gltf.accessors[primitive.attributes.TEXCOORD_0]
        bufferView = gltf.bufferViews[accessor.bufferView]
        buffer = gltf.buffers[bufferView.buffer]
        data = gltf.get_data_from_buffer_uri(buffer.uri)
        dataLength = int(bufferView.byteLength / accessor.count)

        # pull each vertex from the binary buffer and convert it into a tuple of python floats
        uvs = []
        for i in range(accessor.count):
            index = bufferView.byteOffset + accessor.byteOffset + i * dataLength  # the location in the buffer of this vertex
            uv = data[index:index + dataLength]
            value = struct.unpack("ff", uv)   # convert from base64 to two floats
            uvs.append(value)

        return uvs

    def load_indices(self, gltf, primitive) -> list:
        # get all indices
        # get the binary data for this mesh primitive from the buffer
        accessor = gltf.accessors[primitive.indices]
        bufferView = gltf.bufferViews[accessor.bufferView]
        buffer = gltf.buffers[bufferView.buffer]
        data = gltf.get_data_from_buffer_uri(buffer.uri)
        dataLength = int(bufferView.byteLength / accessor.count)

        # pull each vertex from the binary buffer and convert it into a tuple of python floats
        indices = []
        for i in range(accessor.count):
            index = bufferView.byteOffset + accessor.byteOffset + i * dataLength  # the location in the buffer of this vertex
            indice = data[index:index + dataLength]
            val = struct.unpack("h", indice)
            indices.append(val[0])

        return indices
