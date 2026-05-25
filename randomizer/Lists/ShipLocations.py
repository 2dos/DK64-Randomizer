"""Stores the data for each potential crashed ship location."""

import math
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Maps import Maps


def offset_position(x0, y0, z0, rot_x, rot_y, rot_z, rot_x_offset=0, rot_y_offset=130.9, dist=275.282):
    # Convert degrees to radians
    yaw = math.radians(rot_y + rot_y_offset)
    pitch = math.radians(rot_x + rot_x_offset)
    dx = math.cos(pitch) * math.sin(yaw)
    dy = math.sin(pitch)
    dz = math.cos(pitch) * math.cos(yaw)

    # Apply distance
    new_x = x0 + dx * dist
    new_y = y0 + dy * dist
    new_z = z0 + dz * dist

    return new_x, new_y, new_z


class ShipObject:
    def __init__(
        self,
        name: str,
        map_index: Maps,
        coords: list[float],
        region: Regions,
        logic=None,
        euler_rotation: list[int] = [0, 0, 0],
        lz_position: list[int] = None,
        rotation: list[float] = [0, 0, 0],
        scale: float = 0.25,
        is_vanilla: bool = False,
    ):
        self.name = name
        self.map_index = map_index
        self.coords = coords
        self.region = region
        if logic is not None:
            self.logic = logic
        else:
            self.logic = lambda _: True
        self.rotation = rotation
        self.lz_radius = 60 * scale
        if lz_position is None:
            self.lz_position = offset_position(coords[0], coords[1] + (20 * scale), coords[2], euler_rotation[0], euler_rotation[1], euler_rotation[2], dist=275.282 * scale)
        else:
            self.lz_position = lz_position
        self.scale = scale
        self.is_vanilla = is_vanilla


ship_locations: list[ShipObject] = [
    ShipObject(
        name="Jungle Japes: Cannon Platform",
        map_index=Maps.JungleJapes,
        coords=[1257.5957693466887, 520, 2309.0319632875244],
        region=Regions.JapesCannonPlatform,
        euler_rotation=[0, 0, 0],
        rotation=[0, 0, 0],
        scale=0.1832350134513773,
    ),
    ShipObject(
        name="Jungle Japes: Stormy Area",
        map_index=Maps.JungleJapes,
        coords=[1486.3193217002445, 280.00000000000006, 3691.427635084099],
        region=Regions.JapesBeyondCoconutGate2,
        euler_rotation=[0, 0, 0],
        rotation=[0, 0, 0],
        scale=0.25,
    ),
    ShipObject(
        name="Jungle Japes: Near Fairy Pool",
        map_index=Maps.JungleJapes,
        coords=[567.133469107452, 240, 3159.6219847091684],
        region=Regions.BeyondRambiGate,
        euler_rotation=[0, 0, 0],
        rotation=[0, 0, 0],
        scale=0.25,
    ),
    ShipObject(
        name="Jungle Japes: Chunky's Cave",
        map_index=Maps.JapesUnderGround,
        coords=[833.573387925955, 33.827699026248546, 1112.110174267377],
        region=Regions.JapesCatacomb,
        lz_position=[878.6878609410554, 4.499580320670058, 1077.9101789381023],
        rotation=[-39.94141022929682, 0, 0],
        scale=0.25,
    ),
    ShipObject(
        name="Jungle Japes: Mountain Interior",
        map_index=Maps.JapesMountain,
        coords=[698.1428654287425, 102.72215884936865, 1174.2547057606032],
        region=Regions.Mine,
        lz_position=[754.8353091640479, 104.78477048565924, 1140.4222412340405],
        rotation=[0, -11.511106003520865, 0],
        scale=0.24999999999999997,
    ),
    ShipObject(
        name="Jungle Japes: Minecart Ride",
        map_index=Maps.JapesMinecarts,
        coords=[213.00021490804565, 165.69754146828424, 3171.2951373489486],
        region=Regions.JapesMinecarts,
        lz_position=[260.1929047053399, 205.9730708956007, 3173.726575807188],
        rotation=[80.29859721419669, 0, 0],
        scale=0.25,
    ),
    ShipObject(
        name="Angry Aztec: Vase Room",
        map_index=Maps.AngryAztec,
        coords=[337.14454615754187, 121.83547952764468, 944.4567004656129],
        region=Regions.AngryAztecStart,
        logic=lambda l: (l.pineapple and l.ischunky) or l.CanPhase(),
        euler_rotation=[0, 0, 0],
        rotation=[0, 0, 0],
        scale=0.25,
    ),
    ShipObject(
        name="Gloomy Galleon: Lighthouse underwater",
        map_index=Maps.GloomyGalleon,
        coords=[1926.508307797383, 956.2259831671781, 3970.4787778944815],
        region=Regions.LighthouseUnderwater,
        euler_rotation=[0, 0, 0],
        rotation=[0, 0, 0],
        scale=0.25,
    ),
    ShipObject(
        name="Creepy Castle: Graveyard",
        map_index=Maps.CreepyCastle,
        coords=[608.794859027693, 523.6666666666666, 1843.6024908447173],
        region=Regions.CastleGraveyardPlatform,
        euler_rotation=[0, 0, 0],
        rotation=[0, 0, 0],
        scale=0.25,
    ),
]
