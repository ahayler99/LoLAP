import requests
import json

versions_url = "https://ddragon.leagueoflegends.com/api/versions.json"
maps_url = "https://static.developer.riotgames.com/docs/lol/maps.json"
most_recent_version = requests.get(versions_url).json()[0]
items_url = "https://ddragon.leagueoflegends.com/cdn/" + str(most_recent_version) + "/data/en_US/item.json"
items = {}
for map in requests.get(maps_url).json():
    if map["mapName"] == "Summoner's Rift" and map["notes"] == "Current Version":
        map_id = map["mapId"]

item_data = requests.get(items_url).json()["data"]
for item_id in item_data.keys():
    if "into" not in item_data[item_id].keys() and item_data[item_id]["maps"][str(map_id)] and item_data[item_id]["gold"]["purchasable"] and item_data[item_id]["gold"]["total"] > 1000:
        items[item_id] = item_data[item_id]["name"]