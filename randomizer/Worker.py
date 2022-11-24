"""Task file to run functions in the background via webworkers."""
import inspect
import json

import js


def background(function, args, returning_func):
    """Background a function via a webworker.

    This is a fully isolated function, you can not access the UIs DOM.

    Args:
        function (func): The function we run after backgrounding.
        args (list): List of args to pass to the function.
        returning_func (func): Function to run once we complete the main function.
    """
    module = inspect.getmodule(function)
    run_func = inspect.getsource(module)
    run_func += str(function.__name__) + "(" + ",".join(args) + ")"
    returning_mod = inspect.getmodule(returning_func)
    js.background_worker.postMessage(json.dumps({"func": run_func, "returning_func": "from " + returning_mod.__name__ + " import " + returning_func.__name__}))
