"""Convert Dirt Patch CSV into a python list."""
import csv
import re

with open("doors.csv", newline="") as csvfile:
    patch_data = csv.reader(csvfile, delimiter=",", quotechar="|")
    door_data_json = []
    for idx, row in enumerate(patch_data):
        if idx > 0:
            door_data_json.append(
                {
                    "levelname": row[0],
                    "map": row[1],
                    "logicregion": row[2],
                    "name": row[3],
                    "coords": [float(row[4]), float(row[5]), float(row[6]), float(row[7])],
                    "rx": row[9],
                    "rz": row[10],
                    "scale": row[11],
                    "door_type": row[12],
                    "group": row[14],  # argument prevents tns portals from being too close to each other
                    "moveless": row[15],
                    "logic": row[16],
                    "kongs": row[17],
                    "placed": row[18],  # vanilla door types
                    "commented": row[19],
                    "post_comment": row[20],
                    "test_round": row[21],
                }
            )
    print(f"{len(door_data_json)} doors found")
    print("-----------------")
    print("Levels.JungleJapes: [")
    previous_levelname = "JungleJapes"
    for x in door_data_json:
        precomment = ""
        if x["post_comment"] != "":
            x["post_comment"] = "  # " + x["post_comment"]
        if x["commented"] != "":
            precomment = "# "
        level_name = x["levelname"].replace(" ", "")
        if level_name != previous_levelname:
            previous_levelname = level_name
            print("],")
            print("Levels." + level_name + ": [")
        rx_text = ""
        rz_text = ""
        scale_text = ""
        door_type_text = ""
        placed_text = ""
        if x["rx"]:
            rx_text = ", rx=" + x["rx"] + ""
        if x["rz"]:
            rz_text = ", rz=" + x["rz"] + ""
        if x["scale"]:
            scale_text = ", scale=" + x["scale"] + ""
        if x["door_type"]:
            door_type_text = ', door_type="' + x["door_type"] + '"'
        name = f"{x['levelname']}: {x['name']}"
        moveless_text = ", moveless=False"
        if x["moveless"].strip() == "":
            moveless_text = ""
        if x["logic"].strip() == "":
            x["logic"] = "True"
        x["logic"] = x["logic"].replace("|", ",")
        logic = f"lambda l: {x['logic']}"
        kongs_text = ""
        if x["kongs"]:
            kongs_text = x["kongs"].replace(" or ", ", Kongs.")
            kongs_text = ", kong_lst=[Kongs." + kongs_text + "]"
        if x["placed"] != "":
            placed_text = ', placed="' + x["placed"] + '"'
        print(
            f"\t"
            + precomment
            + f"DoorData(name=\"{name}\", map=Maps.{x['map']}, logicregion=Regions.{x['logicregion']}, location=[{x['coords'][0]}, {x['coords'][1]}, {x['coords'][2]}, {x['coords'][3]}]{rx_text}{rz_text}{scale_text}{kongs_text}, group={x['group']}{moveless_text}, logic={logic}{placed_text}{door_type_text}, test_round={x['test_round']}),{x['post_comment']}"
        )
    print("],")
