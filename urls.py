"""Create the flask endpoints for form viewing."""
import json
import os

from flask import Blueprint, Response, render_template, request

from static.level_progression import LevelProgression
from static.misc import Misc

Version = 0.2
urls_blueprint = Blueprint("urls", __name__)


@urls_blueprint.route("/", methods=["GET"])
def index():
    """Index Page.

    Returns:
        render_template: Flask form.
    """
    return render_template("index.html", version=Version, progression=LevelProgression(), misc=Misc())

