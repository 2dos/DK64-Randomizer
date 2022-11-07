enable = true
read_file = false
savestate.loadslot(9)
client.unpause()
idx = 0
results = io.open("results.txt", "w")
results:close()

function runTest()
    data_ram = 0x3EAB84
    data_file = 0xA0
    if enable then
        frame = emu.framecount()
        if frame > 5550 then
            savestate.loadslot(9)
            read_file = false
            cs = mainmemory.readbyte(0x7444EC)
            if cs == 1 then
                results = io.open("results.txt", "a")
                results:write(idx.."\n")
                enable = false
                results:close()
            end
            idx = idx + 1
            if idx > 0x300 then
                enable = false
            end
        else
            if read_file == false then
                src = assert(io.open("lanky_idle_anim.bin", "rb"))
                src:seek("set", data_file + idx)
                str = src:read("*a")
                src:close()
                a = string.byte(str:sub(1, 1))
                mainmemory.writebyte(data_ram + idx, a)
                read_file = true
            end
        end
    end
end

event.onframestart(runTest, "")