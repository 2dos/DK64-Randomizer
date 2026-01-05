"""Generate Watch File."""


def read_symbols():
    """Read the symbols file and update the labels."""
    addr_set = []
    sym_path = "asm/symbols.asm"
    with open(sym_path, "r") as fh:
        lines = fh.readlines()
        for x in lines:
            if ".definelabel" in x:
                name = x.split(".definelabel ")[1].split(", ")[0]
                addr = "0x" + x.split(", ")[1][4:10]
                addr_set.append({name, addr})
    return addr_set


def read_h_file(symbols_data):
    """Read the H file and update the externs."""
    addr_set = []
    type_set = []
    with open("include/dk64.h", "r") as fh:
        c = fh.readlines()
        for x in symbols_data:
            for y in c:
                if "extern " in y:
                    if ("(" not in y) and (")" not in y):
                        y = y.split("extern ")[1]
                        if "//" in y:
                            y = y.split("//")[0]
                        z = y.split(" ")
                        s = ""
                        n = z[-1].split(";")[-1]
                        if n == list(x)[1]:
                            for i in range(len(z) - 1):
                                s += z[i] + " "
                            if s not in type_set:
                                type_set.append(s)
                            addr_set.append([list(x)[0], list(x)[1], s])
    return addr_set


def create_wch_file(_data, watch_file_name):
    """Create an update WCH file."""
    wch_info = [
        ["*", "d", "h"],  # Pointer
        ["float", "d", "f"],
        ["unsigned int", "d", "h"],
        ["int", "d", "h"],
        ["unsigned short", "w", "h"],
        ["short", "w", "h"],
        ["unsigned char", "b", "h"],
        ["char", "b", "h"],
    ]
    with open(watch_file_name, "w") as fh:
        lines = ["SystemID N64"]
        for x in _data:
            found = False
            for y in wch_info:
                if y[0] in x[2]:
                    _size = y[1]
                    _type = y[2]
                    found = True
                    break
            if found:
                lines.append(str(x[0][2:]) + "	" + str(_size) + "	" + str(_type) + "	1	RDRAM	" + str(x[1]))
        for x in lines:
            fh.write(x + "\n")


a = read_symbols()
b = read_h_file(a)
create_wch_file(b, "rom/dk64-randomizer-base.wch")
