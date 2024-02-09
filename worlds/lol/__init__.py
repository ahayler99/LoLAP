from typing import List

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import LOLItem, LOLItemData, event_item_table, get_items_by_category, item_table
from .Locations import LOLLocation, location_table, get_locations_by_category
from .Options import LOLOptions
from .Regions import create_regions
from .Rules import set_rules
from .Data import champions
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
    options_dataclass = LOLOptions
    options: LOLOptions
    topology_present = True
    required_client_version = (0, 3, 5)
    web = LOLWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}

    def create_items(self):
        print(self.options.champions.value)
        possible_champions = []
        for champion_id in champions:
            champion_name = champions[champion_id]["name"]
            if champion_name in self.options.champions.value:
                possible_champions.append(champion_name)
        starting_champions = random.sample(possible_champions, min(self.options.starting_champions, len(self.options.champions.value)))
        for i in range(len(starting_champions)):
            self.multiworld.get_location("Starting Champion " + str(i+1), self.player).place_locked_item(self.create_item(starting_champions[i]))
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        item_pool: List[LOLItem] = []
        for name, data in item_table.items():
            if name in possible_champions and name != starting_champion:
                item_pool += [self.create_item(name) for _ in range(0, 1)]
        while len(item_pool) < total_locations:
            item_pool.append(self.create_item("LP"))
        self.multiworld.itempool += item_pool
        
    def create_item(self, name: str) -> LOLItem:
        data = item_table[name]
        return LOLItem(name, data.classification, data.code, self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.player, self.options, int((len(self.multiworld.itempool) - len(self.options.champions.value)) * (self.options.required_lp / 100)))

    def create_regions(self):
        create_regions(self.multiworld, self.player, self.options)
    
    def fill_slot_data(self) -> dict:
        slot_data = {"Required CS":      int(self.options.required_creep_score)
                    ,"Required VS":      int(self.options.required_vision_score)
                    ,"Required Kills":   int(self.options.required_kills)
                    ,"Required Assists": int(self.options.required_assists)
                    ,"Required LP":      int(((len(self.multiworld.itempool)+1) - len(self.options.champions.value)) * (self.options.required_lp / 100))}
        return slot_data