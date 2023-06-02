"""Task file to run functions in the background via webworkers."""
import json
import uuid
import js
import time


def background(body):
    """Background a function via a webworker.

    This is a fully isolated function, you can not access the UIs DOM.

    Args:
        function (func): The function we run after backgrounding.
        args (list): List of args to pass to the function.
        returning_func (func): Function to run once we complete the main function.
    """
    if js.location.hostname == "dev.dk64randomizer.com" or js.location.hostname == "dk64randomizer.com":
        branch = "dev"
        if "dev" not in str(js.location.hostname).lower():
            branch = "master"
            url = "https://generate.dk64rando.com/generate"
        else:
            url = "https://generate.dk64rando.com/generate"
    else:
        url = "http://" + str(js.window.location.hostname) + ":5000/generate"
        branch = "dev"
    # Get the current time in milliseconds so we can use it as a key for the future.
    current_time = str(time.time()) + str(uuid.uuid1())
    url = url + "?gen_key=" + current_time
    js.generate_seed(url, json.dumps(body), branch)
