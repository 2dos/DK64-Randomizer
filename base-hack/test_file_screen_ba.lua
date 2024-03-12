init_count = 500
count_remaining = init_count
press_f = emu.framecount();
client.unpause()
output_file = io.open("./file_screen_test_quick.log", "w");
output_file:close();
state = 0
gap = 100
function testFileScreen()
    frame = emu.framecount()
    diff = frame - press_f
    gap = 50
    if state == 0 then
        gap = 100
    end
    if diff > gap then
        if state == 0 or state == 2 then
            joypad.set({["A"] = true}, 1);
        else
            joypad.set({["B"] = true}, 1);
        end
    end
    if diff > (gap + 10) then
        state = state + 1
        if state > 2 then
            state = 0
            count_remaining = count_remaining - 1
        end
        press_f = frame
        output_file = io.open("./file_screen_test_quick.log", "a");
        output_file:write("Ran test "..(init_count-count_remaining).."/"..init_count..": Success\n");
        if count_remaining == 0 then
            output_file:write("Test complete\n");
        end
        output_file:close();
    end
end
event.onframeend(testFileScreen, "Test File Screen")