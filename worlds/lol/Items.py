from typing import Dict, NamedTuple, Optional
from .Data import sr_items, aram_items, arena_items

from BaseClasses import Item, ItemClassification


class LOLItem(Item):
    game: str = "League of Legends"


class LOLItemData(NamedTuple):
    category: str
    sub: str = "None"
    code: Optional[int] = None
    classification: ItemClassification = ItemClassification.filler
    max_quantity: int = 1
    weight: int = 1


def get_items_by_category(category: str, disclude: list) -> Dict[str, LOLItemData]:
    item_dict: Dict[str, LOLItemData] = {}
    for name, data in item_table.items():
        if data.category == category and all(x not in name for x in disclude):
            item_dict.setdefault(name, data)

    return item_dict


item_table: Dict[str, LOLItemData] = {}
for item_id in sr_items:
    item_table["SR " + sr_items[item_id]] = LOLItemData("GameMode(Summoners Rift)", code = 565_000000 + int(item_id), classification = ItemClassification.progression, max_quantity = 1, weight = 1)
for item_id in aram_items:
    item_table["ARAM " + aram_items[item_id]] = LOLItemData("GameMode(Aram)", code = 565_000000 + int(item_id), classification = ItemClassification.progression, max_quantity = 1, weight = 1)
for item_id in arena_items:
    item_table["ARENA " + arena_items[item_id]] = LOLItemData("GameMode(Arena)", code = 565_000000 + int(item_id), classification = ItemClassification.progression, max_quantity = 1, weight = 1)
item_table["Bronze Rank"]              = LOLItemData("Victory", code = 565_000001, classification = ItemClassification.progression, max_quantity = 1, weight = 1)
item_table["Silver Rank"]              = LOLItemData("Victory", code = 565_000002, classification = ItemClassification.progression, max_quantity = 1, weight = 1)
item_table["Gold Rank"]                = LOLItemData("Victory", code = 565_000003, classification = ItemClassification.progression, max_quantity = 1, weight = 1)
item_table["Platinum Rank"]            = LOLItemData("Victory", code = 565_000004, classification = ItemClassification.progression, max_quantity = 1, weight = 1)
item_table["Emerald Rank"]             = LOLItemData("Victory", code = 565_000005, classification = ItemClassification.progression, max_quantity = 1, weight = 1)
item_table["Diamond Rank"]             = LOLItemData("Victory", code = 565_000006, classification = ItemClassification.progression, max_quantity = 1, weight = 1)


event_item_table: Dict[str, LOLItemData] = {
}