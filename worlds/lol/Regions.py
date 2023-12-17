from typing import Dict, List, NamedTuple, Optional

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import LOLLocation, location_table, get_locations_by_category
from .Data import sr_items, aram_items, arena_items


class LOLRegionData(NamedTuple):
    locations: Optional[List[str]]
    region_exits: Optional[List[str]]


def create_regions(multiworld: MultiWorld, player: int, game_mode: str):
    regions: Dict[str, LOLRegionData] = {
        "Menu":     LOLRegionData(None, ["Match"]),
        "Match":  LOLRegionData([], []),
    }

    # Set up locations
    
    if game_mode == "GameMode(Summoners Rift)":
        for item_id in sr_items:
            regions["Match"].locations.append("Win Summoners Rift with " + str(sr_items[item_id]))
    if game_mode == "GameMode(Aram)":
        for item_id in aram_items:
            regions["Match"].locations.append("Win ARAM with " + str(aram_items[item_id]))
    if game_mode == "GameMode(Arena)":
        for item_id in arena_items:
            regions["Match"].locations.append("Win Arena with " + str(arena_items[item_id]))
    regions["Match"].locations.append("Starting Item 1")
    regions["Match"].locations.append("Starting Item 2")
    regions["Match"].locations.append("Starting Item 3")
    regions["Match"].locations.append("Starting Item 4")
    regions["Match"].locations.append("Starting Item 5")
    regions["Match"].locations.append("Starting Item 6")
    
    # Set up the regions correctly.
    for name, data in regions.items():
        multiworld.regions.append(create_region(multiworld, player, name, data))
    
    multiworld.get_entrance("Match", player).connect(multiworld.get_region("Match", player))


def create_region(multiworld: MultiWorld, player: int, name: str, data: LOLRegionData):
    region = Region(name, player, multiworld)
    if data.locations:
        for loc_name in data.locations:
            loc_data = location_table.get(loc_name)
            location = LOLLocation(player, loc_name, loc_data.code if loc_data else None, region)
            region.locations.append(location)

    if data.region_exits:
        for exit in data.region_exits:
            entrance = Entrance(player, exit, region)
            region.exits.append(entrance)

    return region
