keybindsRealtime = {};

function bind(keybindArray, key, callback, preventHold)
    if type(keybindArray) == "table" and type(key) == "string" and type(callback) == "function" then
        if type(preventHold) ~= "boolean" then
            preventHold = true
        end
        table.insert(keybindArray, {key = key, callback = callback, pressed = false, preventHold = preventHold});
    end
end

function bindKeyRealtime(key, callback, preventHold)
	bind(keybindsRealtime, key, callback, preventHold);
end

function processKeybinds(keybinds)
	local input_table = input.get();

	for i, keybind in ipairs(keybinds) do
		if not input_table[keybind.key] then
			keybind.pressed = false;
		end
		if input_table[keybind.key] and (not keybind.preventHold or not keybind.pressed) then
			keybind.callback();
			keybind.pressed = true;
		end
	end
end

positions = {};

function storePosition()
    player = mainmemory.read_u32_be(0x7FBB4C)
    if player ~= 0 then
        player = player - 0x80000000
        x = math.floor(mainmemory.readfloat(player + 0x7C, true))
        y = math.floor(mainmemory.readfloat(player + 0x80, true))
        z = math.floor(mainmemory.readfloat(player + 0x84, true))
        table.insert(positions, {x, y, z})
        print("Pushed Position")
        if #positions >= 2 then
            dumpPosition()
        end
    end
end


function dumpPosition()
    print("")
    print("FairyData(")
    print("\tname=\"\",")
    print("\tmap=None,")
    print("\tregion=None,")
    if positions[1][1] < positions[2][1] then
        xmin = positions[1][1]
        xmax = positions[2][1]
    else
        xmin = positions[2][1]
        xmax = positions[1][1]
    end
    if positions[1][3] < positions[2][3] then
        zmin = positions[1][3]
        zmax = positions[2][3]
    else
        zmin = positions[2][3]
        zmax = positions[1][3]
    end
    spawn_y = math.floor((positions[1][2] + positions[2][2]) / 2)

    print("\tfence=Fence("..xmin..", "..zmin..", "..xmax..", "..zmax.."),")
    print("\tspawn_y="..spawn_y..",")
    print("\tlogic=lambda l: l.camera,")
    print("),")
    print("")
    positions = {}
end

function clearPositions()
    positions = {}
    print("Cleared Positions")
end

bindKeyRealtime("J", storePosition, true);
bindKeyRealtime("K", dumpPosition, true);
bindKeyRealtime("L", clearPositions, true);

print("DK64 Position Dumper")
print("By Ballaam. 2023")
print("--------------------")
print("J - Log a position")
print("K - Dump all positions into a class format for banana coins. This also wipes your positions after dumping")
print("L - Clear all positions from memory")
print("")
while true do
    processKeybinds(keybindsRealtime);
    emu.yield();
end