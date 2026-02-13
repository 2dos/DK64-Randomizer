"""Imports an object file and converts it into a valid DK64 model file."""

import json
from typing import BinaryIO

OBJ_FILE = "dogadon.obj"
CONNECTION_FILE = "dogadon.json"
BASE_ADDR = 0x10002080
MODEL_DATA_OFFSET = 0x28
BIN_FILE = OBJ_FILE.split(".obj")[0] + ".bin"

def parse_obj_vertices(filepath):
    """
    Parses an .obj file and retrieves vertex coordinates for each mesh.
    
    Returns a dictionary: {mesh_name: [(x, y, z), ...], ...}
    """
    mesh_vertices = {}
    mesh_vertex_indexes = {}
    verts = []

    with open(filepath, 'r') as file:
        for line in file:
            stripped = line.strip()
            if stripped.startswith('o ') or stripped.startswith('g '):
            # if stripped.startswith('o '):
                current_mesh = stripped[2:].strip()
                if current_mesh not in mesh_vertices:
                    mesh_vertices[current_mesh] = []
                if current_mesh not in mesh_vertex_indexes:
                    mesh_vertex_indexes[current_mesh] = []
            elif stripped.startswith('v '):
                parts = stripped.split()
                if len(parts) >= 4:
                    x, y, z = map(float, parts[1:4])
                    r, g, b = map(float, parts[4:7])
                    verts.append({
                        "coords": (x, y, z),
                        "rgb": (int(r * 255), int(g * 255), int(b * 255))
                    })
            elif stripped.startswith('f '):
                parts = stripped.split()
                for index, face in enumerate(parts):
                    if index == 0:
                        continue
                    mesh_vertices[current_mesh].append(verts[int(face) - 1])
                    mesh_vertex_indexes[current_mesh].append(int(face) - 1)
    return mesh_vertices, mesh_vertex_indexes, verts

def writePointer(fh: BinaryIO, location: int):
    location -= MODEL_DATA_OFFSET
    location += BASE_ADDR
    fh.write(location.to_bytes(4, "big"))

mesh_verts, mesh_indexes, verts = parse_obj_vertices(OBJ_FILE)
connections: dict = None
with open(CONNECTION_FILE, 'r') as file:
    connections = json.load(file)
scale = connections.get("scale", 1)
print(verts)
# print(connections)
vert_end = None
dl_end = None
with open(BIN_FILE, "wb") as bin:
    # Write an empty header for now
    for _ in range(MODEL_DATA_OFFSET):
        bin.write(b"\0")
    # Write the verts
    for vert in verts:
        for coord in vert["coords"]:
            value = coord
            # Put any mesh offset fix here
            value = int(value * scale)
            if value < 0:
                value += 0x10000
            bin.write(value.to_bytes(2, "big"))
        for _ in range(3):
            bin.write((0).to_bytes(2, "big"))  # UV Mapping
        for channel in vert["rgb"]:
            bin.write(channel.to_bytes(1, "big"))  # RGB
        bin.write((255).to_bytes(1, "big"))  # Alpha
    vert_end = bin.tell() # let the writer know where the vert stuff ends
    starter = [
        0xE7000000, 0x00000000,
        0xE3000A01, 0x00100000,
        0xE200001C, 0x0C192078,
        0xFC127E04, 0xFF13F9FF,
        0xE3000F00, 0x00010000,
        0xD7002002, 0xFFFFFFFF,
        0xFD100000, 0x0C000000,
        0xF5100000, 0x07000000,
        0xE6000000, 0x00000000,
        0xF3000000, 0x0715B000,
        0xE7000000, 0x00000000,
        0xE3001001, 0x00000000,
        0xF5100800, 0x00090240,
        0xF2002002, 0x0003E03E,
        0xF5100440, 0x0108C631,
        0xF2002002, 0x0101E01E,
        0xF5100250, 0x02088A22,
        0xF2002002, 0x0200E00E,
        0xF5100254, 0x03084E13,
        0xF2002002, 0x03006006,
        0xF5100256, 0x04081204,
        0xF2002002, 0x04002002,
        0xE3000D01, 0x00000000,
        0xE3001201, 0x00002000,
        0xD9FFFFFF, 0x00000400,
    ]
    footer = [
        0xE7000000, 0x00000000,
        0xE3000A01, 0x00000000,
        0xE200001C, 0x00552078,
        0xFC41FE83, 0xFFFFF9FC,
        0xD7000002, 0xFFFFFFFF
    ]
    for item in starter:
        bin.write(item.to_bytes(4, "big"))
    # DA command to start the mesh, 01 command to load the verts, 05/06 commands to create the tris
    for footer in starter:
        bin.write(item.to_bytes(4, "big"))
    dl_end = bin.tell() # let the writer know where the vert stuff ends
    writePointer(bin, vert_end)

# with open(OBJ_FILE, "r") as obj:
#     