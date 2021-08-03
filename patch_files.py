"""Deal with logic for the footer patch files."""
import json

from browser import bind, document, timer, window

import common
from randomize import randomize

jq = window.jQuery


@bind(document["nav-seed-gen-tab"], "click")
@bind(document["nav-patch-tab"], "click")
def disable_input(event):
    """Disable input for each tab as we rotate through the navbar.

    Args:
        event (DOMEvent): DOM item that triggered the event.
    """
    ev_type = False
    if "patch-tab" in event.target.id:
        ev_type = True
    inputs = document["form"].select("input")
    for item in document["form"].select(".form-check"):
        inputs.append(item)
    for item in document["form"].select("select"):
        inputs.append(item)
    for item in inputs:
        if ev_type is True:
            item.attrs["disabled"] = "disabled"
        else:
            try:
                del item.attrs["disabled"]
            except Exception:
                pass
    if ev_type is False:
        common.update_disabled_progression()
        try:
            document["input-file-rom"].id = "input-file-rom_2"
        except Exception:
            pass
        document["input-file-rom_1"].id = "input-file-rom"
    else:
        try:
            document["input-file-rom"].id = "input-file-rom_1"
        except Exception:
            pass
        document["input-file-rom_2"].id = "input-file-rom"


def start_randomizing_seed(form_data: dict):
    """Randomize the seed data using the passed dict.

    Args:
        form_data (dict): Passed JSON Data.
    """
    jq("#patchprogress").width("30%")
    jq("#progress-text").text("Randomizing seed")
    randomized_data = randomize(form_data)

    def randomize_seed_data():
        jq("#patchprogress").width("40%")
        jq("#progress-text").text("Randomizing complete")
        timer.set_timeout(finish_randomizing_seed(randomized_data, form_data), 1000)

    timer.set_timeout(randomize_seed_data, 1000)


def finish_randomizing_seed(data, form_data):
    """Randomized Generation completed.

    Args:
        data (str): String data of the ASM.
        form_data (dict): Dict data of the form.
    """
    if data is False:
        jq("#patchprogress").addClass("bg-danger")
        jq("#patchprogress").width("100%")
        jq("#progress-text").text("Failed to successfully generate a seed.")
    else:
        if document["downloadjson"].checked:

            def save_lanky():
                jq("#patchprogress").width("100%")
                jq("#progress-text").text("Patch File Generated.")
                file = window.File.new([json.dumps(form_data)], "dk64r-settings-" + form_data.get("seed") + ".lanky")
                window.saveAs(file)

            timer.set_timeout(save_lanky, 2000)
        else:
            convert_asm(data)
    timer.set_timeout(reset_progress_bar, 5000)


def reset_progress_bar():
    """Reset the progress bar once it has completed."""
    try:
        jq("#patchprogress").removeClass("bg-danger")
    except Exception:
        pass
    jq("#patchprogress").width("0%")
    jq("#progress-text").text("")
    jq("#progressmodal").modal("hide")


def convert_asm(asm):
    """Convert the passed ASM to byte code.

    Args:
        asm (str): String data of the ASM code.
    """
    jq("#patchprogress").width("60%")
    jq("#progress-text").text("Generating ASM")
    window.L.execute(
        """
      function convert(code_filename)
          lips = require 'lips.init';
          local code = {};
          function codeWriter(key, value)
              function isPointer(value)
                  return type(value) == 'number' and value >= 0x80000000 and value < 0x80800000;
              end
              if isPointer(key) then
                  table.insert(code, {key - 0x80000000, value});
              end
          end
          lips(code_filename, codeWriter);
          local formatted_code = '';
          for k,v in pairs(code) do
            local pair_string = '';
            for key, value in pairs(v) do
              if(key == 1)
              then
                pair_string = pair_string .. value .. ':';
              else
                pair_string = pair_string .. value;
              end
            end
            formatted_code = formatted_code .. pair_string .. '\\n';
          end
          window.asmcode = formatted_code;
      end
      convert([["""
        + asm
        + "]])"
    )

    def asm_progress():
        jq("#patchprogress").width("70%")
        jq("#progress-text").text("ASM Generated")
        timer.set_timeout(start_apply_asm, 1000)

    timer.set_timeout(asm_progress, 1000)


def start_apply_asm():
    """Apply the ASM code to the rom."""
    # Convert the rom type to z64
    window.romFile.convert()
    # Apply the BPS
    apply_bps()
    max_addr = -1
    asm = str(window.asmcode)
    for item in asm.split("\n"):
        if item:
            addr = int(item.split(":")[0])
            if addr < 0x5FAE00:
                if addr > max_addr:
                    max_addr = addr
    if max_addr != -1 and max_addr >= 0x5DAE00:
        patch_extension_size = (max_addr - 0x5DAE00) + 1
        window.expand_rom_size(patch_extension_size)
        for line in asm.split("\n"):
            if line:
                data = line.split(":")
                apply_asm_bytes(int(data[0]), int(data[1]))
        fix_checksum()
        window.patchedRom.fileName = "dk64-randomizer-" + document["seed"].value + ".z64"
        window.patchedRom.save()


def apply_bps():
    """Apply the BPS file to the rom."""
    jq("#patchprogress").width("80%")
    jq("#progress-text").text("Applying patches")
    window.apply_bps_javascript()


def fix_checksum():
    """Set the security code and update the rom checksum."""
    window.patchedRom.seek(0x3154)
    window.patchedRom.writeU8(0)
    window.fixChecksum(window.patchedRom)
    jq("#patchprogress").width("100%")
    jq("#progress-text").text("Patching Complete")


def apply_asm_bytes(addr, val):
    """Apply ASM Bytes to the rom.

    Args:
        addr (int): Int address to rewrite.
        val (int): Int value to rewrite.
    """
    if addr >= 0x72C and addr < (0x72C + 8):
        diff = addr - 0x72C
        window.patchedRom.seek(0x132C + diff)
        window.patchedRom.writeU8(val)
        # print("Boot hook code")
    elif addr >= 0xA30 and addr < (0xA30 + 1696):
        diff = addr - 0xA30
        window.patchedRom.seek(0x1630 + diff)
        window.patchedRom.writeU8(val)
        # print("Expansion Pak Draw Code")
    elif addr >= 0xDE88 and addr < (0xDE88 + 3920):
        diff = addr - 0xDE88
        window.patchedRom.seek(0xEA88 + diff)
        window.patchedRom.writeU8(val)
        # print("Expansion Pak Picture")
    elif addr >= 0x5DAE00 and addr < (0x5DAE00 + 0x20000):
        diff = addr - 0x5DAE00
        window.patchedRom.seek(0x2000000 + diff)
        window.patchedRom.writeU8(val)
        # print("Heap Shrink Space")
