import requests
import json

url = "https://127.0.0.1:2999/liveclientdata/allgamedata"

def took_tower(game_data, player_name):
    for event in game_data["events"]["Events"]:
        if event["EventName"] == "TurretKilled" and event["KillerName"] == player_name:
            return True
    return False

def assisted_tower(game_data, player_name):
    for event in game_data["events"]["Events"]:
        if event["EventName"] == "TurretKilled" and (event["KillerName"] == player_name or player_name in event["Assisters"]):
            return True
    return False

def took_epic_monster(game_data, player_name, monster_name):
    for event in game_data["events"]["Events"]:
        if event["EventName"] == monster_name + "Kill" and event["KillerName"] == player_name:
            return True
    return False

def assisted_epic_monster(game_data, player_name, monster_name):
    for event in game_data["events"]["Events"]:
        if event["EventName"] == monster_name + "Kill" and (event["KillerName"] == player_name or player_name in event["Assisters"]):
            return True
    return False

def stole_epic_monster(game_data, player_name, monster_name):
    for event in game_data["events"]["Events"]:
        if event["EventName"] == monster_name + "Kill" and (event["KillerName"] == player_name or player_name in event["Assisters"]) and str(event["Stolen"]) == "True":
            return True
    return False

def assisted_kill(game_data, player_name):
    for event in game_data["events"]["Events"]:
        if event["EventName"] == "ChampionKill" and (event["KillerName"] == player_name or player_name in event["Assisters"]):
            return True
    return False

def player_vision_score(game_data, player_name):
    for player in game_data["allPlayers"]:
        if player["summonerName"] == player_name:
            return player["wardScore"]
    return 0

def player_creep_score(game_data, player_name):
    for player in game_data["allPlayers"]:
        if player["summonerName"] == player_name:
            return player["creepScore"]
    return 0

def vision_score_above(game_data, player_name, score_target):
    return player_vision_score(game_data, player_name) >= score_target

def creep_score_above(game_data, player_name, score_target):
    return player_creep_score(game_data, player_name) >= score_target





try:
    x = requests.get(url, verify=False).json()
    print(json.dumps(x, indent=2))
except:
    print("No connection to game")