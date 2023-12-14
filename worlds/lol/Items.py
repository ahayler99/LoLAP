from typing import Dict, NamedTuple, Optional
from .Data import items

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
for item_id in items:
    item_table[items[item_id]] = LOLItemData("Item", code = 565_0000 + int(item_id), classification = ItemClassification.progression, max_quantity = 1, weight = 1)
item_table["Bronze Rank"]              = LOLItemData("Item", code = 565_0001, classification = ItemClassification.progression, max_quantity = 1, weight = 1)
item_table["Silver Rank"]              = LOLItemData("Item", code = 565_0002, classification = ItemClassification.progression, max_quantity = 1, weight = 1)
item_table["Gold Rank"]                = LOLItemData("Item", code = 565_0003, classification = ItemClassification.progression, max_quantity = 1, weight = 1)
item_table["Platinum Rank"]            = LOLItemData("Item", code = 565_0004, classification = ItemClassification.progression, max_quantity = 1, weight = 1)
item_table["Emerald Rank"]             = LOLItemData("Item", code = 565_0005, classification = ItemClassification.progression, max_quantity = 1, weight = 1)
item_table["Diamond Rank"]             = LOLItemData("Item", code = 565_0006, classification = ItemClassification.progression, max_quantity = 1, weight = 1)


event_item_table: Dict[str, LOLItemData] = {
}