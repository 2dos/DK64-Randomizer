"""Start the GUI Process for Flask."""
import os
import signal
import sys
import threading
import time
from pathlib import Path

import psutil
from flask import Flask
from flaskwebgui import FlaskUI  # import FlaskUI

# If this flag is set to true this flask app will only launch in a web format
app_mode = True

app = Flask(__name__, template_folder="/", static_folder="/", static_url_path="")
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
gui = FlaskUI(app=app, maximized=True, app_mode=app_mode, start_server="flask")


@app.route("/", methods=["GET"])
def index():
    """Index Page.

    Returns:
        render_template: Flask form.
    """
    html = open("./index.html", "r")
    data = html.read()
    html.close()
    return data


if __name__ == "__main__":

    def startup():
        """Start the flaskwebgui process."""
        gui.run()

    def signal_handler(sig, frame):
        """Terminate the flask process and gui.

        Args:
            sig (signal): Signal sent.
            frame (frame): Frame to terminate.
        """
        try:
            os.remove("lockfile")
        except Exception:
            pass
        try:
            gui.BROWSER_PROCESS.terminate()
        except Exception:
            pass
        try:
            os.kill(os.getpid(), signal.SIGINT)
        except Exception:
            pass

    signal.signal(signal.SIGINT, signal_handler)
    procObjList = [procObj for procObj in psutil.process_iter() if "python" in procObj.name().lower()]
    if os.path.isfile("lockfile"):
        print(len(procObjList))
        if len(procObjList) <= 1:
            try:
                os.remove("lockfile")
                os.execv(sys.executable, ["python"] + sys.argv)
            except Exception:
                pass
        sys.exit(1)
    else:
        Path("lockfile").touch()
        threading.Thread(target=startup).start()
        poll = None
        while poll is None:
            try:
                poll = gui.BROWSER_PROCESS
            except Exception:
                pass
        while True:
            if not psutil.pid_exists(poll.pid):
                signal_handler(None, None)
            time.sleep(1)
