from typing import Dict

from Options import Choice, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionSet

class GameMode(Choice):
    """
    Select game mode to base items/location on.
    """
    display_name = "Game Mode"
    option_summoners_rift = 0
    option_aram = 1
    option_arena = 2
    default = 0

lol_options: Dict[str, type(Option)] = {
    "game_mode": GameMode
}
