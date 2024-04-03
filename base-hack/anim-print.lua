dest = mainmemory.read_u32_be(0x7FBB54) - 0x80000000;
for i=0, 0x90 do
    str="";
    for j = 0, 6 do
        str = str.."0x"..bizstring.hex(mainmemory.read_u16_be(dest + (14 * i) + (2 * j))).."        ";
    end
    print(str)
end