from BaseClasses import CollectionState, MultiWorld, LocationProgressType
from .Locations import get_locations_by_category
from .Data import champions

def has_item(state: CollectionState, player: int, item) -> bool:
    return state.has(item, player)

def has_at_least(state: CollectionState, player: int, item_name, item_qty_required) -> bool:
    return state.count(item_name, player) >= item_qty_required

def set_rules(multiworld: MultiWorld, player: int, options, required_lp):
    for champion_id in champions:
        champion_name = champions[champion_id]["name"]
        if champion_name in options.champions.value:
            multiworld.get_location("Assist Taking Dragon as "      + champion_name, player).access_rule = lambda state, champion_name = champion_name: has_item(state, player, champion_name)
            multiworld.get_location("Assist Taking Rift Herald as " + champion_name, player).access_rule = lambda state, champion_name = champion_name: has_item(state, player, champion_name)
            multiworld.get_location("Assist Taking Baron as "       + champion_name, player).access_rule = lambda state, champion_name = champion_name: has_item(state, player, champion_name)
            multiworld.get_location("Assist Taking Tower as "       + champion_name, player).access_rule = lambda state, champion_name = champion_name: has_item(state, player, champion_name)
            multiworld.get_location("Assist Taking Inhibitor as "   + champion_name, player).access_rule = lambda state, champion_name = champion_name: has_item(state, player, champion_name)
            multiworld.get_location("Assist Taking Inhibitor as "   + champion_name, player).access_rule = lambda state, champion_name = champion_name: has_item(state, player, champion_name)
            multiworld.get_location("Get X Assists as "             + champion_name, player).access_rule = lambda state, champion_name = champion_name: has_item(state, player, champion_name)
            if "Support" in champions[champion_id]["tags"]:
                multiworld.get_location("Get X Ward Score as "      + champion_name, player).access_rule = lambda state, champion_name = champion_name: has_item(state, player, champion_name)
            if "Support" not in champions[champion_id]["tags"]:
                multiworld.get_location("Get X Kills as "           + champion_name, player).access_rule = lambda state, champion_name = champion_name: has_item(state, player, champion_name)
                multiworld.get_location("Get X Creep Score as "     + champion_name, player).access_rule = lambda state, champion_name = champion_name: has_item(state, player, champion_name)
    
    # Win condition.
    multiworld.completion_condition[player] = lambda state: has_at_least(state, player, "LP", required_lp)
