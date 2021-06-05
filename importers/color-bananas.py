"""Color Banana importer from Bismuths Spreadsheet."""


with open("import.csv", newline="") as csvfile:
    dataset = []
    group = None
    map = None
    kongs = {}
    for row in csvfile:
        rowdata = row.replace("\r\n", "").split(",")
        newentry = {}
        if rowdata[0] != "" and rowdata[0] != group:
            group = rowdata[0]
            map = rowdata[1]
            kongs = {
                "dk": False if rowdata[7] == "FALSE" else True,
                "diddy": False if rowdata[8] == "FALSE" else True,
                "lanky": False if rowdata[9] == "FALSE" else True,
                "tiny": False if rowdata[10] == "FALSE" else True,
                "chunky": False if rowdata[11] == "FALSE" else True,
            }
            dataset.append({"group": int(group), "map": map, "kongs": kongs, "locations": [], "size": int(0)})

        newentry["amount"] = int(rowdata[2])
        newentry["x"] = int(float(rowdata[4]))
        newentry["y"] = int(float(rowdata[5]))
        newentry["z"] = int(float(rowdata[6]))
        dict_index = next((index for (index, d) in enumerate(dataset) if d["group"] == int(group)), None)
        dataset[dict_index]["locations"].append(newentry)
        dataset[dict_index]["size"] += newentry["amount"]
    print(dataset)
