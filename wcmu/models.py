from flask import current_app
import requests

config = current_app.config

matchDataUrl = 'https://api.football-data.org/v4/matches'
standingsDataUrl = 'https://api.football-data.org/v4/competitions/WC/standings'
header = { 'X-Auth-Token': config["API_KEY"] }

# required data
# # Matches
# # # Match Date and Match Day
# # # Status
# # # Playing Teams (Home and Away)
# # # # if stage = group_stage: Group else: round
# # # # Team crest
# # # # Short name
# # # # Score
# # # # Goal Scorer
# # # Current Half
# # # Referee

class Match:    
    def __init__(self, match_dict):
        self.status = match_dict["status"]
        if match_dict['stage'] == 'GROUP_STAGE':
            self.group = match_dict['group']
        self.home = match_dict['homeTeam']
        self.away = match_dict['awayTeam']
        self.startTime = match_dict['utcDate']
        if match_dict['score']['fullTime']['home'] != None:
            self.ft_score = match_dict['score']['fullTime']
        else:
            self.ft_score = {"home":"-","away":"-"}

class TeamRow:
    def __init__(self, tD):
        self.position = tD["position"]
        self.name = tD["team"]["name"]
        self.tla = tD["team"]["tla"]
        self.crest = tD["team"]["crest"]
        
        self.mp = tD["playedGames"]
        self.w = tD["won"]
        self.d = tD["draw"]
        self.l = tD["lost"]
        self.pts = tD["points"]
        self.scored = tD["goalsFor"]
        self.conceded = tD["goalsAgainst"]
        self.gd = tD["goalDifference"]

class GroupStandings:
    def __init__(self, sd):
        self.groupname = str(sd["group"])[-1]
        self.table = [TeamRow(row) for row in sd["table"]]

def loadMatchData():
    response = requests.get(matchDataUrl, headers=header)
    matchData = response.json()['matches']
    print("match:", response)
    return [Match(match) for match in matchData]

def loadStandingsData():
    response = requests.get(standingsDataUrl, headers=header)
    standingsData = response.json()['standings']
    print("standings:", response)
    return [GroupStandings(group) for group in standingsData]
    