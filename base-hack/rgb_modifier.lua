red = 0xFF;
green = 0xFF;
blue = 0xFF;

prev_r = red;
prev_g = green;
prev_b = blue;
function recolor()
	player = mainmemory.read_u32_be(0x7FBB4C)
	if player then
		player = player - 0x80000000
		pre = mainmemory.read_u32_be(player + 0x60)
		pre = bit.bor(pre, 0x00800000)
		mainmemory.write_u32_be(player + 0x60,pre)
		mainmemory.writebyte(player + 0x16A,red)
		mainmemory.writebyte(player + 0x16B,green)
		mainmemory.writebyte(player + 0x16C,blue)
		if prev_r ~= red then
			print("Changed RGB to 0x"..bizstring.hex(red)..bizstring.hex(green)..bizstring.hex(blue))
		end
		if prev_g ~= green then
			print("Changed RGB to 0x"..bizstring.hex(red)..bizstring.hex(green)..bizstring.hex(blue))
		end
		if prev_b ~= blue then
			print("Changed RGB to 0x"..bizstring.hex(red)..bizstring.hex(green)..bizstring.hex(blue))
		end
		prev_r = red;
		prev_g = green;
		prev_b = blue;
	end
end

event.onframeend(recolor)