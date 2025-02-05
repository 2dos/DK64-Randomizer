"""Backebd for RandoBot."""

from asyncio import sleep
import random
import requests
import logging
from racetime_bot import RaceHandler, monitor_cmd, can_moderate, can_monitor, msg_actions

logger = logging.getLogger(__name__)


class RandoHandler(RaceHandler):
    """RandoBot race handler. Generates seeds, presets, and frustration."""

    stop_at = ["cancelled", "finished"]
    max_status_checks = 50
    greetings = (
        "Let me roll a seed for you. I promise it won't hurt.",
        "I promise that today's seed will be nice.",
        "I can roll a race seed for you. If you dare.",
        "All rolled seeds comply with the laws of thermodynamics.",
    )

    def __init__(self, dk64, **kwargs):
        """Initialize the handler."""
        super().__init__(**kwargs)
        self.dk64 = dk64

    async def begin(self):
        """Send introduction messages."""
        if not self.state.get("intro_sent") and not self._race_in_progress():
            await self.send_message(
                "Welcome to DK64R! " + random.choice(self.greetings) + "THIS IS CURRENT IN DEV MODE ONLY. USE AT YOUR OWN RISK.",
                actions=[
                    # msg_actions.Action(
                    #     label="Roll Seed",
                    #     help_text="Create a seed using the latest release",
                    #     message="!seed '${preset}' ${--password} ${--spoiler}",
                    #     submit="Roll Race Seed",
                    #     survey=msg_actions.Survey(
                    #         msg_actions.SelectInput(
                    #             name="preset",
                    #             label="Preset",
                    #             options={key: value["name"] for key, value in self.dk64.master_presets.items()},
                    #         ),
                    #         msg_actions.BoolInput(name="--password", label="Password Protect", default=True),
                    #         msg_actions.BoolInput(name="--spoiler", label="Generate Spoiler Log", default=False),
                    #     ),
                    # ),
                    msg_actions.Action(
                        label="Roll Dev Seed",
                        help_text="Create a seed using the latest release and release a spoiler log",
                        message="!dev '${preset}' ${--password} ${--spoiler}",
                        submit="Roll Dev Seed",
                        survey=msg_actions.Survey(
                            msg_actions.SelectInput(
                                name="preset",
                                label="Preset",
                                options={key: value["name"] for key, value in self.dk64.dev_presets.items()},
                            ),
                            msg_actions.BoolInput(name="--password", label="Password Protect", default=False),
                            msg_actions.BoolInput(name="--spoiler", label="Generate Spoiler Log", default=False),
                        ),
                    ),
                    msg_actions.ActionLink(
                        label="Help",
                        url="https://github.com/2dos/dk64-randomizer/blob/dev/racetime_bot/COMMANDS.md",
                    ),
                ],
                pinned=True,
            )
            self.state["intro_sent"] = True
        if "locked" not in self.state:
            self.state["locked"] = False
        if "fpa" not in self.state:
            self.state["fpa"] = False

    async def end(self):
        """End the race and clean up any pinned messages."""
        if self.state.get("pinned_msg"):
            await self.unpin_message(self.state["pinned_msg"])

    async def chat_message(self, data):
        """Send a welcome message from the bot."""
        message = data.get("message", {})
        if message.get("is_bot") and message.get("bot") == "RandoBot" and message.get("is_pinned") and message.get("message_plain", "").startswith("Welcome to DK64R!"):
            self.state["pinned_msg"] = message.get("id")
        return await super().chat_message(data)

    async def race_data(self, data):
        """Set the race data and sunpin the welcome message."""
        await super().race_data(data)
        if self._race_in_progress() and self.state.get("pinned_msg"):
            await self.unpin_message(self.state["pinned_msg"])
            del self.state["pinned_msg"]

    @monitor_cmd
    async def ex_lock(self, args, message):
        """Handle !lock commands.

        Prevent seed rolling unless user is a race monitor.
        """
        if self._race_in_progress():
            return
        self.state["locked"] = True
        await self.send_message("Lock initiated. I will now only roll seeds for race monitors.")

    @monitor_cmd
    async def ex_unlock(self, args, message):
        """Handle !unlock commands.

        Remove lock preventing seed rolling unless user is a race monitor.
        """
        if self._race_in_progress():
            return
        self.state["locked"] = False
        await self.send_message("Lock released. Anyone may now roll a seed.")

    async def ex_seed(self, args, message):
        """Handle !seed commands."""
        if self._race_in_progress():
            return
        await self.roll_and_send(args, message)

    async def ex_dev(self, args, message):
        """Handle !dev commands."""
        if self._race_in_progress():
            return
        await self.roll_and_send(args, message)

    async def ex_presets(self, args, message):
        """Handle !presets commands."""
        if self._race_in_progress():
            return
        await self.send_presets(False)

    async def ex_fpa(self, args, message):
        """Free Play Agreement command for race mods."""
        if len(args) == 1 and args[0] in ("on", "off"):
            if not can_monitor(message):
                resp = "Sorry %(reply_to)s, only race monitors can do that."
            elif args[0] == "on":
                if self.state["fpa"]:
                    resp = "Fair play agreement is already activated."
                else:
                    self.state["fpa"] = True
                    resp = (
                        "Fair play agreement is now active. @entrants may "
                        "use the !fpa command during the race to notify of a "
                        "crash. Race monitors should enable notifications "
                        "using the bell 🔔 icon below chat."
                    )
            else:  # args[0] == 'off'
                if not self.state["fpa"]:
                    resp = "Fair play agreement is not active."
                else:
                    self.state["fpa"] = False
                    resp = "Fair play agreement is now deactivated."
        elif self.state["fpa"]:
            if self._race_in_progress():
                resp = "@everyone FPA has been invoked by @%(reply_to)s."
            else:
                resp = "FPA cannot be invoked before the race starts."
        else:
            resp = "Fair play agreement is not active. Race monitors may enable " "FPA for this race with !fpa on"
        if resp:
            reply_to = message.get("user", {}).get("name", "friend")
            await self.send_message(resp % {"reply_to": reply_to})

    async def roll_and_send(self, args, message):
        """Read an incoming !seed or !race command, and generate a new seed if valid."""
        reply_to = message.get("user", {}).get("name")

        if self.state.get("locked") and not can_monitor(message):
            await self.send_message("Sorry %(reply_to)s, seed rolling is locked. Only race " "monitors may roll a seed for this race." % {"reply_to": reply_to or "friend"})
            return
        if self.state.get("seed_id") and not can_moderate(message):
            await self.send_message("Well excuuuuuse me princess, but I already rolled a seed. " "Don't get greedy!")
            return
        # merge the args into a single string for parsing
        preset = " ".join(arg for arg in args if not arg.startswith("--")).replace("'", "").strip()
        password_protected = "--password" in args
        spoiler_log = "--spoiler" in args
        try:
            command = str(message.get("message", "").split(" ")[0]).lower()
        except Exception:
            command = ""
        if command == "!seed":
            race = True
        else:
            race = False
        await self.roll(preset=preset if args else "weekly", reply_to=reply_to, race=race, password_protected=password_protected, spoiler_log=spoiler_log)

    async def roll(self, preset, reply_to, race, password_protected, spoiler_log):
        """Generate a seed and send it to the race room."""
        if not race:
            if preset not in self.dk64.dev_presets:
                res_cmd = "!presets"
                await self.send_message("Sorry %(reply_to)s, I don't recognise that preset. Use " "%(res_cmd)s to see what is available." % {"res_cmd": res_cmd, "reply_to": reply_to or "friend"})
                return
        else:
            if preset not in self.dk64.master_presets:
                res_cmd = "!presets"
                await self.send_message("Sorry %(reply_to)s, I don't recognise that preset. Use " "%(res_cmd)s to see what is available." % {"res_cmd": res_cmd, "reply_to": reply_to or "friend"})
                return
        seed_id = self.dk64.roll_seed(preset, race, password_protected, spoiler_log)

        await self.send_message("%(reply_to)s, your seed is generating. Please wait..." % {"reply_to": reply_to or "Okay"})
        if self.state.get("pinned_msg"):
            await self.unpin_message(self.state["pinned_msg"])
            del self.state["pinned_msg"]

        self.state["seed_id"] = seed_id
        self.state["status_checks"] = 0
        self.state["preset"] = preset
        self.state["race"] = race
        await self.check_seed_status()

    async def check_seed_status(self):
        """Check the status of the seed generation."""
        await sleep(5)
        status, data = self.dk64.get_status(self.state["seed_id"])
        if status == 0:
            self.state["status_checks"] += 1
            if self.state["status_checks"] < self.max_status_checks:
                await self.check_seed_status()
            else:
                self.state["seed_id"] = None
                await self.send_message("Sorry, but it looks like the seed is taking too long to generate.")
        elif status == 1:
            self.state["result_data"] = data.json()["result"]
            await self.load_seed_hash()
        elif status >= 2:
            self.state["seed_id"] = None
            await self.send_message("Sorry, but it looks like the seed failed to generate. Use !seed to try again.")

    async def load_seed_hash(self):
        """When the seed is ready, get the data."""
        seed_hash, public_id = (
            " ".join([next(iter(self.dk64.hash_map.get(index, {}).keys()), next(iter(self.dk64.hash_map.values()))) for index in self.state["result_data"]["hash"]]),
            self.state["result_data"].get("seed_number"),
        )
        if self.state["race"]:
            url = self.dk64.master_seed_url
        else:
            url = self.dk64.dev_seed_url
        await self.set_bot_raceinfo(
            "%(seed_hash)s\n%(seed_url)s"
            % {
                "seed_hash": seed_hash,
                "seed_url": url % public_id,
            }
        )
        # Get the racetime room url
        embed_data = {
            "content": None,
            "embeds": [
                {
                    "title": "Race Opened - " + self.data.get("goal").get("name"),
                    "description": "---------------------------------------------------------",
                    "url": "https://racetime.gg" + str(self.data.get("url")),
                    "color": 7602008,
                    "fields": [
                        {
                            "name": "Seed Hash",
                            "value": " ".join(
                                [
                                    "<:{key}:{value}>".format(key=word, value=self.dk64.hash_map[key][word.strip()])
                                    for word in seed_hash.split()
                                    for key, value in self.dk64.hash_map.items()
                                    if word.strip() in value
                                ]
                            ),
                            "inline": True,
                        },
                        {"name": "Description", "value": self.data.get("info_user", "No description"), "inline": True},
                        {"name": "‎", "value": "‎", "inline": True},
                        {"name": "Preset Used", "value": self.state["preset"], "inline": True},
                        {
                            "name": "Race Opened By",
                            "value": self.data.get("opened_by", {}).get("full_name", "Unknown User"),
                            "inline": True,
                        },
                        {"name": "‎", "value": "‎", "inline": True},
                        {"name": "---------------------------------------------------------", "value": url % public_id},
                    ],
                    "footer": {"text": "Happy Donkin!"},
                    "thumbnail": {"url": "https://dk64randomizer.com/base-hack/assets/DKTV/logo.png"},
                }
            ],
            "username": "Racecar",
            "avatar_url": "https://mario.wiki.gallery/images/b/b3/DK64_Racecar.png",
            "attachments": [],
        }
        if self.dk64.discord_webhook and not self.data.get("unlisted", False):
            requests.post(self.dk64.discord_webhook, json=embed_data)
        logger.info("Password Selected? %s" % self.state["result_data"].get("password"))
        if self.state["result_data"].get("password"):
            logger.info("Result Send Message! Password: %(password)s" % {"password": self.state["result_data"]["password"]})
            # await self.send_message("Seed generated! Password: %(password)s" % {"password": self.state["result_data"]["password"]})
            # DM the password to the user
            await self.send_message(f"Seed generated! Password: {self.state['result_data']['password']}", direct_to=self.data.get("opened_by", {}).get("id"))

    async def send_presets(self, dev):
        """Send a list of known presets to the race room."""
        await self.send_message("Available presets:")
        if dev:
            for name, preset in self.dk64.dev_presets.items():
                await self.send_message("%s – %s" % (name, preset["name"]))
        else:
            for name, preset in self.dk64.master_presets.items():
                await self.send_message("%s – %s" % (name, preset["name"]))

    def _race_in_progress(self):
        """See if the race is in progress."""
        return self.data.get("status").get("value") in ("pending", "in_progress")
