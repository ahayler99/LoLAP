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

class ItemNumber(Range):
    """
    How many items/locations should be included in the pool?
    """
    default = 30
    range_start = 10
    range_end = 60
    display_name = "Number of Items"

lol_options: Dict[str, type(Option)] = {
    "game_mode": GameMode,
    "item_num": ItemNumber,
}
