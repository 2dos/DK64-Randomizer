"""Test Runner Module for Local Running."""

from flask import send_from_directory, Flask
import os
import sys
from swagger_ui import flask_api_doc
import secrets

os.environ["WORKER_URL_DEV"] = "http://localhost:8000"
os.environ["TEST_REDIS"] = "1"
sys.path.append("worker")
sys.path.append("controller")
# Prepend all routes with /api

from worker.worker import api as worker_api  # noqa
from controller.app import ALLOWED_REFERRERS, API_KEYS, api  # noqa
from controller.app import admin_portal  # noqa


app = Flask(__name__, static_folder="", template_folder="templates")
flask_api_doc(app, config_path="./controller/swagger.yaml", url_prefix="/api/doc", title="API doc")
app.register_blueprint(api)
app.register_blueprint(worker_api)
secret_token = secrets.token_hex(256)

app.config["SECRET_KEY"] = secret_token


@app.route("/")
def index():
    """Serve the index page."""
    return send_from_directory(".", "index.html")


@app.route("/randomizer")
def rando():
    """Serve the randomizer page."""
    return send_from_directory(".", "randomizer.html")


@app.route("/privacy")
def privacy():
    """Serve the privacy page."""
    return send_from_directory(".", "privacy.html")


# Its a full function not a blueprint so we need to register it as a route
app.add_url_rule("/admin", view_func=admin_portal)

ALLOWED_REFERRERS.extend(["*"])
API_KEYS.append("LOCAL_API_KEY")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, threaded=True, debug=True)
