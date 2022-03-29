"""Apply Boss Locations."""
from randomizer.Patcher import ROM
from randomizer.Spoiler import Spoiler


def randomize_barrels(spoiler: Spoiler):
    """Randomize barrel locations."""
    barrel_replacements = [
        {
            "containing_map": 0x26,
            "barrels": [
                {
                    "instance_id": 33,
                    "new_map": 0x11,
                }
            ],
        }
    ]

    barrels = [12, 91]
    if spoiler.settings.bonus_barrel_rando:
        for cont_map in barrel_replacements:
            aztec_setup = 0x235331C
            # Pointer Table 9, use "containing_map" as a map index to grab setup start address
            ROM().seek(aztec_setup)
            model2_count = int.from_bytes(ROM().readBytes(4), "big")
            ROM().seek(aztec_setup + 4 + (model2_count * 0x30))
            mystery_count = int.from_bytes(ROM().readBytes(4), "big")
            ROM().seek(aztec_setup + 4 + (model2_count * 0x30) + 4 + (mystery_count * 0x24))
            actor_count = int.from_bytes(ROM().readBytes(4), "big")
            start_of_actor_range = aztec_setup + 4 + (model2_count * 0x30) + 4 + (mystery_count * 0x24) + 4
            # print(hex(start_of_actor_range))
            for x in range(actor_count):
                start_of_actor = start_of_actor_range + (0x38 * x)
                ROM().seek(start_of_actor)
                ROM().seek(start_of_actor + 0x32)
                actor_type = int.from_bytes(ROM().readBytes(2), "big")
                if actor_type in barrels:
                    ROM().seek(start_of_actor + 0x34)
                    actor_id = int.from_bytes(ROM().readBytes(2), "big")
                    for barrel in cont_map["barrels"]:
                        if barrel["instance_id"] == actor_id:
                            ROM().seek(start_of_actor + 0x12)
                            ROM().write(barrel["new_map"].to_bytes(2, "big"))
