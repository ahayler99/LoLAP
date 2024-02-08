from typing import Dict, List, NamedTuple, Optional

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import LOLLocation, location_table, get_locations_by_category
from .Data import champions


class LOLRegionData(NamedTuple):
    locations: Optional[List[str]]
    region_exits: Optional[List[str]]


def create_regions(multiworld: MultiWorld, player: int, options):
    regions: Dict[str, LOLRegionData] = {
        "Menu":     LOLRegionData(None, ["Match"]),
        "Match":  LOLRegionData([], []),
    }

    # Set up locations
    
    for champion_id in champions:
        champion_name = champions[champion_id]["name"]
        if champion_name in options.champions.value:
            regions["Match"].locations.append("Assist Taking Dragon as "      + champion_name)
            regions["Match"].locations.append("Assist Taking Rift Herald as " + champion_name)
            regions["Match"].locations.append("Assist Taking Baron as "       + champion_name)
            regions["Match"].locations.append("Assist Taking Tower as "       + champion_name)
            regions["Match"].locations.append("Assist Taking Inhibitor as "   + champion_name)
            regions["Match"].locations.append("Assist Taking Inhibitor as "   + champion_name)
            regions["Match"].locations.append("Get X Assists as "             + champion_name)
            if "Support" in champions[champion_id]["tags"]:
                regions["Match"].locations.append("Get X Ward Score as "      + champion_name)
            if "Support" not in champions[champion_id]["tags"]:
                regions["Match"].locations.append("Get X Kills as "           + champion_name)
                regions["Match"].locations.append("Get X Creep Score as "     + champion_name)
    regions["Match"].locations.append("Starting Champion")
    
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
