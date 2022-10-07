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
                    "levelname": row[1],
                    "map": row[2],
                    "logicregion": row[3],
                    "name": row[4],
                    "coords": [float(row[5]), float(row[6]), float(row[7]), float(row[8])],
                    "rx": float(row[10]),
                    "rz": float(row[11]),
                    "scale": float(row[12]),
                    "door_type": row[13],
                    "group": row[15], #argument prevents tns portals from being too close to each other
                    "logic": row[16],
                    "kongs": row[17],
                    "placed": row[18], #vanilla door types
                    "commented": row[19],
                    "post_comment": row[20],
                }
            )
    print(f"{len(door_data_json)} doors found")
    print("-----------------")
    print("Levels.JungleJapes: [")
    previous_levelname = "JungleJapes"
    for x in door_data_json:
        precomment = ""
        if x["post_comment"] is not "":
            x["post_comment"] = "  # "+x["post_comment"]
        if x["commented"] is not "":
            precomment = "# "
        level_name = x["levelname"].replace(" ", "")
        if level_name is not previous_levelname:
            previous_levelname = level_name
            print("],")
            print("Levels."+level_name+": [")
        rx_text = ""
        rz_text = ""
        if x["rx"]:
            rx_text = ", rx="+x["rx"]+""
        if x["rz"]:
            rz_text = ", rz="+x["rz"]+""
        name = f"{x['levelname']}:  {x['name']}"
        kongs_text=""
        if x["kongs"]:
            kongs_text = x["kongs"].replace(" or ", ", Kongs.")
            kongs_text = ", kong_lst=[Kongs."+kongs_text+"]"
        if x["logic"].strip() == "":
            x["logic"] = "True"
        x["logic"] = x["logic"].replace("|", ",")
        logic = f"lambda l: {x['logic']}"
        if x["placed"] == "":
            x["placed"] == "none"
        print(
            f"\t"+precomment+f"DoorData(name=\"{name}\", map=Maps.{x['map']}, logicregion=Regions.{x['logicregion']}, location=[{x['coords'][0]}, {x['coords'][1]}, {x['coords'][2]}, {x['coords'][3]}]{rx_text}{rz_text}, scale={x['scale']}{kongs_text}, group={x['group']}, logic={logic}, placed=\"{x['placed']}\", door_type=\"{x['door_type']}\"),{x['post_comment']}"
        )
    print("],")
