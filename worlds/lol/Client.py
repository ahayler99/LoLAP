from __future__ import annotations
import os
import sys
import asyncio
import shutil
import requests
import json

import ModuleUpdate
ModuleUpdate.update()

import Utils

check_num = 0

###Set up game communication path###
if "localappdata" in os.environ:
    game_communication_path = os.path.expandvars(r"%localappdata%/LOLAP")
else:
    game_communication_path = os.path.expandvars(r"$HOME/LOLAP")
if not os.path.exists(game_communication_path):
    os.makedirs(game_communication_path)


###API FUNCTIONS###
def get_header(api_key):
    return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": api_key
        }

def get_puuid_by_summoner_name(summoner_name, api_key, region_short):
    url = "https://" + region_short + ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" + str(summoner_name)
    response = requests.get(url, headers=get_header(api_key))
    return json.loads(response.text)["puuid"]

def get_last_match_id_by_puuid(puuid, api_key, region_long):
    url = "https://" + region_long + ".api.riotgames.com/lol/match/v5/matches/by-puuid/" + str(puuid) + "/ids?start=0&count=1"
    response = requests.get(url, headers=get_header(api_key))
    return json.loads(response.text)[0]

def get_match_info_by_match_id(match_id, api_key, region_long):
    url = "https://" + region_long + ".api.riotgames.com/lol/match/v5/matches/" + str(match_id)
    response = requests.get(url, headers=get_header(api_key))
    return json.loads(response.text)

def get_item_ids_purchased(puuid, match_info):
    item_ids = []
    item_slots = ["item0", "item1", "item2", "item3", "item4", "item5", "item6"]
    for participant in match_info["info"]["participants"]:
        if participant["puuid"] == puuid:
            for item_slot in item_slots:
                if item_slot in participant.keys():
                    item_ids.append(participant[item_slot])
    return item_ids

def won_match(puuid, match_info):
    for participant in match_info["info"]["participants"]:
        if participant["puuid"] == puuid:
            return participant["win"]
    return False

def get_collected_item_ids():
    item_ids = []
    for root, dirs, files in os.walk(game_communication_path):
        for file in files:
            if str(file).startswith("AP"):
                with open(os.path.join(game_communication_path, file), 'r') as f:
                    item_id = int(f.readline())
                    item_ids.append(item_id)
                    f.close()
    return item_ids

def send_check(item_id):
    with open(os.path.join(game_communication_path, "send" + str(566000000 + int(item_id))), 'w') as f:
        f.close()
        
def send_victory():
    with open(os.path.join(game_communication_path, "victory"), 'w') as f:
        f.close()

###Client###
if __name__ == "__main__":
    Utils.init_logging("LOLClient", exception_logger="Client")

from NetUtils import NetworkItem, ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    CommonContext, server_loop


def check_stdin() -> None:
    if Utils.is_windows and sys.stdin:
        print("WARNING: Console input is not routed reliably on Windows, use the GUI instead.")

class LOLClientCommandProcessor(ClientCommandProcessor):
    api_key = ""
    player_puuid = ""
    region_short = "na1"
    region_long = "americas"
    
    region_short_options = ["br1"     , "la1"     , "la2"     , "na1"     , "jp1" , "kr"  , "tw2" , "eun1"  , "euw1"  , "ru"    , "tr1"   , "oc1", "ph2", "sg" , "th2", "vn2"]
    region_long_options =  ["americas", "americas", "americas", "americas", "asia", "asia", "asia", "europe", "europe", "europe", "europe", "sea", "sea", "sea", "sea", "sea"]
    
    def _cmd_set_api_key(self, api_key):
        """Set the API Key for RIOT API"""
        self.api_key = api_key
        self.output(f"API Key Set")
    
    def _cmd_set_summoner_name(self, summoner_name):
        """Set the PUUID from Riot API using the passed Summoner Name"""
        if self.api_key != "":
            self.player_puuid = get_puuid_by_summoner_name(summoner_name, self.api_key, self.region_short)
            self.output(f"PUUID Set")
        else:
            self.output(f"Please set your API Key")
    
    def _cmd_set_region(self, region_number):
        """Sets the region number.  Default is NA"""
        if region_number.isnumeric():
            region_number = int(region_number)
            if region_number >= 0 and region_number < len(self.region_short_options):
                self.region_short = self.region_short_options[region_number]
                self.region_long = self.region_long_options[region_number]
                self.output(f"Region set: " + self.region_short + " - " + self.region_long)
            else:
                self.output(f"Invalid int.  Please choose a valid option.  View options by running /print_region_options")
        else:
            self.output(f"Invalid integer passed.  Please pass a valid option.  View options by running /print_region_options")
    
    def _cmd_check_last_match(self):
        """Checks the last match for victory with unlocked items"""
        new_locations = []
        if self.api_key != "" and self.player_puuid != "":
            unlocked_item_ids = get_collected_item_ids()
            if len(unlocked_item_ids) > 0:
                last_match_id = get_last_match_id_by_puuid(self.player_puuid, self.api_key, self.region_long)
                last_match_info = get_match_info_by_match_id(last_match_id, self.api_key, self.region_long)
                if won_match(self.player_puuid, last_match_info):
                    item_ids_purchased = get_item_ids_purchased(self.player_puuid, last_match_info)
                    for item_id in item_ids_purchased:
                        if int(item_id) + 565000000 in unlocked_item_ids:
                            new_locations.append(int(item_id))
                else:
                    self.output(f"Last Match Resulted in a Loss...")
            else:
                self.output(f"You have no items!")
        else:
            self.output(f"Please set your API Key and Summoner Name")
        if len(new_locations) > 0:
            for location in new_locations:
                send_check(location)
        else:
            self.output(f"No new valid items")
    
    def _cmd_receive_starting_items(self):
        """When you're ready to start your run, this receives your starting items"""
        starting_location_ids = [566_000001, 566_000002, 566_000003, 566_000004, 566_000005, 566_000006]
        for location_id in starting_location_ids:
            with open(os.path.join(game_communication_path, "send" + str(location_id)), 'w') as f:
                f.close()
        self.output("Items Received")
    
    def _cmd_check_for_victory(self):
        victory_item_ids = [565000001, 565000002, 565000003, 565000004, 565000005, 565000006]
        victory_items_collected = 0
        item_ids = get_collected_item_ids()
        for item_id in item_ids:
            if int(item_id) in victory_item_ids:
                victory_items_collected = victory_items_collected + 1
        if victory_items_collected >= len(victory_item_ids):
            send_victory()
        else:
            self.output("You have " + str(victory_items_collected) + " out of " + str(len(victory_item_ids)) + " victory items collected.")
    
    def _cmd_print_item_ids(self):
        """Prints currently collected item ids"""
        item_ids = get_collected_item_ids()
        for item_id in item_ids:
            self.output(item_id)
    
    def _cmd_print_puuid(self):
        """Prints the defined PUUID"""
        self.output(self.player_puuid)
    
    def _cmd_print_api_key(self):
        """Prints the defined API Key"""
        self.output(self.api_key)
    
    def _cmd_print_region(self):
        """Prints currently selected region."""
        self.output(f"Region: " + self.region_short + " - " + self.region_long)
    
    def _cmd_print_region_options(self):
        """Prints all region options"""
        i = 0
        while i < len(self.region_short_options):
            self.output(f"Region " + str(i) + ": " + self.region_short_options[i] + " - " + self.region_long_options[i])
            i = i + 1

class LOLContext(CommonContext):
    command_processor: int = LOLClientCommandProcessor
    game = "League of Legends"
    items_handling = 0b111  # full remote

    def __init__(self, server_address, password):
        super(LOLContext, self).__init__(server_address, password)
        self.send_index: int = 0
        self.syncing = False
        self.awaiting_bridge = False
        # self.game_communication_path: files go in this path to pass data between us and the actual game
        if "localappdata" in os.environ:
            self.game_communication_path = os.path.expandvars(r"%localappdata%/LOLAP")
        else:
            self.game_communication_path = os.path.expandvars(r"$HOME/LOLAP")
        if not os.path.exists(self.game_communication_path):
            os.makedirs(self.game_communication_path)
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                if file.find("obtain") <= -1:
                    os.remove(root+"/"+file)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(LOLContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        await super(LOLContext, self).connection_closed()
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                if file.find("obtain") <= -1:
                    os.remove(root + "/" + file)

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        await super(LOLContext, self).shutdown()
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                if file.find("obtain") <= -1:
                    os.remove(root+"/"+file)

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            if not os.path.exists(self.game_communication_path):
                os.makedirs(self.game_communication_path)
            for ss in self.checked_locations:
                filename = f"send{ss}"
                with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                    f.close()
        if cmd in {"ReceivedItems"}:
            start_index = args["index"]
            if start_index != len(self.items_received):
                for item in args['items']:
                    check_num = 0
                    for filename in os.listdir(self.game_communication_path):
                        if filename.startswith("AP"):
                            if int(filename.split("_")[-1].split(".")[0]) > check_num:
                                check_num = int(filename.split("_")[-1].split(".")[0])
                    item_id = ""
                    location_id = ""
                    player = ""
                    found = False
                    for filename in os.listdir(self.game_communication_path):
                        if filename.startswith(f"AP"):
                            with open(os.path.join(self.game_communication_path, filename), 'r') as f:
                                item_id = str(f.readline()).replace("\n", "")
                                location_id = str(f.readline()).replace("\n", "")
                                player = str(f.readline()).replace("\n", "")
                                if str(item_id) == str(NetworkItem(*item).item) and str(location_id) == str(NetworkItem(*item).location) and str(player) == str(NetworkItem(*item).player):
                                    found = True
                    if not found:
                        filename = f"AP_{str(check_num+1)}.item"
                        with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                            f.write(str(NetworkItem(*item).item) + "\n" + str(NetworkItem(*item).location) + "\n" + str(NetworkItem(*item).player))
                            f.close()

        if cmd in {"RoomUpdate"}:
            if "checked_locations" in args:
                for ss in self.checked_locations:
                    filename = f"send{ss}"
                    with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                        f.close()

    def run_gui(self):
        """Import kivy UI system and start running it as self.ui_task."""
        from kvui import GameManager

        class LOLManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago LOL Client"

        self.ui = LOLManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


async def game_watcher(ctx: LOLContext):
    from worlds.lol.Locations import lookup_id_to_name
    while not ctx.exit_event.is_set():
        if ctx.syncing == True:
            sync_msg = [{'cmd': 'Sync'}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
            ctx.syncing = False
        sending = []
        victory = False
        for root, dirs, files in os.walk(ctx.game_communication_path):
            for file in files:
                if file.find("send") > -1:
                    st = file.split("send", -1)[1]
                    if st != "nil":
                        sending = sending+[(int(st))]
                if file.find("victory") > -1:
                    victory = True
        ctx.locations_checked = sending
        message = [{"cmd": 'LocationChecks', "locations": sending}]
        await ctx.send_msgs(message)
        if not ctx.finished_game and victory:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
        await asyncio.sleep(0.1)


def launch():
    async def main(args):
        ctx = LOLContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        progression_watcher = asyncio.create_task(
            game_watcher(ctx), name="LOLProgressionWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await progression_watcher

        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="LOL Client, for text interfacing.")

    args, rest = parser.parse_known_args()
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()
