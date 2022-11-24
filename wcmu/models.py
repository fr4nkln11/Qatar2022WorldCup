import requests

api1 = 'https://api.football-data.org/v4/matches'
header_1 = { 'X-Auth-Token': 'b3211cb5487941569bfb0401c4b15725' }

user = {
"email": "ikehfranklind3c0d3r@gmail.com",
"password": "wc4p1project2022",
}

#login_response = requests.post("http://api.cup2022.ir/api/v1/user/login", json=user)
#print(login_response.text)
#token = login_response.json()["data"]["token"]

#header_2= {'Accept': 'application/json', 'Authorization': f'Bearer {token}'}
#api2 = 'http://api.cup2022.ir/api/v1/bydate'
#date = {"date":"11/22/2022"}

response = requests.get(api1, headers=header_1)
#response2 = requests.post(api2, json=date, headers=header_2)

print(response)

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
    