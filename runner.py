from flask import send_from_directory, Flask
import os
import sys
from swagger_ui import flask_api_doc

os.environ["WORKER_URL_DEV"] = "http://localhost:8000"
os.environ["TEST_REDIS"] = "1"
sys.path.append("worker")
sys.path.append("controller")

from worker.worker import api as worker_api
from controller.app import ALLOWED_REFERRERS, API_KEYS, api


app = Flask(__name__, static_folder="", template_folder="")
flask_api_doc(app, config_path='./controller/swagger.yaml', url_prefix='/api/doc', title='API doc')
app.register_blueprint(api)
app.register_blueprint(worker_api)


@app.route("/")
def index():
    """Serve the index page."""
    return send_from_directory(".", "index.html")


@app.route("/randomizer")
def rando():
    """Serve the randomizer page."""
    return send_from_directory(".", "randomizer.html")


ALLOWED_REFERRERS.extend(["*"])
API_KEYS.append("LOCAL_API_KEY")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, threaded=True, debug=True)
