"""Get move sign data."""

from BuildLib import float_to_hex
from BuildEnums import Maps, Vendors


class SignInformation:
    """Class to store information regarding a shop sign."""

    def __init__(self, vendor: Vendors, x: float, y: float, z: float, angle: int):
        """Initialize with given data."""
        self.vendor = vendor
        self.x = x
        self.y = y
        self.z = z
        self.angle = angle


sign_data = {
    Maps.Japes: [
        SignInformation(Vendors.Cranky, 1695.127, 280, 3998.528, 3),
        SignInformation(Vendors.Funky, 2074.149, 520, 2248.571, 119),
        SignInformation(Vendors.Snide, 2174.763, 680, 2581.554, 288),
    ],
    Maps.Aztec: [
        SignInformation(Vendors.Candy, 2364.392, 120.5, 414.73, 0),
        SignInformation(Vendors.Cranky, 2697.736, 120.5, 2538.648, 290),
        SignInformation(Vendors.Funky, 2888.978, 121.051, 4546.7, 77),
        SignInformation(Vendors.Snide, 4217.064, 120, 4468.096, 334),
    ],
    Maps.Factory: [
        SignInformation(Vendors.Candy, 192.108, 225.5, 567.249, 38),
        SignInformation(Vendors.Funky, 1426.279, 1131.833, 468.852, 315),
        SignInformation(Vendors.Cranky, 202.208, 225.5, 902.929, 335),
        SignInformation(Vendors.Snide, 1753.705, 826, 2074.416, 34),
    ],
    Maps.Galleon: [
        SignInformation(Vendors.Cranky, 3288.249, 1790, 2370.118, 196),
        SignInformation(Vendors.Candy, 2816.421, 1564.253, 553.305, 82),
        SignInformation(Vendors.Funky, 3676.859, 1560.177, 1235.449, 337),
        SignInformation(Vendors.Snide, 2091.915, 1610, 4726.344, 307),
    ],
    Maps.Fungi: [
        SignInformation(Vendors.Cranky, 1005.894, 247, 263.491, 164),
        SignInformation(Vendors.Funky, 3271.472, 178.69, 93.169, 264),
        SignInformation(Vendors.Snide, 3090.001, 267.011, 3588.082, 194),
    ],
    Maps.Caves: [
        SignInformation(Vendors.Cranky, 1127.643, 281.527, 1574.504, 225),
        SignInformation(Vendors.Funky, 2777.721, 280, 1340.63, 86),
        SignInformation(Vendors.Candy, 3285.967, 112.833, 2187.781, 214),
        SignInformation(Vendors.Snide, 1210.936, 64.5, 411.259, 110),
    ],
    Maps.Castle: [
        SignInformation(Vendors.Cranky, 235.221, 1135.469, 1412.605, 278),
        SignInformation(Vendors.Snide, 784.377, 1794.167, 1362.74, 180),
    ],
    Maps.CastleCrypt: [
        SignInformation(Vendors.Funky, 1456.806, 200, 246.614, 274),
    ],
    Maps.CastleDungeon: [
        SignInformation(Vendors.Candy, 1191.144, 300, 2142.678, 269),
    ],
    Maps.TrainingGrounds: [
        SignInformation(Vendors.Cranky, 602.935, 75, 1870.478, 309),
    ],
    Maps.Isles_SnideRoom: [
        SignInformation(Vendors.Snide, 449.519, 0, 468.524, 268),
    ],
}

default_offsets = {
    Vendors.Candy: 0,
    Vendors.Cranky: 180,
    Vendors.Funky: 90,
    Vendors.Snide: 270,
}


def convertCoord(f):
    """Convert a coord to an int."""
    return int(float_to_hex(f), 16)


def convertAngle(f):
    """Convert an angle to DK64 Angle system."""
    return int(((f / 360) * 4096))


def getMoveSignData(map_index):
    """Get current move sign data."""
    sign_arr = []
    if map_index in list(sign_data.keys()):
        for sign in sign_data[map_index]:
            id = 0x100 + int(sign.vendor)
            a_offset = default_offsets[sign.vendor]
            sign_arr.append(
                {
                    "x": sign.x,
                    "y": sign.y,
                    "z": sign.z,
                    "ry": convertAngle(sign.angle + a_offset) % 4096,
                    "id": id,
                }
            )
    return sign_arr
