import requests
import json

versions_url = "https://ddragon.leagueoflegends.com/api/versions.json"
maps_url = "https://static.developer.riotgames.com/docs/lol/maps.json"
most_recent_version = requests.get(versions_url).json()[0]
items_url = "https://ddragon.leagueoflegends.com/cdn/" + str(most_recent_version) + "/data/en_US/item.json"
champions_url = "https://ddragon.leagueoflegends.com/cdn/" + str(most_recent_version) + "/data/en_US/champion.json"
items = {}
champions = {}
for map in requests.get(maps_url).json():
    if map["mapName"] == "Howling Abyss":
        map_id = map["mapId"]
item_data = requests.get(items_url).json()["data"]
for item_id in item_data.keys():
    if "into" not in item_data[item_id].keys() and item_data[item_id]["gold"]["purchasable"] and item_data[item_id]["gold"]["total"] > 1000 and "requiredAlly" not in item_data[item_id].keys():
        if item_data[item_id]["maps"][str(map_id)]:
            items[item_id] = item_data[item_id]["name"]
for i in range(3): #Doing this multiple times for items that transform multiple times
    for item_id in item_data.keys():
        if "specialRecipe" in item_data[item_id].keys():
            if str(item_data[item_id]["specialRecipe"]) in items.keys():
                del items[str(item_data[item_id]["specialRecipe"])]
                items[item_id] = item_data[item_id]["name"]
champion_data = requests.get(champions_url).json()["data"]
for champion in list(champion_data.keys()):
    champions[int(champion_data[champion]["key"])] = champion
print(json.dumps(champions, indent=2))
print(json.dumps(items, indent=2))
