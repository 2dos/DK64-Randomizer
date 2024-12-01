from flask import send_from_directory, Flask
import os

os.environ["WORKER_URL_DEV"] = "http://localhost:8000"
os.environ["TEST_REDIS"] = "1"
from threading import Thread
from fakeredis import TcpFakeServer

try:
    server = TcpFakeServer(("127.0.0.1", 6379), server_type="redis")
    t = Thread(target=server.serve_forever, daemon=True)
    t.start()
except Exception:
    pass

from worker.worker import api as worker_api
from controller.app import ALLOWED_REFERRERS, API_KEYS, api


app = Flask(__name__, static_folder="", template_folder="")
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
        