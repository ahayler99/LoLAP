from typing import Dict, NamedTuple, Optional
from .Data import champions
import typing


from BaseClasses import Location


class LOLLocation(Location):
    game: str = "League of Legends"


class LOLLocationData(NamedTuple):
    category: str
    code: Optional[int] = None


def get_locations_by_category(category: str) -> Dict[str, LOLLocationData]:
    location_dict: Dict[str, LOLLocationData] = {}
    for name, data in location_table.items():
        if data.category == category:
            location_dict.setdefault(name, data)

    return location_dict


location_table: Dict[str, LOLLocationData] = {}
for champion_id in champions:
    champion_name = champions[champion_id]["name"]
    if "JUNGLE" in champions[champion_id]["tags"] or "BOTTOM" in champions[champion_id]["tags"] or "UTILITY" in champions[champion_id]["tags"]:
        location_table[champion_name + " - Assist Taking Dragon"]      = LOLLocationData("Objective", 566_000000 + (int(champion_id) * 100) + 1)
    if "JUNGLE" in champions[champion_id]["tags"] or "TOP" in champions[champion_id]["tags"]:
        location_table[champion_name + " - Assist Taking Rift Herald"] = LOLLocationData("Objective", 566_000000 + (int(champion_id) * 100) + 2)
    location_table[champion_name + " - Assist Taking Baron"]       = LOLLocationData("Objective", 566_000000 + (int(champion_id) * 100) + 3)
    if "JUNGLE" not in champions[champion_id]["tags"]:
        location_table[champion_name + " - Assist Taking Tower"]       = LOLLocationData("Objective", 566_000000 + (int(champion_id) * 100) + 4)
        location_table[champion_name + " - Assist Taking Inhibitor"]   = LOLLocationData("Objective", 566_000000 + (int(champion_id) * 100) + 5)
    if "UTILITY" in champions[champion_id]["tags"]:
        location_table[champion_name + " - Get X Assists"]             = LOLLocationData("Objective", 566_000000 + (int(champion_id) * 100) + 6)
        location_table[champion_name + " - Get X Ward Score"]      = LOLLocationData("Objective", 566_000000 + (int(champion_id) * 100) + 7)
    if "UTILITY" not in champions[champion_id]["tags"]:
        location_table[champion_name + " - Get X Kills"]           = LOLLocationData("Objective", 566_000000 + (int(champion_id) * 100) + 8)
        location_table[champion_name + " - Get X Creep Score"]     = LOLLocationData("Objective", 566_000000 + (int(champion_id) * 100) + 9)

location_table["Starting Champion 1"] = LOLLocationData("Starting", 566_000001)
location_table["Starting Champion 2"] = LOLLocationData("Starting", 566_000002)
location_table["Starting Champion 3"] = LOLLocationData("Starting", 566_000003)
location_table["Starting Champion 4"] = LOLLocationData("Starting", 566_000004)
location_table["Starting Champion 5"] = LOLLocationData("Starting", 566_000005)

event_location_table: Dict[str, LOLLocationData] = {
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in location_table.items() if data.code}