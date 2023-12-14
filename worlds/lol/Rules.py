from BaseClasses import CollectionState, MultiWorld, LocationProgressType
from .Locations import get_locations_by_category
from .Data import items

def has_item(state: CollectionState, player: int, item) -> bool:
    return state.has(item, player)

def set_rules(multiworld: MultiWorld, player: int):
    for item_id in items:
        multiworld.get_location("Win with " + str(items[item_id]), player).access_rule = lambda state: has_item(state, player, items[item_id])
    
    # Win condition.
    multiworld.completion_condition[player] = lambda state: state.has_all({"Bronze Rank", "Silver Rank", "Gold Rank", "Platinum Rank", "Emerald Rank", "Diamond Rank"}, player)
