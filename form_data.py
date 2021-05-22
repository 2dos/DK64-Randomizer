"""Builds the default page."""
from browser.template import Template
from rando_options import Randomizers
from level_progression import LevelProgression
from misc import Misc

randos = Randomizers()
progression = LevelProgression()
misc = Misc()

Template("random_tab").render(randos=randos)
Template("level_progression_tab").render(progression=progression)
Template("misc_tab").render(misc=misc)
Template("spoiler_tab").render()
