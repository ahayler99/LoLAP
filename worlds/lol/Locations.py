from typing import Dict, NamedTuple, Optional
from .Data import sr_items, aram_items, arena_items
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
for item_id in sr_items:
    location_table["Win Summoners Rift with " + str(sr_items[item_id])]  = LOLLocationData("GameMode(Summoners Rift)", 5661_000000 + int(item_id))
for item_id in aram_items:
    location_table["Win ARAM with " + str(aram_items[item_id])]  = LOLLocationData("GameMode(Aram)", 5662_000000 + int(item_id))
for item_id in arena_items:
    location_table["Win Arena with " + str(arena_items[item_id])]  = LOLLocationData("GameMode(Arena)", 5663_000000 + int(item_id))
location_table["Starting Item 1"]   = LOLLocationData("Starting"   , 5660_000001)
location_table["Starting Item 2"]   = LOLLocationData("Starting"   , 5660_000002)
location_table["Starting Item 3"]   = LOLLocationData("Starting"   , 5660_000003)
location_table["Starting Item 4"]   = LOLLocationData("Starting"   , 5660_000004)
location_table["Starting Item 5"]   = LOLLocationData("Starting"   , 5660_000005)
location_table["Starting Item 6"]   = LOLLocationData("Starting"   , 5660_000006)

event_location_table: Dict[str, LOLLocationData] = {
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in location_table.items() if data.code}