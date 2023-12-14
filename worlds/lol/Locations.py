from typing import Dict, NamedTuple, Optional
from .Data import items
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
for item_id in items:
    location_table[items[item_id]]  = LOLLocationData("Progression", 566_0000 + int(item_id))
location_table["Starting Item 1"]   = LOLLocationData("Starting"   , 566_0001)
location_table["Starting Item 2"]   = LOLLocationData("Starting"   , 566_0002)
location_table["Starting Item 3"]   = LOLLocationData("Starting"   , 566_0003)
location_table["Starting Item 4"]   = LOLLocationData("Starting"   , 566_0004)
location_table["Starting Item 5"]   = LOLLocationData("Starting"   , 566_0005)
location_table["Starting Item 6"]   = LOLLocationData("Starting"   , 566_0006)
location_table["Starting Item 6"]   = LOLLocationData("Starting"   , 566_0007)
location_table["Starting Item 6"]   = LOLLocationData("Starting"   , 566_0008)
location_table["Starting Item 6"]   = LOLLocationData("Starting"   , 566_0009)
location_table["Starting Item 6"]   = LOLLocationData("Starting"   , 566_0010)

event_location_table: Dict[str, LOLLocationData] = {
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in location_table.items() if data.code}