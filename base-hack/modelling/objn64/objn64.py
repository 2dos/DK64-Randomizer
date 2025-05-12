"""Based on https://github.com/n64dev/objn64."""

from objload import objLoadObj
from objlib import Object

def strBetween(input: str, start: str, end: str) -> str:
    """Get the substring between a start and end point"""
    if start not in input:
        raise Exception(f"{start} not in {input}")
    input = input.split(start)[1]
    if end not in input:
        raise Exception(f"{end} not in {input}")
    return input.split(end)[0]

def convert_model(file: str, ambient_occlusion: bool = False, normals: bool= False, one_tri: bool = False, scale: float = 1, vert_cache_size: int = 32):
    obj = Object()
    obj.scale = scale
    obj.cn = normals
    if file is None:
        return
    obj = objLoadObj(file, obj)
    #objSetVertices(obj)
    if ambient_occlusion and not one_tri:
        # objAmbientOcclusion(obj)
    file_dl = file.replace(".obj", ".h")
    # writeDL(file_dl, obj, vert_cache_size, one_tri)