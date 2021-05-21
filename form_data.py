"""Builds the default page."""
from browser.template import Template
from randomizers import Randomizers
from level_progression import LevelProgression
from misc import Misc

randomizers = Randomizers()
progression = LevelProgression()
misc = Misc()

Template("randomizers_tab").render(randomizers=randomizers)
Template("level_progression_tab").render(progression=progression)
Template("misc_tab").render(misc=misc)
Template("spoiler_tab").render()
