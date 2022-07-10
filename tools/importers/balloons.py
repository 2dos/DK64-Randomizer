"""Balloon importer from Bismuths Spreadsheet."""


with open("import.csv", newline="") as csvfile:
    dataset = []
    balloon = None
    map = None
    speed = None
    for row in csvfile:
        rowdata = row.replace("\r\n", "").split(",")
        newentry = {}
        if rowdata[0] != "" and rowdata[0] != balloon:
            balloon = rowdata[0]
            speed = rowdata[1]
            map = rowdata[2]
            dataset.append({"balloon": int(balloon), "map": map, "speed": int(speed), "path": []})

        newentry["order"] = int(rowdata[3])
        newentry["x"] = int(float(rowdata[4]))
        newentry["y"] = int(float(rowdata[5]))
        newentry["z"] = int(float(rowdata[6]))
        dict_index = next((index for (index, d) in enumerate(dataset) if d["balloon"] == int(balloon)), None)
        dataset[dict_index]["path"].append(newentry)
    print(dataset)
