"""Color Banana importer from Bismuths Spreadsheet."""


def convertTruthiness(truth_string):
    """Convert Excel truth strings to boolean."""
    if truth_string == "TRUE":
        return True
    return False


with open("import.csv", newline="") as csvfile:
    dataset = []
    group = None
    name = None
    map = None
    kongs = {}
    for row_index, row in enumerate(csvfile):
        if row_index >= 2:
            rowdata = row.replace("\r\n", "").split(",")
            newentry = {}
            if rowdata[0] != "" and rowdata[0] != group:
                group = rowdata[0]
                name = rowdata[1]
                map = rowdata[2]
                kongs = {
                    "dk": convertTruthiness(rowdata[9]),
                    "diddy": convertTruthiness(rowdata[10]),
                    "lanky": convertTruthiness(rowdata[11]),
                    "tiny": convertTruthiness(rowdata[12]),
                    "chunky": convertTruthiness(rowdata[13]),
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
    for cb_group in dataset:
        kong_lst = []
        for kong in cb_group["kongs"]:
            if cb_group["kongs"][kong]:
                if kong == "dk":
                    kong = "donkey"
                kong_lst.append(f"Kongs.{kong}")
        locations = []
        for loc in cb_group["locations"]:
            locations.append([loc["amount"], loc["scale"], loc["x"], loc["y"], loc["z"]])
        if len(locations) > 0:
            locations.append("&nbsp;")
        translation = {39: None}
        outputfile.write(
            f"ColoredBananaGroup(group={cb_group['group']}, map_id=Maps.{cb_group['map']}, name=\"{cb_group['name']}\", konglist={str(kong_lst).translate(translation)}, region=\"\", locations={str(locations)}),\n".replace(
                " '&nbsp;'", ""
            )
        )
