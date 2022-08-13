"""File which generates a basic HTML tracker table for your seed."""
import js
import json


def generateTracker(spoilerJson):
    """Use the tracker template and spoiler data to generate a basic tracker."""
    tracker = js.getFile("./TrackerTemplate.html")
    spoiler = json.loads(spoilerJson)

    header = "<!--Start Generated Content-->"

    start = tracker.index(header) + len(header)

    generated = "\n"
    generated += "<h4>Seed: " + spoiler["Settings"]["Seed"] + "</h4>\n"

    if "Locations" in spoiler:
        generated += "<h3>Locations</h3>\n"
        generated += "<table>\n"
        i = 0
        for location, item in spoiler["Locations"].items():
            generated += "<tr>\n"
            generated += '<td id="loc_' + str(i) + '">' + location + "</td>\n"
            generated += '<td class="check-cell"><input id="itemCheck_' + str(i) + '" type="checkbox" onclick="showRow(\'item\', ' + str(i) + ')"/></td>\n'
            generated += '<td id="item_' + str(i) + '" class="spoiler">' + item + "</td>\n"
            generated += "</tr>\n"
            i += 1
        generated += "</table>\n"
        generated += '<input type="hidden" id="locCount" value="' + str(i) + '">'
    else:
        generated += '<input type="hidden" id="locCount" value="0">'

    if "Shuffled Exits" in spoiler:
        generated += "<h3>Exits</h3>\n"
        generated += "<table>\n"
        i = 0
        for front, back in spoiler["Shuffled Exits"].items():
            generated += "<tr>\n"
            generated += '<td id="front_' + str(i) + '">' + front + "</td>\n"
            generated += '<td class="check-cell"><input id="backCheck_' + str(i) + '" type="checkbox" onclick="showRow(\'back\', ' + str(i) + ')"/></td>\n'
            generated += '<td id="back_' + str(i) + '" class="spoiler">' + back + "</td>\n"
            generated += "</tr>\n"
            i += 1
        generated += "</table>\n"
        generated += '<input type="hidden" id="exitCount" value="' + str(i) + '">'
    else:
        generated += '<input type="hidden" id="exitCount" value="0">'

    tracker = tracker[:start] + generated + tracker[start:]

    return tracker
