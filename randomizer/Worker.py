"""Task file to run functions in the background via webworkers."""
import json
import uuid
import js


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
        url = "https://dk64-seed-generator.adaptable.app/generate"
    else:
        url = "http://" + str(js.window.location.hostname) + ":5000/generate"
        branch = "dev"
    id = str(uuid.uuid1())
    js.generate_seed(url, json.dumps(body), branch, id)
