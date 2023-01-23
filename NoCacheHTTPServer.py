"""Run a self hosted HTTP server that has no cache tied to it."""
import http.server
from flask import Flask, Response, request
from flask_cors import CORS
from os.path import exists
from os import remove
import threading
import codecs
import json
import pickle
import random
from randomizer.Fill import Generate_Spoiler
from randomizer.Settings import Settings
from randomizer.Spoiler import Spoiler

app = Flask(__name__)
CORS(app, support_credentials=True)
PORT = 8000


class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """No cache response handler.

    Args:
        http (http.server.SimpleHTTPRequestHandler): Properly tacks on the headers we need to expire the files.
    """

    def send_response_only(self, code, message=None):
        """Tack on the headers and only send the response.

        Args:
            code (str): Code to send
            message (str, optional): Message to respond with. Defaults to None.
        """
        super().send_response_only(code, message)
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Expires", "0")


def generate_data(setting_data):
    """Generate a seed from a set of json data."""
    global seed_response
    settings = Settings(setting_data)
    spoiler = Spoiler(settings)
    Generate_Spoiler(spoiler)
    encoded = codecs.encode(pickle.dumps(spoiler), "base64").decode()
    seed_response = encoded


@app.route("/generate", methods=["POST", "GET"])
def generator():
    """Web events for generating seeds peers the actual web app."""
    if request.method == "POST":
        global seed_response
        seed_response = None
        setting_data = json.loads(str(request.json.get("post_body")))
        if not setting_data.get("seed"):
            setting_data["seed"] = random.randint(0, 100000000)
        threading.Thread(target=generate_data, args=[setting_data]).start()
        return "Build Started", 201
    else:
        if not seed_response:
            if exists("error.log"):
                with open("error.log", "r") as file_object:
                    content = file_object.read()
                remove("error.log")
                return content, 400
            else:
                return "Pending", 425
        else:
            return Response(seed_response, mimetype="text/plain", direct_passthrough=True)


def start_webserver():
    """Start the standard web server."""
    http.server.test(HandlerClass=NoCacheHTTPRequestHandler, port=PORT)


if __name__ == "__main__":
    threading.Thread(target=start_webserver).start()
    app.run(debug=True)
