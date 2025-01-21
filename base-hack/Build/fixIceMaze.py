"""Fix the collision surrounding the Ice Maze."""

import zlib

from BuildClasses import ROMPointerFile
from BuildEnums import TableNames
from BuildLib import ROMName
import math

ice_maze_file = "assets/Gong/ice_maze.bin"


def is_clockwise(polygon):
    """Determine if the polygon is ordered in a clockwise direction."""
    total = 0
    for i in range(len(polygon)):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % len(polygon)]
        total += (x2 - x1) * (y2 + y1)
    return total > 0


def point_in_triangle(pt, v1, v2, v3):
    """Check if a point is inside the triangle formed by vertices v1, v2, and v3."""

    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    b1 = sign(pt, v1, v2) < 0.0
    b2 = sign(pt, v2, v3) < 0.0
    b3 = sign(pt, v3, v1) < 0.0
    return b1 == b2 == b3


def ear_clip_triangulation(polygon):
    """Triangulate a simple polygon using the ear clipping method."""
    if len(polygon) < 3:
        raise ValueError("A polygon must have at least 3 vertices.")

    # Ensure the polygon vertices are ordered counter-clockwise
    if is_clockwise(polygon):
        polygon = polygon[::-1]

    triangles = []
    vertices = polygon[:]

    while len(vertices) > 3:
        n = len(vertices)
        for i in range(n):
            prev_idx = (i - 1) % n
            curr_idx = i
            next_idx = (i + 1) % n

            prev_vertex = vertices[prev_idx]
            curr_vertex = vertices[curr_idx]
            next_vertex = vertices[next_idx]

            # Check if the current vertex forms a convex angle
            if is_clockwise([prev_vertex, curr_vertex, next_vertex]):
                continue

            # Check if no other vertices are inside the triangle
            triangle = [prev_vertex, curr_vertex, next_vertex]
            ear_found = True
            for j in range(n):
                if j in {prev_idx, curr_idx, next_idx}:
                    continue
                if point_in_triangle(vertices[j], *triangle):
                    ear_found = False
                    break

            if ear_found:
                # Cut the ear and add the triangle to the list
                triangles.append(triangle)
                del vertices[curr_idx]
                break
    # Add the remaining triangle
    triangles.append(vertices)
    return triangles


maze = [
    (-127, 247),
    (-87, 202),
    (-161, 138),
    (-153, 81),
    (-203, 22),
    (-204, 6),
    (-231, 56),
    (-162, -115),
    (-130, -180),
    (-35, -217),
    (5, -159),
    (56, -204),
    (119, -176),
    (152, -67),
    (215, -17),
    (190, 98),
    (138, 148),
    (74, 134),
    (24, 55),
    (-35, 41),
    (-56, -15),
    (-17, -56),
    (35, -35),
    (53, 14),
    (113, 71),
    (149, 10),
    (97, -26),
    (79, -133),
    (-32, -108),
    (-82, -138),
    (-131, -68),
    (-172, -35),
    (-108, 15),
    (-87, 114),
    (-10, 199),
    (15, 275),
    (152, 227),
    (247, 117),
    (275, -24),
    (227, -162),
    (118, -257),
    (-24, -284),
    (-161, -237),
    (-257, -127),
    (-270, -56),
    (-284, 15),
    (-237, 152),
]


def generateIceMaze():
    """Pull geo file from ROM and modify."""
    with open(ROMName, "rb") as fh:
        ice_maze_f = ROMPointerFile(fh, TableNames.ModelTwoGeometry, 522)
        fh.seek(ice_maze_f.start)
        dec = zlib.decompress(fh.read(ice_maze_f.size), 15 + 32)
        with open("temp.bin", "wb") as fg:
            fg.write(dec)

    triangles = ear_clip_triangulation(maze)
    with open(ice_maze_file, "wb") as fh:
        with open("temp.bin", "r+b") as fg:
            fh.write(fg.read(0x54))
            for _ in range(8):
                old = int.from_bytes(fg.read(4), "big")
                new = old + (0x18 * len(triangles))
                fh.write(new.to_bytes(4, "big"))
            fh.write(fg.read(0x422C - 0x74))
            fg.read(4)  # dummy to shift read pointer
            fh.write(len(triangles).to_bytes(4, "big"))
            min_x = 9999
            max_x = -9999
            min_z = 9999
            max_z = -9999
            for tri in triangles:
                for point in tri:
                    min_x = min(min_x, point[0])
                    min_z = min(min_z, point[1])
                    max_x = max(max_x, point[0])
                    max_z = max(max_z, point[1])
            fg.read(12)  # dummy to shift read pointer
            min_xv = min_x + 65536 if min_x < 0 else min_x
            min_zv = min_z + 65536 if min_z < 0 else min_z
            max_xv = max_x + 65536 if max_x < 0 else max_x
            max_zv = max_z + 65536 if max_z < 0 else max_z
            fh.write(min_xv.to_bytes(2, "big"))
            fh.write((69).to_bytes(2, "big"))
            fh.write(min_zv.to_bytes(2, "big"))
            fh.write(max_xv.to_bytes(2, "big"))
            fh.write((71).to_bytes(2, "big"))
            fh.write(max_zv.to_bytes(2, "big"))
            for tri in triangles:
                for point in reversed(tri):
                    x = point[0] + 65536 if point[0] < 0 else point[0]
                    y = 70
                    z = point[1] + 65536 if point[1] < 0 else point[1]
                    fh.write(x.to_bytes(2, "big"))
                    fh.write(y.to_bytes(2, "big"))
                    fh.write(z.to_bytes(2, "big"))
                fh.write((0x0F00).to_bytes(2, "big"))  # idk what this does lol
                fh.write((0x0000).to_bytes(2, "big"))  # idk what this does lol
                fh.write((0xE840).to_bytes(2, "big"))  # idk what this does lol
            fh.write(fg.read())
