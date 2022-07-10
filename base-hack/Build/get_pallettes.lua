rdram_offset = 0x80000000
rdram_end = rdram_offset + 0x800000
player = mainmemory.read_u32_be(0x7FBB4C) - rdram_offset
palette_master = mainmemory.read_u32_be(player + 0x158) - rdram_offset
cont = true
while cont do
    palette = mainmemory.read_u32_be(palette_master)
    if ((palette >= rdram_offset) and (palette < rdram_end)) then
        palette = mainmemory.read_u32_be(palette - rdram_offset)
        if ((palette >= rdram_offset) and (palette < rdram_end)) then
            print("0x"..bizstring.hex(palette))
        end
    end
    palette_master = mainmemory.read_u32_be(palette_master + 0x24)
    if ((palette_master >= rdram_offset) and (palette_master < rdram_end)) then
        palette_master = palette_master - rdram_offset
    else
        cont = false
    end
end