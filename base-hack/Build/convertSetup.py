"""Convert file setup."""

import os
import shutil

from enum import IntEnum, auto
from BuildLib import float_to_hex, intf_to_float
from BuildEnums import Maps
from getMoveSignLocations import getMoveSignData
from place_vines import generateVineSeries

BUTTON_DIST_NORMAL = 20
CAVES_ITEM_HEIGHT = 20


class ObjectChangeType(IntEnum):
    """Object Change Type Enum."""

    add = auto()
    delete = auto()
    edit = auto()
    null = auto()


class ObjectTypes(IntEnum):
    """Object Type Enum."""

    actor = auto()
    modeltwo = auto()


def writeValueToByteArray(data_stream: bytearray, value: int, size: int, offset: int, make_float: bool = False, condition: bool = True) -> bytearray:
    """Write value with defined size to byte array, returning that byte array."""
    if not condition:
        return data_stream
    if value is None:
        return data_stream
    value_as_array = [0] * size
    writing = value
    if make_float and size == 4:
        writing = int(float_to_hex(value), 16)
    for x in range(size):
        value_as_array[(size - 1) - x] = int(writing & 0xFF)
        writing = int(writing >> 8)
    for xi, x in enumerate(value_as_array):
        data_stream[offset + xi] = x
    return data_stream


class ObjectChange:
    """Class to store information regarding an object change."""

    def __init__(
        self,
        obj_master_type: ObjectTypes,
        change: ObjectChangeType,
        object_map: Maps,
        source_obj_id: int,
        new_id: int = None,
        obj_type: int = None,
        x: float = None,
        y: float = None,
        z: float = None,
        scale: float = None,
        rx: float = None,
        ry: float = None,
        rz: float = None,
        use_stream: bool = False,
        new_bonus_id: int = None,
    ):
        """Initialize with given parameters."""
        # Mandatory
        self.obj_master_type = obj_master_type
        self.change = change
        self.object_map = object_map
        self.source_obj_id = source_obj_id  # Object which derives the "base byte stream" used to create or edit an object, set to None for deletions
        # Derived
        self.use_stream = obj_master_type == ObjectTypes.modeltwo or use_stream
        # Optional
        self.new_id = new_id
        self.obj_type = obj_type
        self.x = x
        self.y = y
        self.z = z
        self.scale = scale
        self.rx = rx
        self.ry = ry
        self.rz = rz
        self.new_bonus_id = new_bonus_id
        self.added = False

    def getStream(self, data_stream: bytes) -> bytes:
        """Get data stream with modifications."""
        print(f"Making Stream: {self.__dict__}")
        if self.obj_master_type in (ObjectTypes.actor, ObjectTypes.modeltwo):
            byte_array = bytearray(data_stream).copy()
            if self.change == ObjectChangeType.add:
                if not self.use_stream and self.obj_master_type == ObjectTypes.actor:
                    byte_array = writeValueToByteArray(byte_array, 0, 4, 0x10)
                    byte_array = writeValueToByteArray(byte_array, 0, 4, 0x14)
                    byte_array = writeValueToByteArray(byte_array, 0, 4, 0x18)
                    byte_array = writeValueToByteArray(byte_array, 0, 4, 0x1C)
                    byte_array = writeValueToByteArray(byte_array, 0, 4, 0x20)
                    byte_array = writeValueToByteArray(byte_array, 0, 4, 0x24)
                    byte_array = writeValueToByteArray(byte_array, 0, 4, 0x28)
                    byte_array = writeValueToByteArray(byte_array, 0, 4, 0x2C)
                    byte_array = writeValueToByteArray(byte_array, 0, 2, 0x36)
                if self.obj_master_type == ObjectTypes.modeltwo:
                    byte_array = writeValueToByteArray(byte_array, 0xFFFB0000, 4, 0x10)
                    byte_array = writeValueToByteArray(byte_array, 0x15000000, 4, 0x14)
                    byte_array = writeValueToByteArray(byte_array, 0, 0x4, 0x24)
                    byte_array = writeValueToByteArray(byte_array, 0x00010000, 0x4, 0x2C)
            byte_array = writeValueToByteArray(byte_array, self.x, 4, 0x0, True)
            byte_array = writeValueToByteArray(byte_array, self.y, 4, 0x4, True)
            byte_array = writeValueToByteArray(byte_array, self.z, 4, 0x8, True)
            byte_array = writeValueToByteArray(byte_array, self.scale, 4, 0xC, True)
            byte_array = writeValueToByteArray(byte_array, self.new_bonus_id, 2, 0x1A, False)
            byte_array = writeValueToByteArray(byte_array, self.obj_type, 2, 0x32 if self.obj_master_type == ObjectTypes.actor else 0x28)
            byte_array = writeValueToByteArray(byte_array, self.new_id, 2, 0x34 if self.obj_master_type == ObjectTypes.actor else 0x2A)
            byte_array = writeValueToByteArray(byte_array, self.rx, 4, 0x18, True, self.obj_master_type == ObjectTypes.modeltwo)
            byte_array = writeValueToByteArray(byte_array, self.ry, 4, 0x1C, True, self.obj_master_type == ObjectTypes.modeltwo)
            byte_array = writeValueToByteArray(byte_array, self.ry, 2, 0x30, False, self.obj_master_type == ObjectTypes.actor)
            byte_array = writeValueToByteArray(byte_array, self.rz, 4, 0x20, True, self.obj_master_type == ObjectTypes.modeltwo)
            print(hex(len(byte_array)))
            return bytes(byte_array)
        return data_stream


def convertSetup(file_name):
    """Convert file type setup.

    Args:
        file_name (str): File name to convert.
    """
    with open(file_name, "rb") as source:
        with open("_" + file_name, "wb") as modified:
            modified.write(source.read())
    map_index = int(file_name.split("setup")[1].split(".bin")[0])
    modify("_" + file_name, map_index)
    if os.path.exists(file_name):
        os.remove(file_name)
    shutil.copyfile("_" + file_name.replace(".bin", "_.bin"), file_name)
    if os.path.exists("_" + file_name):
        os.remove("_" + file_name)
    if os.path.exists("_" + file_name.replace(".bin", "_.bin")):
        os.remove("_" + file_name.replace(".bin", "_.bin"))


def writedatatoarr(stream, value, size, location):
    """Write data to an array."""
    for x in range(size):
        stream[location + x] = bytearray(value.to_bytes(size, "big"))[x]
    return stream


base_stream = 0
HELM_FACE_LOW = 104.5
HELM_FACE_HIGH = 160
HELM_FACE_Z = 5423.538
MODEL_TWO_INDEXES = {}


def getPortalIndicatorY(portal_y: float) -> float:
    """Get Y Value of the indicator which should be attributed to a portal."""
    return portal_y - 30


def getNewID(map: Maps) -> int:
    """Get free ID for a model two object."""
    if map not in list(MODEL_TWO_INDEXES.keys()):
        MODEL_TWO_INDEXES[map] = 0x221
        return 0x220
    MODEL_TWO_INDEXES[map] += 1
    return MODEL_TWO_INDEXES[map] - 1


def getObjectModifications(target_map: Maps) -> list:
    """Get list of object modifications that need to be made."""
    MODEL_TWO_INDEXES = {}
    obj_modifications = [
        # Static modifications
        ObjectChange(ObjectTypes.modeltwo, ObjectChangeType.edit, Maps.Japes, 0x1A, obj_type=0xCE),  # Japes starting switch
        ObjectChange(ObjectTypes.modeltwo, ObjectChangeType.edit, Maps.TrainingGrounds, 0x39, obj_type=0xCE),  # TGrounds Switch
        ObjectChange(ObjectTypes.modeltwo, ObjectChangeType.edit, Maps.Japes, 0x52, x=1648.095, y=990, z=2431.953),  # Japes Mountain GB
        ObjectChange(ObjectTypes.modeltwo, ObjectChangeType.edit, Maps.Japes, 0x68, scale=0.15),  # Stump GB
        ObjectChange(ObjectTypes.modeltwo, ObjectChangeType.edit, Maps.Factory, 0x13E, scale=0.2),  # Nintendo Coin
        ObjectChange(ObjectTypes.modeltwo, ObjectChangeType.edit, Maps.Cranky, 0x2, scale=0.2),  # Rareware Coin
        ObjectChange(ObjectTypes.modeltwo, ObjectChangeType.edit, Maps.Factory, 0x24, x=1455.853, y=6.5, z=522.716, ry=0),  # Free Chunky Switch
        ObjectChange(ObjectTypes.modeltwo, ObjectChangeType.edit, Maps.Caves, 0x57, x=176.505, z=1089.408),  # Caves 5DI W3
        ObjectChange(ObjectTypes.modeltwo, ObjectChangeType.edit, Maps.Caves, 0xCF, x=176.505, z=1089.408),  # Caves 5DI W3 Bunch
        ObjectChange(ObjectTypes.modeltwo, ObjectChangeType.edit, Maps.Japes, 0xC9, y=400),  # Japes chunky bunch on top of Cranky
        ObjectChange(
            ObjectTypes.modeltwo, ObjectChangeType.add, Maps.Isles, 0x6, new_id=0x100, obj_type=132, x=2457.471, y=1280, z=3458.604, rx=0, ry=166, rz=0, scale=1.18
        ),  # Factory Lobby Barricade
        ObjectChange(ObjectTypes.modeltwo, ObjectChangeType.edit, Maps.Factory, 0x2C, y=715),  # Factory Diddy Prod GB
        ObjectChange(ObjectTypes.modeltwo, ObjectChangeType.edit, Maps.Factory, 0x7, y=475),  # Factory Last Prod Elevator
        # ObjectChange(ObjectTypes.modeltwo, ObjectChangeType.edit, Maps.Factory, 0x1CD, y=178.5), # Factory Spring Coins
        # ObjectChange(ObjectTypes.modeltwo, ObjectChangeType.edit, Maps.Factory, 0x1CE, y=178.5), # Factory Spring Coins
        # ObjectChange(ObjectTypes.modeltwo, ObjectChangeType.edit, Maps.Factory, 0x1CF, y=178.5), # Factory Spring Coins
        ObjectChange(ObjectTypes.actor, ObjectChangeType.add, Maps.Japes, 0x0, new_id=0x100, x=1839.1, y=680, z=2863, obj_type=112, rx=0, ry=0, rz=0, scale=0.25),  # Japes Headphones
        ObjectChange(ObjectTypes.actor, ObjectChangeType.add, Maps.Helm, 0x0, new_id=0x100, x=575.763, y=HELM_FACE_HIGH, z=HELM_FACE_Z, obj_type=54, rx=0, ry=0, rz=0, scale=0.35),  # Helm Faces
        ObjectChange(ObjectTypes.actor, ObjectChangeType.add, Maps.Helm, 0x0, new_id=0x101, x=494.518, y=HELM_FACE_HIGH, z=HELM_FACE_Z, obj_type=54, rx=0, ry=0, rz=0, scale=0.35),  # Helm Faces
        ObjectChange(ObjectTypes.actor, ObjectChangeType.add, Maps.Helm, 0x0, new_id=0x102, x=606.161, y=HELM_FACE_LOW, z=HELM_FACE_Z, obj_type=54, rx=0, ry=0, rz=0, scale=0.35),  # Helm Faces
        ObjectChange(ObjectTypes.actor, ObjectChangeType.add, Maps.Helm, 0x0, new_id=0x103, x=534.567, y=HELM_FACE_LOW, z=HELM_FACE_Z, obj_type=54, rx=0, ry=0, rz=0, scale=0.35),  # Helm Faces
        ObjectChange(ObjectTypes.actor, ObjectChangeType.add, Maps.Helm, 0x0, new_id=0x104, x=463.642, y=HELM_FACE_LOW, z=HELM_FACE_Z, obj_type=54, rx=0, ry=0, rz=0, scale=0.35),  # Helm Faces
        ObjectChange(ObjectTypes.actor, ObjectChangeType.edit, Maps.Galleon, 23, x=1296, y=1600, z=2028),  # Galleon Chunky 2DS Balloon
        ObjectChange(ObjectTypes.actor, ObjectChangeType.edit, Maps.Galleon, 25, y=1600),  # Galleon Lanky 5DS Balloon
        ObjectChange(ObjectTypes.actor, ObjectChangeType.edit, Maps.Galleon, 36, y=383.8333),  # Galleon Mermaid Tag
        ObjectChange(ObjectTypes.actor, ObjectChangeType.add, Maps.Caves5DIDK, 0x0, new_id=0x20, x=118.011, y=20, z=462.749, obj_type=0x29, rx=0, ry=1024, rz=0, scale=1),
        ObjectChange(ObjectTypes.actor, ObjectChangeType.add, Maps.CastleLibrary, 0x0, new_id=0x20, x=2668, y=216, z=287, obj_type=0x29, rx=0, ry=1024, rz=0, scale=1),
        ObjectChange(ObjectTypes.actor, ObjectChangeType.edit, Maps.Factory, 13, x=1237.001, y=175, z=840.569),  # Factory Diddy Storage Bonus
        ObjectChange(ObjectTypes.actor, ObjectChangeType.edit, Maps.TrainingGrounds, 6, new_bonus_id=96),  # Vine Barrel
        ObjectChange(ObjectTypes.actor, ObjectChangeType.edit, Maps.TrainingGrounds, 4, new_bonus_id=95),  # Dive Barrel
        ObjectChange(ObjectTypes.actor, ObjectChangeType.edit, Maps.TrainingGrounds, 3, new_bonus_id=97),  # Orange Barrel
        ObjectChange(ObjectTypes.actor, ObjectChangeType.edit, Maps.TrainingGrounds, 5, new_bonus_id=98),  # Barrel Barrel
    ]

    for switch_index in range(16):
        # Number Game Switches
        switch_z = switch_index % 4
        switch_x = int(switch_index / 4)
        switch_d = 37.7
        pos_x = 2606.114 + (switch_d * switch_x)
        pos_z = 1767.899 + (switch_d * switch_z)
        obj_modifications.append(ObjectChange(ObjectTypes.modeltwo, ObjectChangeType.edit, Maps.Factory, 0x67 + switch_index, x=pos_x, y=1002, z=pos_z))
    for platform_index in range(8):
        # Standardize lanky phase buttons
        id = 0xD + platform_index
        buttons = (0xE, 0xF, 0x10, 0x11)
        platforms = (0xD, 0x13, 0x14, 0x12)
        button_loc = ((780, 419.629 + BUTTON_DIST_NORMAL), (1135.232 - BUTTON_DIST_NORMAL, 780), (780, 1116.334 - BUTTON_DIST_NORMAL), (438.904 + BUTTON_DIST_NORMAL, 780))
        platform_loc = ((778.365, 396.901 + BUTTON_DIST_NORMAL), (1158.427 - BUTTON_DIST_NORMAL, 778.632), (780.283, 1138.851 - BUTTON_DIST_NORMAL), (416.092 + BUTTON_DIST_NORMAL, 778.456))
        x = 0
        z = 0
        if id in buttons:
            index = buttons.index(id)
            x = button_loc[index][0]
            z = button_loc[index][1]
        else:
            index = platforms.index(id)
            x = platform_loc[index][0]
            z = platform_loc[index][1]
        obj_modifications.append(ObjectChange(ObjectTypes.modeltwo, ObjectChangeType.edit, Maps.KRoolLanky, id, x=x, z=z))
    caves_underwater_items = (
        list(range(0xA5, 0xAF)),  # Lanky underwater CBs
        list(range(0xC0, 0xCA)),  # Tiny underwater CBs
        list(range(0x73, 0x76)),  # Chunky underwater coins
        list(range(0xD8, 0xDB)),  # Tiny underwater coins
        list(range(0xB7, 0xBA)),  # Lanky underwater coins (1)
        list(range(0xBD, 0xC0)),  # Lanky underwater coins (2)
    )
    for selection in caves_underwater_items:
        for id in selection:
            obj_modifications.append(ObjectChange(ObjectTypes.modeltwo, ObjectChangeType.edit, Maps.Caves, id, y=CAVES_ITEM_HEIGHT))
    # Vine Memes
    vine_data = generateVineSeries(target_map)
    for vine_add in vine_data["add"]:
        obj_modifications.append(
            ObjectChange(ObjectTypes.actor, ObjectChangeType.add, target_map, vine_add["id_base"], new_id=vine_add["id"], x=vine_add["x"], y=vine_add["y"], z=vine_add["z"], use_stream=True)
        )
    for vine_change in vine_data["change"]:
        obj_modifications.append(ObjectChange(ObjectTypes.actor, ObjectChangeType.edit, target_map, vine_change["id"], x=vine_change["x"], y=vine_change["y"], z=vine_change["z"]))
    # Shop Signs
    shop_signs = getMoveSignData(target_map)
    for sign in shop_signs:
        obj_modifications.append(
            ObjectChange(ObjectTypes.actor, ObjectChangeType.add, target_map, None, new_id=sign["id"], x=sign["x"], y=sign["y"], z=sign["z"], rx=0, ry=sign["ry"], rz=0, scale=0.25, obj_type=54)
        )
    return [x for x in obj_modifications if x.object_map == target_map]


def modify(file_name, map_index):
    """Modify the file to be updated.

    Args:
        file_name (str): File name.
        map_index (int): Map index.
    """
    global base_stream
    with open(file_name, "r+b") as fh:
        byte_read = fh.read()
        model2_count = int.from_bytes(byte_read[:4], "big")
        read_location = 4
        model2 = []
        mystery = []
        actor = []
        added_model2 = []
        added_actor = []
        added_caves_portal = False
        changes = getObjectModifications(map_index)
        for x in range(model2_count):
            byte_stream = byte_read[read_location : read_location + 0x30]
            _type = int.from_bytes(byte_read[read_location + 0x28 : read_location + 0x2A], "big")
            _id = int.from_bytes(byte_read[read_location + 0x2A : read_location + 0x2C], "big")
            if _type == 0x2AC and map_index != Maps.TroffNScoff:
                _y = int.from_bytes(byte_read[read_location + 4 : read_location + 8], "big")
                _yf = getPortalIndicatorY(intf_to_float(_y))
                if map_index == Maps.Japes and _id == 0x11A:
                    changes.append(ObjectChange(ObjectTypes.modeltwo, ObjectChangeType.add, map_index, _id, new_id=getNewID(map_index), x=805.6618, y=_yf, z=2226.797, obj_type=0x2AB, scale=0.35))
                else:
                    if map_index == Maps.Caves and not added_caves_portal:
                        changes.append(
                            ObjectChange(ObjectTypes.modeltwo, ObjectChangeType.add, map_index, _id, x=120.997, y=50.167, z=1182.974, rx=0, ry=75.146, rz=0, new_id=0x170)
                        )  # Caves 5DI Portal
                        changes.append(
                            ObjectChange(
                                ObjectTypes.modeltwo,
                                ObjectChangeType.add,
                                map_index,
                                _id,
                                obj_type=0x2AB,
                                x=120.997,
                                y=getPortalIndicatorY(50.167),
                                z=1182.974,
                                rx=0,
                                ry=75.146,
                                rz=0,
                                new_id=getNewID(Maps.Caves),
                                scale=0.35,
                            )
                        )  # Caves 5DI Portal Indicator
                        added_caves_portal = True
                    changes.append(ObjectChange(ObjectTypes.modeltwo, ObjectChangeType.add, map_index, _id, new_id=getNewID(map_index), y=_yf, obj_type=0x2AB, scale=0.35))
            # Parse changes
            instance_changes = [y for y in changes if (y.source_obj_id == _id or y.source_obj_id is None) and y.obj_master_type == ObjectTypes.modeltwo]
            deleting = False
            raw_byte_stream = byte_stream
            for change_data in instance_changes:
                if change_data.source_obj_id is None and change_data.added:
                    continue
                if change_data.change == ObjectChangeType.edit:
                    byte_stream = change_data.getStream(byte_stream)
                elif change_data.change == ObjectChangeType.add:
                    added_model2.append(change_data.getStream(raw_byte_stream))
                elif change_data.change == ObjectChangeType.delete:
                    deleting = True
                if change_data.source_obj_id is None:
                    change_data.added = True
            if not deleting:
                model2.append(byte_stream)
            read_location += 0x30
        mystery_count = int.from_bytes(byte_read[read_location : read_location + 4], "big")
        read_location += 4
        for x in range(mystery_count):
            byte_stream = byte_read[read_location : read_location + 0x24]
            mystery.append(byte_stream)
            read_location += 0x24
        actor_count = int.from_bytes(byte_read[read_location : read_location + 4], "big")
        read_location += 4
        for x in range(actor_count):
            byte_stream = byte_read[read_location : read_location + 0x38]
            obj_id = int.from_bytes(byte_read[read_location + 0x34 : read_location + 0x36], "big")
            instance_changes = [y for y in changes if (y.source_obj_id == obj_id or y.source_obj_id is None) and y.obj_master_type == ObjectTypes.actor]
            deleting = False
            raw_byte_stream = byte_stream
            for change_data in instance_changes:
                if change_data.source_obj_id is None and change_data.added:
                    continue
                if change_data.change == ObjectChangeType.edit:
                    byte_stream = change_data.getStream(byte_stream)
                elif change_data.change == ObjectChangeType.add:
                    added_actor.append(change_data.getStream(raw_byte_stream))
                elif change_data.change == ObjectChangeType.delete:
                    deleting = True
                if change_data.source_obj_id is None:
                    change_data.added = True
            if not deleting:
                actor.append(byte_stream)
            read_location += 0x38
        actor.extend(added_actor)
        model2.extend(added_model2)
        with open(file_name.replace(".bin", "_.bin"), "wb") as fg:
            fg.write(len(model2).to_bytes(4, "big"))
            for x in model2:
                fg.write(bytearray(x))
            fg.write(len(mystery).to_bytes(4, "big"))
            for x in mystery:
                fg.write(bytearray(x))
            fg.write(len(actor).to_bytes(4, "big"))
            for x in actor:
                fg.write(bytearray(x))
