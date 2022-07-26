static_dir = "../randomizer/"

with open(f"{static_dir}BaseHack.py","w") as pyfile:
    pyfile.write("\"\"\"List of variables in the base hack.\"\"\"\n")
    pyfile.write("\n")
    pyfile.write("def update_basehack_vars(self):\n")
    space_char = "    "
    pyfile.write(f"{space_char}\"\"\"Update Base Hack Variables.\"\"\"\n")
    with open(f"include/variable_space_structs.h","r") as hfile:
        vars = hfile.readlines()[1:-1]
        for var in vars:
            vardata = var.split(";")[0]
            varname = vardata.split(" ")[-1].strip()
            if "[" in varname:
                varname = varname.split("[")[0].strip()
            varoffset = vardata.split("*/")[0].split("/*")[1].strip()
            varline = f"{space_char}self.offsets_{varname} = {varoffset}\n"
            pyfile.write(varline)