"""File which generates a basic HTML tracker table for your seed."""
import json

import js


def generateTracker(spoiler):
    """Use the tracker template and spoiler data to generate a basic tracker."""
    tracker = js.getFile("./TrackerTemplate.html")

    header = "<!--Start Generated Content-->"

    start = tracker.index(header) + len(header)

    generated = "\n"
    generated += "<h4>Seed: " + spoiler["Settings"]["Seed"] + "</h4>\n"

    if "Items" in spoiler:
        locations = {}
        if "Kongs" in spoiler["Items"]:
            locations.update(spoiler["Items"]["Kongs"])
        if "Shops" in spoiler["Items"]:
            locations.update(spoiler["Items"]["Shops"])
        if "Other" in spoiler["Items"]:
            locations.update(spoiler["Items"]["Other"])
        generated += "<h3>Locations</h3>\n"
        generated += "<table>\n"
        i = 0
        for location, item in locations.items():
            generated += "<tr>\n"
            generated += '<td id="loc_' + str(i) + '">' + str(location) + "</td>\n"
            generated += '<td class="check-cell"><input id="itemCheck_' + str(i) + '" type="checkbox" onclick="showRow(\'item\', ' + str(i) + ')"/></td>\n'
            generated += '<td id="item_' + str(i) + '" class="spoiler">' + str(item) + "</td>\n"
            generated += "</tr>\n"
            i += 1
        generated += "</table>\n"
        generated += '<input type="hidden" id="locCount" value="' + str(i) + '">'
    else:
        generated += '<input type="hidden" id="locCount" value="0">'

    exits = {}
    if "Shuffled Exits" in spoiler:
        exits.update(spoiler["Shuffled Exits"])
    if "Shuffled Level Order" in spoiler:
        exits.update(spoiler["Shuffled Level Order"])
    if len(exits) > 0:
        generated += "<h3>Exits</h3>\n"
        generated += "<table>\n"
        i = 0
        for front, back in exits.items():
            generated += "<tr>\n"
            generated += '<td id="front_' + str(i) + '">' + str(front) + "</td>\n"
            generated += '<td class="check-cell"><input id="backCheck_' + str(i) + '" type="checkbox" onclick="showRow(\'back\', ' + str(i) + ')"/></td>\n'
            generated += '<td id="back_' + str(i) + '" class="spoiler">' + str(back) + "</td>\n"
            generated += "</tr>\n"
            i += 1
        generated += "</table>\n"
        generated += '<input type="hidden" id="exitCount" value="' + str(i) + '">'
    else:
        generated += '<input type="hidden" id="exitCount" value="0">'

    tracker = tracker[:start] + generated + tracker[start:]

    return tracker
