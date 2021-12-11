"""Manage the progressbar of the UI."""
import js


class ProgressBar:
    """Management for the Progress Bar of the UI."""

    def __init__(self):
        """Control the function of the progressbar."""
        self.modal = "$('#progressmodal')"
        self.status = "$('#progress-text')"
        self.bar = "$('#patchprogress')"

    def update_progress(self, val: int, text: str):
        """Update your progress percentage and text.

        Args:
            val (int): Percent of 100.
            text (str): Text to display.
        """
        self.width(val)
        self.text(text)
        self.show()

    def reset(self):
        """Set hide, text, width and added classes of the progressbar to nil."""
        self.hide()
        self.text("")
        self.width(0)
        for css in js.document.getElementById("patchprogress").classList:
            if not "progress" in css:
                js.eval(self.bar + f".removeClass('{css}')")

    def width(self, val: int):
        """Set width to value converted to percentage.

        Args:
            val (int): Value percentage of 100.

        Raises:
            Exception: Raises an exception when number is outside 0-100
        """
        if not 0 <= val <= 100:
            raise Exception("Width can only be 0-100")
        quotient = val / 10
        percent = quotient * 100
        js.eval(self.bar + f".width('{percent}%')")

    def text(self, text: str):
        """Set the text of the progress bar.

        Args:
            text (str): Text to set.
        """
        js.eval(self.status + f".text('{text}')")

    def hide(self):
        """Hide the Modal."""
        js.eval(self.modal + ".modal('hide')")

    def show(self):
        """Show the Modal."""
        js.eval(self.modal + ".modal('show')")

    def set_class(self, css: str):
        """Add or Remove the CSS class defined.

        Args:
            css (str): Class to add.
        """
        if js.eval(self.bar + f".hasClass('{css}')"):
            js.eval(self.bar + f".removeClass('{css}')")
        else:
            js.eval(self.bar + f".addClass('{css}')")
