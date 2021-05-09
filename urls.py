"""Create the flask endpoints for form viewing."""
import json
import random

from flask import Blueprint, Response, render_template, request

from level_progression import LevelProgression
from misc import Misc
from seed_generator import randomize

Version = 0.3
urls_blueprint = Blueprint("urls", __name__)


@urls_blueprint.route("/", methods=["GET", "POST"])
def index():
    """Index Page.

    Returns:
        render_template: Flask form.
    """
    if request.method == "POST":
        randomize(request.form)
        return render_template("completed.html", version=Version)
    return render_template(
        "index.html", version=Version, progression=LevelProgression(), random_seed=random_seed(), misc=Misc()
    )


@urls_blueprint.route("/random_seed", methods=["GET"])
def random_seed():
    """Random Seed Id.

    Returns:
        str: Random seed id.
    """
    return str(random.randint(100000, 999999))


@urls_blueprint.route("/blocker/<preset>")
def blocker_selected_preset(preset):
    """Return the preset for b-lockers.

    Args:
        preset (str): Preset name.

    Returns:
        Json: Json dump of the preset data.
    """
    presets = LevelProgression().blocker_presets()
    response = []
    for item in presets.Value:
        if item.get(preset):
            for val in item.get(preset):
                response.append(val)
    return Response(response=json.dumps(response), status=200, mimetype="application/json")


@urls_blueprint.route("/troff/<preset>")
def troff_selected_preset(preset):
    """Return the preset for troffnscoff.

    Args:
        preset (str): Preset Name.

    Returns:
        Json: Json dump of the preset data.
    """
    presets = LevelProgression().troff_presets()
    response = []
    for item in presets.Value:
        if item.get(preset):
            for val in item.get(preset):
                response.append(val)
    return Response(response=json.dumps(response), status=200, mimetype="application/json")
