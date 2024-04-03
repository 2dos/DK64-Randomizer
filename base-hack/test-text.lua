is_crash = true
text_index = 33
client.unpause()
output_file = io.open("./text_test.log", "a")
output_file:close();
mainmemory.writebyte(0x7FFFFF, text_index);
savestate.loadslot(1);

function testText()
    frame = emu.framecount()
    if frame > 2800 then
        output_file = io.open("./text_test.log", "a");
        hint = math.floor(text_index / 3)
        shop = text_index % 3
        output_file:write("Hint "..hint.." Shop "..shop);
        if is_crash then
            output_file:write(": CRASH")
        end
        output_file:write("\n");
        output_file:close();
        is_crash = true
        savestate.loadslot(1)
        text_index = text_index + 1
        mainmemory.writebyte(0x7FFFFF, text_index)
    elseif frame > 2700 then
        if not emu.islagged() then
            is_crash = false
        end
    end
end

event.onframestart(testText, "Test Text")