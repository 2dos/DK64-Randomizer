"""Assesses ROM for optimization purposes."""

from BuildLib import heap_size

CODE_END = 0x805FAE00

sizes = []
with open("rom/dev-function-sizes.txt", "w") as output:
    with open("rom/dev-symbols.sym", "r") as fh:
        lines = fh.readlines()
        previous_address = None
        previous_fn_name = None
        for line in lines:
            text = line.replace("\n", "")
            data = text.split(" ")
            address = data[0]
            if address != "\x1a":
                address_int = int(address, 16)
                if address_int < CODE_END and address_int > CODE_END - heap_size:
                    function_name = data[1]
                    if previous_address is not None and previous_fn_name[:5] != ".byt:":
                        size = int(address, 16) - int(previous_address, 16)
                        sizes.append({"name": previous_fn_name, "size": size})
                previous_fn_name = data[1]
                previous_address = address
    sizes = sorted(sizes, key=lambda x: x["size"], reverse=True)
    for entry in sizes:
        output.write(f"{entry['name']}: {hex(entry['size'])}\n")
