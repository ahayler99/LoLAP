import requests
import json

versions_url = "https://ddragon.leagueoflegends.com/api/versions.json"
playrate_url = "http://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/championrates.json"
most_recent_version = requests.get(versions_url).json()[0]
champions_url = "https://ddragon.leagueoflegends.com/cdn/" + str(most_recent_version) + "/data/en_US/champion.json"
champions = {}
champion_data = requests.get(champions_url).json()["data"]
playrate_data = requests.get(playrate_url).json()["data"]

tags = set([])
ids = set([])

for champion in list(champion_data.keys()):
    champid = champion_data[champion]["key"]
    champions[int(champid)] = champion_data[champion]
    role_data = playrate_data[champid]
    role1 = "NONE"
    role1num = 0
    role2 = "NONE"
    role2num = 0
    for role in list(role_data.keys()):
        if role_data[role]["playRate"] > role1num:
            role1num = role_data[role]["playRate"]
            role1 = role
    del role_data[role]
    for role in list(role_data.keys()):
        if role_data[role]["playRate"] > role1num:
            role2num = role_data[role]["playRate"]
            role2 = role
    champions[int(champid)]["tags"] = [role1, role2]

