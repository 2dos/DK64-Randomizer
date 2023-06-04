"""Run a self hosted HTTP server that has no cache tied to it."""
import http.server
import os
import sys
import threading

from waitress import serve

from runner import app

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


def start_webserver():
    """Start the standard web server."""
    http.server.test(HandlerClass=NoCacheHTTPRequestHandler, port=PORT)


def run_servers():
    """Start the web server and the flask server."""
    threading.Thread(target=start_webserver).start()
    app.debug = True
    # Verify the rom.z64 file exists.
    if not os.path.isfile("dk64.z64"):
        print("dk64.z64 not found, please place a dk64.z64 file in the root directory.")
        sys.exit(1)
    serve(app, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    run_servers()
