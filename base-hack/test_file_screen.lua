init_count = 500
count_remaining = init_count
reset_f = 0
client.unpause()
output_file = io.open("./file_screen_test.log", "w");
output_file:close();
output_message = false
function testFileScreen()
    frame = emu.framecount()
    diff = frame - reset_f
    if (diff > 730 and diff < 750) or (diff > 780 and diff < 800) or (diff > 880 and diff < 900) then
        joypad.set({["A"] = true}, 1);
        output_message = false
    elseif diff > 950 then
        if not output_message then
            count_remaining = count_remaining - 1
            if count_remaining > 0 then
                joypad.set({["Power"] = true});
                reset_f = frame
            end
            output_file = io.open("./file_screen_test.log", "a");
            output_file:write("Ran test "..(init_count-count_remaining).."/"..init_count..": Success\n");
            if count_remaining == 0 then
                output_file:write("Test complete\n");
            end
            output_file:close();
            output_message = true
        end
    end
end
event.onframeend(testFileScreen, "Test File Screen")