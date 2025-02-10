"""Main web endpoint API calls for the bot."""

import json
import os
import requests
import logging

logger = logging.getLogger(__name__)


class DK64:
    """Class for interacting with dk64randomizer.com to generate seeds and available presets."""

    hash_map = {
        0: {"Bongos": 908522167522709545},
        1: {"Crown": 1160363625723199600},
        2: {"RaceCoin": 1160363626645962872},
        3: {"Fairy": 1160363628369817682},
        4: {"Guitar": 908522167338139689},
        5: {"NintendoCoin": 1160363629422592111},
        6: {"Orange": 1160363630638936074},
        7: {"RainbowCoin": 1160363632337625098},
        8: {"RarewareCoin": 1160363633314893865},
        9: {"Saxophone": 908522167296208956},
    }

    def __init__(self):
        """Initialize the API class."""
        self.dev_seed_url = "https://dev.dk64randomizer.com/randomizer?seed_id=%s"
        self.live_seed_url = "https://dk64randomizer.com/randomizer?seed_id=%s"
        self.seed_endpoint = "https://api.dk64rando.com/api/submit-task?branch=%s"
        self.json_converter = "https://api.dk64rando.com/api/convert_settings?branch=%s"
        self.preset_endpoint = "https://api.dk64rando.com/api/get_presets?return_blank=false&branch=%s"
        self.data_endpoint = "https://api.dk64rando.com/api/get_seed?hash=%s"
        self.status_endpoint = "https://api.dk64rando.com/api/task-status/%s"

        self.discord_webhook = os.environ.get("DISCORD_WEBHOOK", None)
        self.api_key = os.environ.get("DK64_API_KEY", None)
        self.load_presets()

    def load_presets(self):
        """Load and return available seed presets."""
        for branch in ["stable", "dev"]:
            try:
                resp = requests.get(self.preset_endpoint % branch, headers={"x-api-key": self.api_key})
                presets = resp.json()
                logger.info(f"Loaded {len(presets)} {branch} presets.")
            except Exception as e:
                logger.error(f"Failed to load {branch} presets: {e}")
                presets = []
            # turn the presets into a dict of name being the key with the settings_string as the value
            presets_dict = {}
            for preset in presets:
                presets_dict[preset["name"].lower()] = preset
            setattr(self, f"{branch}_presets", presets_dict)

    def roll_seed(self, preset, race, password, spoiler):
        """Generate a seed and return its public URL."""
        # Roll with provided preset for non-draft races.
        self.load_presets()
        presets = []
        if race:
            presets = self.master_presets
            branch = "stable"
            logger.info("Rolling Stable Seed")
        else:
            presets = self.dev_presets
            branch = "dev"
            logger.info("Rolling Dev Seed")
        if preset is not None:
            converted_settings = requests.post(
                self.json_converter % branch,
                json.dumps({"settings": presets[preset]["settings_string"]}),
                headers={"Content-Type": "application/json", "x-api-key": self.api_key},
            )
            converted_settings = converted_settings.json()
            logger.info(f"Converted settings for preset {preset} for {branch} branch.")
            if spoiler:
                converted_settings["generate_spoilerlog"] = True
            else:
                converted_settings["generate_spoilerlog"] = False
            if password:
                converted_settings["has_password"] = True
            else:
                converted_settings["has_password"] = False
            req_body = {"settings_data": json.dumps(converted_settings)}
            data = requests.post(
                self.seed_endpoint % branch,
                headers={"Content-Type": "application/json", "x-api-key": self.api_key},
                json=req_body,
            ).json()
            logger.info(f"Rolled seed with preset {preset} for {branch} branch.")
            logger.info(f"Seed ID: {data['task_id']}")
            data["id"] = data["task_id"]
            return data["task_id"]
        else:
            logger.error("No preset provided.")
        return None, None

    def get_status(self, seed_id):
        """Get the status of a seed."""
        data = requests.get(
            self.status_endpoint % seed_id,
            headers={"x-api-key": self.api_key},
        )
        logger.info(f"Checking status of seed {seed_id}")
        logger.info(f"Status: {data.json()['status']}")
        if data.status_code == 200 and data.json()["status"] in ["failure", "stopped", "error"] or data.json().get("error", False):
            return 2, data
        elif data.status_code == 200 and data.json()["status"] == "finished":
            return 1, data
        else:
            return 0, data
