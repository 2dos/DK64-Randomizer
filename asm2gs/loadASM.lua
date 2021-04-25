lips = require "lips.init";

function isPointer(value)
	return type(value) == "number" and value >= 0x80000000 and value < 0x80800000;
end

local code = {};

function codeWriter(...)
	if isPointer(arg[1]) then
		table.insert(code, {arg[1] - 0x80000000, arg[2]});
	else
		print("Warning: "..toHexString(arg[1]).." isn't a pointer to RDRAM on the System Bus. Writing outside RDRAM isn't currently supported.");
	end
end

function fileExists(file)
	local f=io.open(file,"r")
	if f ~= nil then
		io.close(f)
		return true;
	else
		return false;
	end
end

function loadASMPatch(code_filename)
	if not fileExists(code_filename) then
		print("No code loaded, aborting mission...");
		return false;
	end

	-- Open the file and assemble the code
	code = {};
	local result = lips(code_filename, codeWriter);

	if #code == 0 then
		print(result);
		print("The code did not compile correctly, check for errors in your source.");
		return false;
	end

	-- Patch the code
	file = io.open("codeOutput.txt","w+")
	for i = 1, #code do
		file:write(code[i][1]..":"..code[i][2].."\n");
	end
	file:write()

	--print("")
	return true;
end