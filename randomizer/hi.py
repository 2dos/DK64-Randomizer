file = open('LogicFiles/AngryAztec.py', 'r')
output = ""

inquotes = False
prefix = ""
while True:
    char = file.read(1)
    if not char:
        break
    if char == " ":
        prefix = ""
    prefix += char
    if prefix == " LocationLogic(\"":
        inquotes = True
        output += "Locations."
        char = ""
    elif inquotes and char == "\"":
        char = ""
        inquotes = False
    if inquotes and char == " ":
        char = ""
    output += char

outfile = open('out.txt', 'w')
outfile.write(output)
outfile.close()
