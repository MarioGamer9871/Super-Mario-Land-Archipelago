while true do
	heart = memory.readbyte(0x00A3, "WRAM")
	if heart == 1 then
		memory.writebyte(0x1FFF, 1, "WRAM")
		heart = 0
	end
	emu.frameadvance();
end
