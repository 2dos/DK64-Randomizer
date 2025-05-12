"""Class definitions for converting models."""

from enum import IntEnum, auto

MAX_VERTICES = 8192*2
MAX_NORMALS = 4096*2
MAX_TEXCOORDS = 4096*2
MAX_FACES = 4096*2

class TexMode(IntEnum):
    RGBA5551 = 1
    CI8 = auto()
    CI4 = auto()
    IA8 = auto()
    IA4 = auto()

class Point3:
    def __init__(self):
        self.x = None
        self.y = None
        self.z = None

class Vertex:
    def __init__(self):
        self.x = None
        self.y = None
        self.z = None
        self.tu = None
        self.tv = None
        self.nx = None
        self.ny = None
        self.nz = None
        self.b = None
        self.a = None
        self.Kd = None

class Point2:
    def __init__(self):
        self.x = None
        self.y = None

class Face:
    def __init__(self):
        self.v = [None] * 3 # Vertex
        self.vt = [None] * 3 # Vertex Tex UV
        self.vn = [None] * 3 # Vertex Normals

class Mesh:
    def __init__(self):
        self.name = ""
        self.material = ""
        self.material_num = 0
        self.vertices: list[Vertex] = []
        self.normals: list[Point3] = []
        self.texcoords: list[Point2] = []
        self.faces: list[Face] = []

class Texture:
    def __init__(self):
        self.name = ""
        self.mode: TexMode = None
        self.data = [0] * 4096
        self.width = 0
        self.height = 0

class Material:
    def __init__(self):
        self.name = ""
        self.diffuse = 0
        self.alpha: float = 1
        self.texture_diff = ""
        self.texture_num = 0

class Object:
    def __init__(self):
        self.meshes: list[Mesh] = []
        self.materials: list[Material] = []
        self.textures: list[Texture] = []
        self.scale: float = 1
        self.cn = False
        self.filename_mtl = ""