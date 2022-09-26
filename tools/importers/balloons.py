"""Balloon importer from Bismuths Spreadsheet."""


def convertTruthiness(truth_string):
    """Convert Excel truth strings to boolean."""
    if truth_string == "TRUE":
        return True
    return False


with open("import.csv", newline="") as csvfile:
    dataset = []
    balloon = None
    name = None
    map = None
    speed = None
    kongs = {}
    for row_index, row in enumerate(csvfile):
        if row_index >= 2:
            rowdata = row.replace("\r\n", "").split(",")
            newentry = {}
            if rowdata[15] != "" and rowdata[15] != balloon:
                balloon = rowdata[15]
                name = rowdata[16]
                speed = rowdata[17]
                map = rowdata[18]
                kongs = {
                    "dk": convertTruthiness(rowdata[23]),
                    "diddy": convertTruthiness(rowdata[24]),
                    "lanky": convertTruthiness(rowdata[25]),
                    "tiny": convertTruthiness(rowdata[26]),
                    "chunky": convertTruthiness(rowdata[27]),
                }
                dataset.append({"balloon": int(balloon), "map": map, "name": name, "speed": int(speed), "kongs": kongs, "path": []})
            if rowdata[19] != "":
                newentry["order"] = int(rowdata[19])
                newentry["x"] = int(float(rowdata[20]))
                newentry["y"] = int(float(rowdata[21]))
                newentry["z"] = int(float(rowdata[22]))
                dict_index = next((index for (index, d) in enumerate(dataset) if d["balloon"] == int(balloon)), None)
                dataset[dict_index]["path"].append(newentry)
with open("balloons.txt", "w") as outputfile:
    for bln_data in dataset:
        kong_lst = []
        for kong in bln_data["kongs"]:
            if bln_data["kongs"][kong]:
                if kong == "dk":
                    kong = "donkey"
                kong_lst.append(f"Kongs.{kong}")
        points = []
        for pt in bln_data["path"]:
            points.append([pt["order"], pt["x"], pt["y"], pt["z"]])
        if len(points) > 0:
            points.append("&nbsp;")
        translation = {39: None}
        outputfile.write(
            f"Balloon(id={bln_data['balloon']}, map_id=Maps.{bln_data['map']}, name=\"{bln_data['name']}\", speed={bln_data['speed']}, konglist={str(kong_lst).translate(translation)}, region=\"\", points={str(points)}),\n".replace(
                " '&nbsp;'", ""
            )
        )
