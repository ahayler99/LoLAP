from typing import Dict, List, NamedTuple, Optional

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import LOLLocation, location_table, get_locations_by_category
from .Data import items


class LOLRegionData(NamedTuple):
    locations: Optional[List[str]]
    region_exits: Optional[List[str]]


def create_regions(multiworld: MultiWorld, player: int):
    regions: Dict[str, LOLRegionData] = {
        "Menu":     LOLRegionData(None, ["Summoner's Rift"]),
        "Summoner's Rift":  LOLRegionData([], []),
    }

    # Set up locations

    for item_id in items:
        regions["Summoner's Rift"].locations.append("Win with " + str(items[item_id]))
    regions["Summoner's Rift"].locations.append("Starting Item 1")
    regions["Summoner's Rift"].locations.append("Starting Item 2")
    regions["Summoner's Rift"].locations.append("Starting Item 3")
    regions["Summoner's Rift"].locations.append("Starting Item 4")
    regions["Summoner's Rift"].locations.append("Starting Item 5")
    regions["Summoner's Rift"].locations.append("Starting Item 6")
    
    # Set up the regions correctly.
    for name, data in regions.items():
        multiworld.regions.append(create_region(multiworld, player, name, data))
    
    multiworld.get_entrance("Summoner's Rift", player).connect(multiworld.get_region("Summoner's Rift", player))


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
