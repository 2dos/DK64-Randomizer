"""Color Banana importer from Bismuths Spreadsheet."""


with open("import.csv", newline="") as csvfile:
    dataset = []
    group = None
    name = None
    map = None
    kongs = {}
    for row in csvfile:
        rowdata = row.replace("\r\n", "").split(",")
        newentry = {}
        if rowdata[0] != "" and rowdata[0] != group:
            group = rowdata[0]
            name = rowdata[1]
            map = rowdata[2]
            kongs = {
                "dk": bool(int(rowdata[9])),
                "diddy": bool(int(rowdata[10])),
                "lanky": bool(int(rowdata[11])),
                "tiny": bool(int(rowdata[12])),
                "chunky": bool(int(rowdata[13])),
            }
            dataset.append({"group": int(group), "map": map, "name": name, "kongs": kongs, "locations": []})

        newentry["amount"] = int(rowdata[3])
        newentry["scale"] = float(rowdata[5])
        newentry["x"] = int(float(rowdata[6]))
        newentry["y"] = int(float(rowdata[7]))
        newentry["z"] = int(float(rowdata[8]))
        dict_index = next((index for (index, d) in enumerate(dataset) if d["group"] == int(group)), None)
        dataset[dict_index]["locations"].append(newentry)

with open("coloredbananas.txt", "w") as outputfile:
    outputfile.write(str(dataset))
