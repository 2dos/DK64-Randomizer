"""Place the ship object and associated attributes into ROM."""
from randomizer.Lists.ShipLocations import ship_locations
from randomizer.Enums.Maps import Maps
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames
from randomizer.Patching.Library.Generic import getNextFreeID
from randomizer.Patching.Library.DataTypes import float_to_hex
from randomizer.Patching.Library.Scripts import addNewScript
from randomizer.Enums.ScriptTypes import ScriptTypes

def RemoveOldShip(ROM_COPY):
    """Remove all remnants of the original ship from isles."""
    # Remove from the setup
    cont_map_setup_address = getPointerLocation(TableNames.Setups, Maps.Isles)
    ROM_COPY.seek(cont_map_setup_address)
    model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
    new_ints = [model2_count]
    for x in range(model2_count):
        item_start = cont_map_setup_address + 4 + (x * 0x30)
        ROM_COPY.seek(item_start + 0x28)
        item_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
        if item_type == 675:
            new_ints[0] = new_ints[0] - 1
            continue
        for y in range(12):
            ROM_COPY.seek(item_start + (y * 4))
            new_ints.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
    ROM_COPY.seek(cont_map_setup_address + 4 + (model2_count * 0x30))
    mys_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
    new_ints.append(mys_count)
    for x in range(mys_count):
        item_start = cont_map_setup_address + 8 + (model2_count * 0x30) + (x * 0x24)
        for y in range(9):
            ROM_COPY.seek(item_start + (y * 4))
            new_ints.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
    ROM_COPY.seek(cont_map_setup_address + 8 + (model2_count * 0x30) + (mys_count * 0x24))
    act_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
    new_ints.append(act_count)
    for x in range(act_count):
        item_start = cont_map_setup_address + 12 + (model2_count * 0x30) + (mys_count * 0x24) + (x * 0x38)
        for y in range(14):
            ROM_COPY.seek(item_start + (y * 4))
            new_ints.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
    ROM_COPY.seek(cont_map_setup_address)
    for x in new_ints:
        ROM_COPY.writeMultipleBytes(x, 4)

def PlaceShip(spoiler, ROM_COPY):
    """Place Ship function."""
    if spoiler.ship_location_index is None:
        return
    if not spoiler.settings.ship_location_rando:
        return
    # First, remove the ship from Isles
    RemoveOldShip(ROM_COPY)
    # Now, place the new one
    ship_data = ship_locations[spoiler.ship_location_index]

    # Write the setup
    cont_map_setup_address = getPointerLocation(TableNames.Setups, ship_data.map_index)
    ROM_COPY.seek(cont_map_setup_address)
    model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
    new_ints = [model2_count]
    for x in range(model2_count):
        item_start = cont_map_setup_address + 4 + (x * 0x30)
        for y in range(12):
            ROM_COPY.seek(item_start + (y * 4))
            new_ints.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
    # Add the new ship in
    new_ints[0] = new_ints[0] + 2
    selected_id = getNextFreeID(ROM_COPY, ship_data.map_index)
    selected_id_controller = getNextFreeID(ROM_COPY, ship_data.map_index, [selected_id])
    print(ship_data.lz_position)
    new_ints.extend(
        [
            # Ship
            int(float_to_hex(ship_data.coords[0]), 16),
            int(float_to_hex(ship_data.coords[1]), 16),
            int(float_to_hex(ship_data.coords[2]), 16),
            int(float_to_hex(ship_data.scale), 16),
            0x027B0002,
            0x05800640,
            int(float_to_hex(ship_data.rotation[0]), 16),
            int(float_to_hex(ship_data.rotation[1]), 16),
            int(float_to_hex(ship_data.rotation[2]), 16),
            0,
            (675 << 16) | selected_id,
            1 << 16,
            # Controller
            int(float_to_hex(ship_data.lz_position[0]), 16),
            int(float_to_hex(ship_data.lz_position[1]), 16),
            int(float_to_hex(ship_data.lz_position[2]), 16),
            int(float_to_hex(ship_data.scale), 16),
            0x027B0002,
            0x05800640,
            0,
            0,
            0,
            0,
            (0 << 16) | selected_id_controller,
            1 << 16,
        ]
    )
    # Get the rest of the file, then recompose it
    ROM_COPY.seek(cont_map_setup_address + 4 + (model2_count * 0x30))
    mys_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
    new_ints.append(mys_count)
    for x in range(mys_count):
        item_start = cont_map_setup_address + 8 + (model2_count * 0x30) + (x * 0x24)
        for y in range(9):
            ROM_COPY.seek(item_start + (y * 4))
            new_ints.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
    ROM_COPY.seek(cont_map_setup_address + 8 + (model2_count * 0x30) + (mys_count * 0x24))
    act_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
    new_ints.append(act_count)
    for x in range(act_count):
        item_start = cont_map_setup_address + 12 + (model2_count * 0x30) + (mys_count * 0x24) + (x * 0x38)
        for y in range(14):
            ROM_COPY.seek(item_start + (y * 4))
            new_ints.append(int.from_bytes(ROM_COPY.readBytes(4), "big"))
    ROM_COPY.seek(cont_map_setup_address)
    for x in new_ints:
        ROM_COPY.writeMultipleBytes(x, 4)
    # Scripts
    addNewScript(ROM_COPY, ship_data.map_index, [selected_id], ScriptTypes.KRoolShip)
    addNewScript(ROM_COPY, ship_data.map_index, [selected_id_controller], ScriptTypes.KRoolShipController, {
        selected_id_controller: {
            "radius": int(ship_data.lz_radius)
        }
    })