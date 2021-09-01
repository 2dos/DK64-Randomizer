"""Data objects for data management."""
from browser import document, html
import os


class GoldenBanana:
    """Golden Banana location/Collected status."""

    def __init__(self, name: str, **kwargs):
        """Init the golden banana location with the name and any args accepted.

        Args:
            name (str): Name of the location

        Raises:
            Exception: If the attribute passed from kwargs does not exist.
        """
        self.name = name
        self.collected = False
        self.slam = 0
        self.cranky()
        self.frees()
        self.guns()
        self.instruments()
        self.pickup()
        self.shared_moves()
        self.key_requirements()
        self.lobby_location()
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise Exception("Attribute does not exist")

    def __str__(self):
        """Get the string.

        Returns:
            str: returns a string of the GB location.
        """
        return self.name

    def __repr__(self):
        """Get the string.

        Returns:
            str: returns a string of the GB location.
        """
        return self.name

    def cranky(self, dk=0, diddy=0, chunky=0, lanky=0, tiny=0):
        """Set Cranky data 0-3 on how many cranky upgrades they have.

        Args:
            dk (int, optional): dk. Defaults to 0.
            diddy (int, optional): diddy. Defaults to 0.
            chunky (int, optional): chunky. Defaults to 0.
            lanky (int, optional): lanky. Defaults to 0.
            tiny (int, optional): tiny. Defaults to 0.
        """
        self.dk_cranky = dk
        self.diddy_cranky = diddy
        self.chunky_cranky = chunky
        self.lanky_cranky = lanky
        self.tiny_cranky = tiny

    def frees(self, dk=False, diddy=False, chunky=False, lanky=False, tiny=False):
        """Define if a kong is freed from this banana.

        Args:
            dk (bool, optional): dk. Defaults to False.
            diddy (bool, optional): diddy. Defaults to False.
            chunky (bool, optional): chunky. Defaults to False.
            lanky (bool, optional): lanky. Defaults to False.
            tiny (bool, optional): tiny. Defaults to False.
        """
        self.frees_dk = dk
        self.frees_diddy = diddy
        self.frees_chunky = chunky
        self.frees_lanky = lanky
        self.frees_tiny = tiny

    def guns(self, dk=False, diddy=False, chunky=False, lanky=False, tiny=False):
        """Define if the golden banana requires a gun unlock from a kong.

        Args:
            dk (bool, optional): dk. Defaults to False.
            diddy (bool, optional): diddy. Defaults to False.
            chunky (bool, optional): chunky. Defaults to False.
            lanky (bool, optional): lanky. Defaults to False.
            tiny (bool, optional): tiny. Defaults to False.
        """
        self.dk_gun = dk
        self.diddy_gun = diddy
        self.chunky_gun = chunky
        self.lanky_gun = lanky
        self.tiny_gun = tiny

    def instruments(self, dk=False, diddy=False, chunky=False, lanky=False, tiny=False):
        """Define if the golden banana requires an instrument to unlock.

        Args:
            dk (bool, optional): dk. Defaults to False.
            diddy (bool, optional): diddy. Defaults to False.
            chunky (bool, optional): chunky. Defaults to False.
            lanky (bool, optional): lanky. Defaults to False.
            tiny (bool, optional): tiny. Defaults to False.
        """
        self.dk_instrument = dk
        self.diddy_instrument = diddy
        self.chunky_instrument = chunky
        self.lanky_instrument = lanky
        self.tiny_instrument = tiny

    def pickup(self, dk=False, diddy=False, chunky=False, lanky=False, tiny=False):
        """Define what kong can pickup the banana.

        Args:
            dk (bool, optional): dk. Defaults to False.
            diddy (bool, optional): diddy. Defaults to False.
            chunky (bool, optional): chunky. Defaults to False.
            lanky (bool, optional): lanky. Defaults to False.
            tiny (bool, optional): tiny. Defaults to False.
        """
        self.dk_pickup = dk
        self.diddy_pickup = diddy
        self.chunky_pickup = chunky
        self.lanky_pickup = lanky
        self.tiny_pickup = tiny

    def shared_moves(self, barrel=False, dive=False, homing=False, orange=False, sniper=False, vine=False):
        """Define if a shared move is required to pick up the golden banana.

        Args:
            barrel (bool, optional): barrel. Defaults to False.
            dive (bool, optional): dive. Defaults to False.
            homing (bool, optional): homing. Defaults to False.
            orange (bool, optional): orange. Defaults to False.
            sniper (bool, optional): sniper. Defaults to False.
            vine (bool, optional): vine. Defaults to False.
        """
        self.barrel = barrel
        self.dive = dive
        self.homing = homing
        self.orange = orange
        self.sniper = sniper
        self.vine = vine

    def key_requirements(
        self, key1=False, key2=False, key3=False, key4=False, key5=False, key6=False, key7=False, key8=False
    ):
        """Define if a key is required to get this banana.

        Args:
            key1 (bool, optional): key1. Defaults to False.
            key2 (bool, optional): key2. Defaults to False.
            key3 (bool, optional): key3. Defaults to False.
            key4 (bool, optional): key4. Defaults to False.
            key5 (bool, optional): key5. Defaults to False.
            key6 (bool, optional): key6. Defaults to False.
            key7 (bool, optional): key7. Defaults to False.
            key8 (bool, optional): key8. Defaults to False.
        """
        self.key1 = key1
        self.key2 = key2
        self.key3 = key3
        self.key4 = key4
        self.key5 = key5
        self.key6 = key6
        self.key7 = key7
        self.key8 = key8

    def lobby_location(
        self,
        lobby1=False,
        lobby2=False,
        lobby3=False,
        lobby4=False,
        lobby5=False,
        lobby6=False,
        lobby7=False,
        lobby8=False,
    ):
        """Define if a golden banana is within a lobby area.

        Args:
            lobby1 (bool, optional): lobby1. Defaults to False.
            lobby2 (bool, optional): lobby2. Defaults to False.
            lobby3 (bool, optional): lobby3. Defaults to False.
            lobby4 (bool, optional): lobby4. Defaults to False.
            lobby5 (bool, optional): lobby5. Defaults to False.
            lobby6 (bool, optional): lobby6. Defaults to False.
            lobby7 (bool, optional): lobby7. Defaults to False.
            lobby8 (bool, optional): lobby8. Defaults to False.
        """
        self.lobby1 = lobby1
        self.lobby2 = lobby2
        self.lobby3 = lobby3
        self.lobby4 = lobby4
        self.lobby5 = lobby5
        self.lobby6 = lobby6
        self.lobby7 = lobby7
        self.lobby8 = lobby8


class ASMPatch:
    def __init__(self, asm_file: str, var_type: str, form_var: str, function=None, asm_start=[], **kwargs):
        self.asm_file = asm_file
        self.var_type = var_type.lower()
        self.form_var = form_var
        self.function = function
        self.asm_start = asm_start
        for key, value in kwargs.items():
            setattr(self, key, value)
        self._verify_asm_exists()

    def _verify_asm_exists(self):
        if not os.path.exists(f"./asm/{self.asm_file}.asm"):
            raise Exception("Source ASM file does not exist.")
        else:
            self.path = f"./asm/{self.asm_file}.asm"

    def generate_html(self):
        # Note: Requires self.content, self.title, self.enabled currently but does not actively check for them.
        if self.var_type == "checkbox":
            element = html.DIV(Class="form-check form-switch")
            label = html.LABEL(self.content, data_bs_toggle="tooltip", title=self.title)
            element <= label
            label <= html.INPUT(
                Class="form-check-input",
                type="checkbox",
                name=self.form_var,
                value="True",
                data_bs_toggle="tooltip",
                title=self.title,
                enabled=self.enabled,
            )
            document["body_data"] <= element
        elif self.var_type == "form-select":
            # TODO: Incomplete select
            element = html.div()
            element <= html.SELECT(self.content)
            document["body_data"] <= element

    def generate_asm(self, post_data: dict):
        asm = str()
        return_data = None
        with open(self.path, "r") as file:
            asm += file.read()
            asm += "\n"
        if self.function != None and post_data:
            asm, return_data = self.function(asm, post_data)
        return asm, return_data
