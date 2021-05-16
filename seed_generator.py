"""Generate ROM patch files."""
from lupa import LuaRuntime


def apply_asm(post_data):
    """Apply the ASM patch.

    Args:
        post_data (dict): Form Data.
    """
    loadASM = LuaRuntime(unpack_returned_tuples=False).eval(
        """function(code_filename)
        lips = require "lips.init";
        local code = {};
        function codeWriter(key, value)
            function isPointer(value)
                return type(value) == "number" and value >= 0x80000000 and value < 0x80800000;
            end
            if isPointer(key) then
                table.insert(code, {key - 0x80000000, value});
            end
        end
        lips(code_filename, codeWriter);
        return code;
    end"""
    )
    asm_binary = dict(loadASM(post_data))
    formatted_dat = ""
    for key in asm_binary:
        inter = dict(asm_binary[key])
        formatted_dat += str(inter[1]) + ":" + str(inter[2]) + "\n"
    return formatted_dat
