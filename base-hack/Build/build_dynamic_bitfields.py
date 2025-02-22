"""Build dynamic bitfield entries."""

H_FILE = "include/dynamic_structs.h"
BITFIELDS = {
    "RemovedBarriers": [
        "five_dt_switches",
        "production_room_on",
        "seasick_ship_spawned",
        "igloo_pads_spawned",
        "unused_4",
        "japes_coconut_gates",
        "shellhive_gate",
        "aztec_tunnel_door",
        "factory_testing_gate",
        "lighthouse_gate",
        "fungi_green_tunnel",
        "fungi_yellow_tunnel",
        "shipwreck_gate",
        "llama_switches",
    ],
    "FasterChecks": [
        "piano",
        "diddy_rnd",
        "mech_fish",
        "arcade_first_round",
        "rabbit_race",
        "castle_cart",
        "arcade_second_round",
    ],
}

with open(H_FILE, "w") as fh:
    warning = [
        "/*",
        "\tThis file is automatically written to by build_dynamic_bitfields.py",
        "\tDon't directly modify this file, instead modify the script",
        "\tOtherwise your changes will be overwritten on next build",
        "",
        "\tThanks,",
        "\t\tBallaam",
        "*/",
        "",
    ]
    for w in warning:
        fh.write(f"{w}\n")
    for key in BITFIELDS:
        txt_struct = [f"typedef struct {key} {{"]
        txt_enum = [f"typedef enum ENUM_{key} {{"]
        for index, data in enumerate(BITFIELDS[key]):
            modulo = index & 7
            offset = index >> 3
            mask = 0x80 >> modulo
            txt_struct.append(f"\tunsigned char {data} : 1; // {hex(mask)} {f'(OFFSET {offset})' if modulo == 0 else ''}")
            txt_enum.append(f"\t/* {index} */ {key.upper()}_ENUM_{data.upper().replace('_','')},")
        txt_struct.append(f"}} {key};")
        txt_enum.append(f"}} ENUM_{key};")
        fh.write("\n")
        for item in txt_struct:
            fh.write(f"{item}\n")
        fh.write("\n")
        for item in txt_enum:
            fh.write(f"{item}\n")
