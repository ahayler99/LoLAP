from typing import List

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import LOLItem, LOLItemData, event_item_table, get_items_by_category, item_table
from .Locations import LOLLocation, location_table, get_locations_by_category
from .Options import lol_options
from .Regions import create_regions
from .Rules import set_rules
from worlds.LauncherComponents import Component, components, Type, launch_subprocess
import random



def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="LOL Client")


components.append(Component("LOL Client", "LOLClient", func=launch_client, component_type=Type.CLIENT))

class LOLWeb(WebWorld):
    theme = "ocean"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the League of Legends AP Randomizer software on your computer. This guide covers single-player, "
        "multiworld, and related software.",
        "English",
        "lol_en.md",
        "LOL/en",
        ["Gicu"]
    )]

class LOLWorld(World):
    """
    League of Legends (LoL), commonly referred to as League, is a 2009 multiplayer online battle arena video game developed and published by Riot Games.
    """
    game = "League of Legends"
    option_definitions = lol_options
    topology_present = True
    data_version = 4
    required_client_version = (0, 3, 5)
    web = LOLWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}

    # TODO: Replace calls to this function with "options-dict", once that PR is completed and merged.
    def get_setting(self, name: str):
        return getattr(self.multiworld, name)[self.player]

    def fill_slot_data(self) -> dict:
        return {option_name: self.get_setting(option_name).value for option_name in lol_options}

    def create_items(self):
        item_pool: List[LOLItem] = []
        
        for name, data in item_table.items():
            quantity = data.max_quantity
            item_pool += [self.create_item(name) for _ in range(0, quantity)]

        self.multiworld.itempool += item_pool

    def get_filler_item_name(self) -> str:
        fillers = {}
        disclude = []
        fillers.update(get_items_by_category("Item", disclude))
        weights = [data.weight for data in fillers.values()]
        return self.multiworld.random.choices([filler for filler in fillers.keys()], weights, k=1)[0]
        
    def create_item(self, name: str) -> LOLItem:
        data = item_table[name]
        return LOLItem(name, data.classification, data.code, self.player)

    def create_event(self, name: str) -> LOLItem:
        data = event_item_table[name]
        return LOLItem(name, data.classification, data.code, self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def create_regions(self):
        create_regions(self.multiworld, self.player)