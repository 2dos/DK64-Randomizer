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
                "dk": rowdata[7],
                "diddy": rowdata[8],
                "lanky": rowdata[9],
                "tiny": rowdata[10],
                "chunky": rowdata[11],
            }
            dataset.append(
                {"group": group, "map": map, "kongs": kongs, "locations": []}
            )

        newentry["amount"] = rowdata[2]
        newentry["x"] = rowdata[4]
        newentry["y"] = rowdata[5]
        newentry["z"] = rowdata[6]
        dict_index = next(
            (index for (index, d) in enumerate(dataset) if d["group"] == group), None
        )
        dataset[dict_index]["locations"].append(newentry)
    print(dataset)
