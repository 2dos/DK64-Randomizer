"""Builds the default page."""
from browser.template import Template
from level_progression import LevelProgression
from misc import Misc


progression = LevelProgression()
misc = Misc()
Template("level_progression_tab").render(progression=progression)
Template("misc_tab").render(misc=misc)
Template("spoiler_tab").render()
