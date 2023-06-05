"""Convert all script files to json files."""
import json
import os

folders = [x[0] for x in os.walk("./")]
for folder in folders:
    if folder != "./" and "__pycache__" not in folder:
        files = [x[2] for x in os.walk(folder)][0]
        for file in files:
            referenced_file = f"{folder}/{file}"
            if file != ".map" and ".script" in file:
                json_data = {
                    "id": 0,
                    "behav_9C": 0,
                    "ignore": False,
                    "output_version": 2,
                    "script": [],
                }
                rep_idx = 0
                replacement_bank = []
                with open(referenced_file, "r") as fh:
                    data = [x.replace("\n", "") for x in fh.readlines()]
                    mode = "none"
                    current_block = {
                        "conditions": [],
                        "executions": [],
                    }
                    for d in data:
                        if ".data" in d:
                            mode = "data"
                        elif ".code" in d:
                            mode = "code"
                        elif mode == "data":
                            attrs = d.split(" = ")
                            val = attrs[1]
                            if "x" in val:
                                val = int(val, 16)
                            else:
                                val = int(val)
                            json_data[attrs[0]] = val
                        elif mode == "code":
                            attrs = d.split(" ")
                            if attrs[0] in ("COND", "CONDINV"):
                                replacement_bank.append({"function": int(attrs[1]), "inverted": attrs[0] == "CONDINV", "parameters": [int(attrs[x + 3]) for x in range(3)]})
                                current_block["conditions"].append(f"rep_asdf_{rep_idx}")
                                rep_idx += 1
                            elif attrs[0] == "EXEC":
                                replacement_bank.append({"function": int(attrs[1]), "parameters": [int(attrs[x + 3]) for x in range(3)]})
                                current_block["executions"].append(f"rep_asdf_{rep_idx}")
                                rep_idx += 1
                            elif attrs[0] == "ENDBLOCK":
                                json_data["script"].append(current_block.copy())
                                current_block = {
                                    "conditions": [],
                                    "executions": [],
                                }
                json_file = referenced_file.replace(".script", ".json")
                with open(json_file, "w") as fh:
                    json.dump(json_data, fh, indent=4)
                data_str = ""
                with open(json_file, "r") as fh:
                    data_str = fh.read()
                replacement_bank.reverse()
                for index, new_str in enumerate(replacement_bank):
                    new_index = (len(replacement_bank) - 1) - index
                    data_str = data_str.replace(f"rep_asdf_{new_index}", json.dumps(new_str))
                with open(json_file, "w") as fh:
                    fh.write(data_str.replace('"{', "{").replace('}"', "}"))
                os.remove(referenced_file)
