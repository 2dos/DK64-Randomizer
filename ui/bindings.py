"""Decorator function for UI elements to bind events to buttons."""
from functools import wraps
from pyodide import create_proxy

from js import document


def bind(event, id, iterations=0):
    """Bind a function to an event for a buttton.

    Args:
        event (str): Event to bind to eg: click
        id (str): ID of the element to bind to.
        iterations (int, optional): If we want to run this function multiple times with an increasing iteration. Defaults to 0.
    """

    def real_decorator(function):
        """Return the main decorator back this is the main response.

        Args:
            function (func): The original function.

        Returns:
            func: The original function to return.
        """
        function = create_proxy(function)
        if iterations == 0:
            document.getElementById(id).addEventListener(event, function, False)
        else:
            for i in range(0, iterations):
                try:
                    document.getElementById(id + str(i)).addEventListener(event, function)
                except Exception:
                    pass

        @wraps(function)
        def wrapper(*args, **kwargs):
            """Wrap our existing function with our passed function.

            Returns:
                func: The function to wrap.
            """
            retval = function(*args, **kwargs)
            return retval

        return wrapper

    return real_decorator
