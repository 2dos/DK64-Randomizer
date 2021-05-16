"""Create the flask endpoints for form viewing."""
import json
import os

from flask import Blueprint, Response, render_template, request

from static.level_progression import LevelProgression
from static.misc import Misc
from seed_generator import apply_asm

Version = 0.2
urls_blueprint = Blueprint("urls", __name__)


@urls_blueprint.route("/", methods=["GET", "POST"])
def index():
    """Index Page.

    Returns:
        render_template: Flask form.
    """
    if request.method == "POST":
        # TODO: Store this as a cookie rather than in a file
        converted_settings = dict(request.form)
        del converted_settings["seed"]
        with open("settings.json", "w") as outfile:
            json.dump(converted_settings, outfile)

        return Response(status=200, mimetype="application/json")
    return render_template("index.html", version=Version, progression=LevelProgression(), misc=Misc())


@urls_blueprint.route("/asm_patch", methods=["POST"])
def asm_patch():
    """Apply the ASM patch.

    Returns:
        Response: 200 status code.
    """
    return Response(response=apply_asm(dict(request.form)["asm"]), status=200, mimetype="application/json")


@urls_blueprint.route("/load_settings", methods=["GET"])
def load_settings():
    """Load settings from a file or load defaults.

    Returns:
        Response: JSON Response.
    """
    try:
        with open("settings.json") as f:
            return Response(response=f.readlines(), status=200, mimetype="application/json")
    except Exception:
        if os.path.exists("settings.json"):
            os.remove("settings.json")
    return "None"
