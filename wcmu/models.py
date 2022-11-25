from flask import current_app
import requests

config = current_app.config

api1 = 'https://api.football-data.org/v4/matches'
header_1 = { 'X-Auth-Token': config["API_KEY"] }

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
# # # # Current Half
# # # Referee

class Match_Obj:    
    def __init__(self, match_dict):
        if match_dict["status"] == 'IN_PLAY':
            self.status = 'LIVE'
        else:
            self.status = match_dict["status"]
        
        if match_dict['stage'] == 'GROUP_STAGE':
            self.group = match_dict['group']
        
        self.home = match_dict['homeTeam']
        self.away = match_dict['awayTeam']
        self.ltu = match_dict['lastUpdated']
        if match_dict['score']['fullTime']['home'] != None:
            self.ft_score = match_dict['score']['fullTime']
        else:
            self.ft_score = {'home': '-', 'away':'-'}

def load():
    response = requests.get(api1, headers=header_1)
    match_data = response.json()['matches']
    print(response)
    return [Match_Obj(m) for m in match_data]
    