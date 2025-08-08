"""Verification script that there are no excluded settings with random settings."""

import os

excluded_templates = [
    "admin.html",
    "base.html",
    "cosmetics.html",
    "detailed_logic.html",
    "getting_started.html",
    "dropdown_multiselector.html",
    "lightswitch.html",
    "macros.html",
    "music.html",
    "nav-tabs.html",
    "settings.html",
    "spoiler.html",
    "spoiler_new.html",
]
template_files = [
    os.path.join("./templates", f) for f in os.listdir("./templates") if os.path.isfile(os.path.join("./templates", f)) and ".html" in os.path.join("./templates", f) and f not in excluded_templates
]


def parseToggleMacro(line: str) -> tuple:
    """Parse the jinja toggle macro and extract the setting data from it."""
    line = line.split("toggle_input(")[1]
    segments = line.split('"')
    setting = segments[1]
    name = segments[3]
    return (setting, name)


def parseSelect(lines: list[str], starting_index: int) -> tuple:
    """Parse a select tag and it's child object tags for setting data."""
    select_whole = ""
    excluded_lines = [starting_index]
    ref_idx = starting_index
    while True:
        if "</select>" in lines[ref_idx]:
            excluded_lines.append(ref_idx)
            select_whole += lines[ref_idx].strip()
            break
        excluded_lines.append(ref_idx)
        select_whole += lines[ref_idx].strip()
        ref_idx += 1
    if "name=" not in select_whole:
        print(f"No name for {select_whole}")
        return None, None, excluded_lines, []
    setting = select_whole.split('name="')[1].split('"')[0]
    if "display_name=" not in select_whole:
        name = setting.replace("_", " ").title()
    else:
        name = select_whole.split('display_name="')[1].split('"')[0]
    options = []
    if "<option" in select_whole:
        # Option parsing
        option_text = select_whole.split("<option")
        for x in option_text[1:]:
            if "value=" not in x:
                continue
            option_value = x.split('value="')[1].split('"')[0]
            option_name = x.split("</option>")[0].split(">")[-1]
            options.append({"name": option_name, "value": option_value})
    return setting, name, excluded_lines, options


settings = {}
for template in template_files:
    in_script = False
    with open(template, "r") as fh:
        lines = fh.readlines()
        excluded_lines = []
        for index, line in enumerate(lines):
            if "<script>" in line:
                in_script = True
                continue
            if "</script>" in line:
                in_script = False
                continue
            if in_script:
                continue
            if index in excluded_lines:
                continue
            if "{{ toggle_input(" in line:
                setting, name = parseToggleMacro(line)
                settings[setting] = {
                    "name": name,
                    "vartype": "bool",
                }
                continue
            if "<select" in line:
                setting, name, exclusions, options = parseSelect(lines, index)
                if setting is None:
                    continue
                settings[setting] = {"name": name, "vartype": "choice", "options": options}
                excluded_lines.extend(exclusions)
                continue
            # print(line)
print(settings)
