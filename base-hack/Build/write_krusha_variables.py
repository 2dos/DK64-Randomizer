"""Write the Krusha to apply the model changes."""

import json

with open("test.json", "r") as fh:
    test_vars = json.loads(fh.read())
    slot = [0, 0, 0, 0, 0]
    if "kong_models" in test_vars:
        slot = test_vars["kong_models"]
    with open("krusha_setting.txt", "w") as fg:
        fg.write(" ".join(slot))
