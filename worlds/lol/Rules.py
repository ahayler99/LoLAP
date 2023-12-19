from BaseClasses import CollectionState, MultiWorld, LocationProgressType
from .Locations import get_locations_by_category
from .Data import sr_items, aram_items, arena_items

def has_item(state: CollectionState, player: int, item) -> bool:
    return state.has(item, player)

def set_rules(multiworld: MultiWorld, player: int, game_mode: str, items: list[str]):
    if game_mode == "GameMode(Summoners Rift)":
        for item_id in sr_items:
            if str(sr_items[item_id]) in items or len(items) == 0:
                multiworld.get_location("Win Summoners Rift with " + str(sr_items[item_id]), player).access_rule = lambda state: has_item(state, player, "SR " + sr_items[item_id])
    if game_mode == "GameMode(Aram)":
        for item_id in aram_items:
            if str(aram_items[item_id]) in items or len(items) == 0:
                multiworld.get_location("Win ARAM with " + str(aram_items[item_id]), player).access_rule = lambda state: has_item(state, player, "ARAM " + aram_items[item_id])
    if game_mode == "GameMode(Arena)":
        for item_id in arena_items:
            if str(arena_items[item_id]) in items or len(items) == 0:
                multiworld.get_location("Win Arena with " + str(arena_items[item_id]), player).access_rule = lambda state: has_item(state, player, "ARENA " + arena_items[item_id])
    
    # Win condition.
    multiworld.completion_condition[player] = lambda state: state.has_all({"Bronze Rank", "Silver Rank", "Gold Rank", "Platinum Rank", "Emerald Rank", "Diamond Rank"}, player)
