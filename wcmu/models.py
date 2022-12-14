from flask import current_app
from datetime import datetime, timezone
from random import randint
from rich import print
import requests
from requests import ConnectTimeout, Timeout, ConnectionError

config = current_app.config

standingsDataUrl = 'https://api.football-data.org/v4/competitions/WC/standings'
fixturesUrl = "https://api.football-data.org/v4/competitions/WC/matches?season=2022"
header = { 'X-Auth-Token': config["API_KEY"] }

flag_dict = requests.get("https://flagcdn.com/en/codes.json").json()
swapped_flag_dict = {v: k for k, v in flag_dict.items()}

def getFlagUrl(country):
    if country != None:
        return f"https://flagcdn.com/{swapped_flag_dict[country]}.svg"

matchStatus = {"FINISHED":'FULL TIME', "PAUSED":'HALF TIME', "IN_PLAY":'LIVE', "TIMED":'SCHEDULED'}

class Match:    
    def __init__(self, match_dict):
        self.id = match_dict['id']
        self.status = matchStatus[match_dict["status"]]
        if match_dict["stage"] == "GROUP_STAGE":
            self.stage = match_dict["group"].replace("_"," ")
        else:
            self.stage = match_dict["stage"].replace("_"," ")
        self.home = match_dict['homeTeam']
        self.away = match_dict['awayTeam']
        #print(self.home, self.away)
        self.home_crest = getFlagUrl(self.home['name'])
        self.away_crest = getFlagUrl(self.away['name'])
        self.date = datetime.strptime(match_dict['utcDate'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        self.dateStr = self.date.strftime("%B %d, %Y")
        if match_dict['score']['fullTime']['home'] != None:
            self.ft_score = match_dict['score']['fullTime']
            #self.ft_score = {"home":randint(0,9),"away":randint(0,9)}
        else:
            self.ft_score = {"home":"-","away":"-"}
            

class TeamRow:
    def __init__(self, team_dict):
        self.position = team_dict["position"]
        self.name = team_dict["team"]["name"]
        self.tla = team_dict["team"]["tla"]
        self.crest = getFlagUrl(self.name) #team_dict["team"]["crest"]
        
        self.mp = team_dict["playedGames"]
        self.w = team_dict["won"]
        self.d = team_dict["draw"]
        self.l = team_dict["lost"]
        self.pts = team_dict["points"]
        self.scored = team_dict["goalsFor"]
        self.conceded = team_dict["goalsAgainst"]
        self.gd = team_dict["goalDifference"]

class GroupStandings:
    def __init__(self, standings_dict):
        self.name = str(standings_dict["group"])[-1]
        self.table = [TeamRow(row) for row in standings_dict["table"]]

def loadToday():
    today = datetime.utcnow().replace(tzinfo=timezone.utc)
    print(today.strftime("%B %d, %Y"))
    try:
        response = requests.get(fixturesUrl, headers=header)
        try:
            allMatches = [Match(match) for match in response.json()['matches']]
            print("match:", response)

            return [
                match
                for match in allMatches
                if today.strftime("%B %d, %Y") == match.dateStr
            ]

        except KeyError:
            print("\nerror retrieving match data, trying again\n")
    except (ConnectTimeout, Timeout, ConnectionError) as e:
        print("something went wrong")
        print(f"[[{e}]]")

def loadStandings():
    try:
        response = requests.get(standingsDataUrl, headers=header)
        try:
            standingsData = response.json()['standings']
            print("standings:", response)
            return [GroupStandings(group) for group in standingsData]
        except KeyError:
            print("\nerror retrieving standings data, trying again\n")
    except (ConnectTimeout, Timeout, ConnectionError) as e:
        print("something went wrong")
        print(f"[[{e}]]")

def loadFixtures():
    try:
        response = requests.get(fixturesUrl, headers=header)
        try:
            fixturesData = response.json()['matches']
            print("fixtures:", response)
            return {
                "allMatches": [Match(match) for match in fixturesData],
                "dates": list(
                    dict.fromkeys(
                        [
                            Match(match).date.strftime("%B %d, %Y")
                            for match in fixturesData
                        ]
                    )
                ),
                "stages": list(
                    dict.fromkeys([Match(m).stage for m in fixturesData])
                ),
            }

        except KeyError:
            print("\nerror retrieving fixtures data, trying again\n")
    except (ConnectTimeout, Timeout, ConnectionError) as e:
        print("something went wrong")
        print(f"[[{e}]]")
        