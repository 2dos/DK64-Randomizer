anim_table = mainmemory.read_u32_be(0x7FBB58) - 0x80000000
for i = 0, 0x6E do
    str = ""
    for j = 0, 7 do
        if j == 0 then
            str = "0x"..bizstring.hex(mainmemory.read_u16_be(anim_table + (i * 14) + (j * 2)))
        else
            str = str.."    0x"..bizstring.hex(mainmemory.read_u16_be(anim_table + (i * 14) + (j * 2)))
        end
    end
    print(str)
end