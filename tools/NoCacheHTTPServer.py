"""Run a self hosted HTTP server that has no cache tied to it."""
import http.server

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


if __name__ == "__main__":
    http.server.test(HandlerClass=NoCacheHTTPRequestHandler, port=PORT)
