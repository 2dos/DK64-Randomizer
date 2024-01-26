"""Write the Krusha to apply the model changes."""

import json

with open("test.json", "r") as fh:
    test_vars = json.loads(fh.read())
    slot = -1
    if "krusha_slot" in test_vars:
        slot = test_vars["krusha_slot"]
        if slot == 0xFF:
            slot = -1
    with open("krusha_setting.txt", "w") as fg:
        fg.write(str(slot))
