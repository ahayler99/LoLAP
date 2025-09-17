from msilib.schema import CheckBox
import FreeSimpleGUI as sg
import json
import requests
import os

###GET CHAMPION DATA###
versions_url = "https://ddragon.leagueoflegends.com/api/versions.json"
most_recent_version = requests.get(versions_url).json()[0]
champions_url = "https://ddragon.leagueoflegends.com/cdn/" + str(most_recent_version) + "/data/en_US/champion.json"
champions = {}
playrate_url = "http://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/championrates.json"
champion_data = requests.get(champions_url).json()["data"]
playrate_data = requests.get(playrate_url).json()["data"]
eventflag = False
row = 0

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

###SET GLOBAL VARIABLES###
url = "https://127.0.0.1:2999/liveclientdata/allgamedata"
unlocked_champion_ids = []
total_lp_gained = 0
in_match = False
game_values = {
    "required_assists": 0,
    "required_cs"     : 0,
    "required_kills"  : 0,
    "required_lp"     : 0,
    "required_vs"     : 0,
    "current_lp"      : 0
}

###SET UP GAME COMMUNICATION PATH###
if "localappdata" in os.environ:
    game_communication_path = os.path.expandvars(r"%localappdata%/LOLAP")
else:
    game_communication_path = os.path.expandvars(r"$HOME/LOLAP")
if not os.path.exists(game_communication_path):
    os.makedirs(game_communication_path)


###DEFINE FUNCTIONS###
def get_game_data():
    try:
        return requests.get(url, verify=False).json()
    except:
        return None

def get_items(game_values):
    game_values["current_lp"] = 0
    unlocked_champion_ids.clear()
    for root, dirs, files in os.walk(game_communication_path):
        for file in files:
            if file.startswith("AP"):
                with open(os.path.join(game_communication_path, file), 'r') as f:
                    item_id = int(f.readline())
                    if item_id % 565000000 == 0:
                        game_values["current_lp"] = game_values["current_lp"] + 1
                    else:
                        unlocked_champion_ids.append(item_id % 565000000)
                    f.close()

def check_sent(champid):
    completed_checks = []
    for root, dirs, files in os.walk(game_communication_path):
        for file in files:
            if file.startswith('send'):
                foo, prev_sent = file.split("send566")
                if str(champid) in prev_sent:
                    foo, prev_sent = prev_sent.split(str(champid))
                    completed_checks.append(int(prev_sent))
    return completed_checks

def check_checks(champid):
    no_check = []
    if "UTILITY" not in champions[champid]["tags"]:
        no_check.append(6)
        no_check.append(7)
    if "BOTTOM" or "UTILITY" in champions[champid]["tags"]:
        no_check.append(3)
    if "JUNGLE" in champions[champid]["tags"]:
        no_check.append(4)
        no_check.append(5)
    if "TOP" in champions[champid]["tags"]:
        no_check.append(1)
    return no_check

def read_cfg(game_values):
    for root, dirs, files in os.walk(game_communication_path):
        if "Required_Assists.cfg" in files:
            with open(os.path.join(game_communication_path, "Required_Assists.cfg"), 'r') as f:
                game_values["required_assists"] = int(f.readline())
        else:
            game_values["required_assists"] = 0
        if "Required_CS.cfg" in files:
            with open(os.path.join(game_communication_path, "Required_CS.cfg"), 'r') as f:
                game_values["required_cs"] = int(f.readline())
        else:
            game_values["required_cs"] = 0
        if "Required_Kills.cfg" in files:
            with open(os.path.join(game_communication_path, "Required_Kills.cfg"), 'r') as f:
                game_values["required_kills"] = int(f.readline())
        else:
            game_values["required_kills"] = 0
        if "Required_LP.cfg" in files:
            with open(os.path.join(game_communication_path, "Required_LP.cfg"), 'r') as f:
                game_values["required_lp"] = int(f.readline())
        else:
            game_values["required_lp"] = 0
        if "Required_VS.cfg" in files:
            with open(os.path.join(game_communication_path, "Required_VS.cfg"), 'r') as f:
                game_values["required_vs"] = int(f.readline())
        else:
            game_values["required_vs"] = 0

def display_champion_list(window):
    champion_table_rows = []
    for champion_id in unlocked_champion_ids:
        champion_table_rows.append([champions[champion_id]["name"], champion_id])
    window["Champions Unlocked Table"].update(values=champion_table_rows)
    return champion_table_rows

def display_values(window, game_values):
    value_table_rows = []
    value_table_rows.append(['Dragon Assist'           ])
    value_table_rows.append(['Baron Assist'           ])
    value_table_rows.append(['Herald/Grubs Assist'           ])
    value_table_rows.append(['Tower Assist'          ])
    value_table_rows.append(['Inhibitors Assist'           ])
    value_table_rows.append(['Required Assists:'     , str(game_values["required_assists"])])
    value_table_rows.append(['Required VS:'          , str(game_values["required_vs"])])
    value_table_rows.append(['Required Kills:'       , str(game_values["required_kills"])])
    value_table_rows.append(['Required CS:'          , str(game_values["required_cs"])])

    window["Values Table"].update(values=value_table_rows)

def display_values_colours(window, game_values, completed_checks, no_check):
    window["Values Table"].update(select_rows = None, row_colors = None)
    if completed_checks:
        for i in completed_checks:
            window["Values Table"].update(row_colors=[(i-1, 'green')])
    if no_check:
        for i in no_check:
            window["Values Table"].update(row_colors=[(i-1, 'red')])

def send_starting_champion_check():
    for i in range(6):
        with open(os.path.join(game_communication_path, "send56600000" + str(i)), 'w') as f:
            f.close()

def check_lp_for_victory(game_values):
    if game_values["current_lp"] >= game_values["required_lp"] and game_values["required_lp"] != 0:
        with open(os.path.join(game_communication_path, "victory"), 'w') as f:
            f.close()

def get_player_name(game_data):
    return game_data["activePlayer"]["summonerName"].split("#")[0]

def get_champion_name(game_data, player_name):
    for player in game_data["allPlayers"]:
        if player["summonerName"] == player_name:
            return player["championName"]

def get_champion_id(champion_name):
    for champion_id in champions:
        if champions[champion_id]["name"] == champion_name:
            return champion_id

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

def took_inhibitor(game_data, player_name):
    for event in game_data["events"]["Events"]:
        if event["EventName"] == "InhibKilled" and event["KillerName"] == player_name:
            return True
    return False

def assisted_inhibitor(game_data, player_name):
    for event in game_data["events"]["Events"]:
        if event["EventName"] == "InhibKilled" and (event["KillerName"] == player_name or player_name in event["Assisters"]):
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
            return player["scores"]["wardScore"]
    return 0

def player_creep_score(game_data, player_name):
    for player in game_data["allPlayers"]:
        if player["summonerName"] == player_name:
            return player["scores"]["creepScore"]
    return 0

def player_kills(game_data, player_name):
    for player in game_data["allPlayers"]:
        if player["summonerName"] == player_name:
            return player["scores"]["kills"]
    return 0

def player_assists(game_data, player_name):
    for player in game_data["allPlayers"]:
        if player["summonerName"] == player_name:
            return player["scores"]["assists"]
    return 0

def vision_score_above(game_data, player_name, score_target):
    return player_vision_score(game_data, player_name) >= score_target and score_target > 0

def creep_score_above(game_data, player_name, score_target):
    return player_creep_score(game_data, player_name) >= score_target and score_target > 0

def kills_above(game_data, player_name, score_target):
    return player_kills(game_data, player_name) >= score_target and score_target > 0

def assists_above(game_data, player_name, score_target):
    return player_assists(game_data, player_name) >= score_target and score_target > 0

def get_objectives_complete(game_data, game_values):
    objectives_complete = []
    player_name = get_player_name(game_data)
    champion_name = get_champion_name(game_data, player_name)
    champion_id = get_champion_id(champion_name)
    if champion_id in unlocked_champion_ids:
        if assisted_epic_monster(game_data, player_name, "Dragon"):
            objectives_complete.append(1)
        if assisted_epic_monster(game_data, player_name, "Herald") or assisted_epic_monster(game_data, player_name, "Horde"):
            objectives_complete.append(2)
        if assisted_epic_monster(game_data, player_name, "Baron"):
            objectives_complete.append(3)
        if assisted_tower(game_data, player_name):
            objectives_complete.append(4)
        if assisted_inhibitor(game_data, player_name):
            objectives_complete.append(5)
        if assists_above(game_data, player_name, game_values["required_assists"]):
            objectives_complete.append(6)
        if vision_score_above(game_data, player_name, game_values["required_vs"]):
            objectives_complete.append(7)
        if kills_above(game_data, player_name, game_values["required_kills"]):
            objectives_complete.append(8)
        if creep_score_above(game_data, player_name, game_values["required_cs"]):
            objectives_complete.append(9)
    send_locations(objectives_complete, champion_id)

def send_locations(objectives_complete, champion_id):
    for objective_id in objectives_complete:
        with open(os.path.join(game_communication_path, "send" + str(566000000 + (champion_id * 100) + objective_id)), 'w') as f:
            f.close()

sg.theme('DarkAmber')
layout = [  [
                sg.Text('In Match: No', justification = 'center', key = "In Match Text"),
                sg.Button('Check for Match', key = "Check for Match Button", disabled_button_color = "blue", expand_x = True, expand_y = True),
                sg.Column(
                [   [sg.Text('LP Progress', expand_x = True, expand_y = True, key = "LP_text")],
                    [sg.ProgressBar(game_values["required_lp"], size = (40, 10), expand_x = True, key='LP_progress')]
                ])
            ],
            [   
                sg.Column(
                [   [sg.Text("Champions Unlocked")],
                    [sg.Table(
                        [
                        ], headings = ["Champion Name", "Champion ID"], key = "Champions Unlocked Table", enable_click_events=True, expand_x = True, expand_y = True)],
                ], expand_x = True, expand_y = True),
                sg.Column(
                [
                    [sg.Text("Required Values")],
                    [sg.Table(
                        [
                        ], headings = ["Value Type", "Value Amount"], key = "Values Table", auto_size_columns=True, expand_x = True, expand_y = True)]
               ], expand_x = True, expand_y = True)
            ]
        ]

window = sg.Window('LOL AP', layout, resizable=True)
while True:
    game_data = None
    event, values = window.read(timeout=2000)
    if event == sg.WIN_CLOSED:
        break
    if event == 'Check for Match Button':
        in_match = True
    check_lp_for_victory(game_values)
    get_items(game_values)
    read_cfg(game_values)
    champion_table_rows = display_champion_list(window)
    display_values(window, game_values)
    send_starting_champion_check()
    window['LP_progress'].update(max=game_values["required_lp"], current_count=game_values["current_lp"])
    window['LP_text'].update(value=(f"LP Progress ({game_values["current_lp"]}/{game_values["required_lp"]})"))
    for i in range(0,9):
        window["Values Table"].update(row_colors = [(i,'#2C2825')])
    if in_match:
        game_data = get_game_data()
    if game_data is None:
        window["In Match Text"].update("In Match: No Match Found")
        in_match = False
    else:
        window["In Match Text"].update("In Match: In Match")
        get_objectives_complete(game_data, game_values)
    if event[0] == 'Champions Unlocked Table' or eventflag:
        if event[2][0] == -1:
            eventflag = False
        else:
            if event[0] == 'Champions Unlocked Table' and event[2][0] >= 0:
                row, col = event[2]
            eventflag = True
            selected_row_data = champion_table_rows[row]
            completed_checks = check_sent(selected_row_data[1])
            no_check = check_checks(selected_row_data[1])
            if completed_checks or no_check:
                display_values_colours(window, game_values, completed_checks, no_check)

window.close()