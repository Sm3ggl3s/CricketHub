import requests
import json

# url = url 

# headers = {
# 	"X-RapidAPI-Key": X-RapidAPI-Key
# 	"X-RapidAPI-Host": X-RapidAPI-Host
# }

# response = requests.request("GET", url, headers=headers)

# json_data = json.loads(response.text)

with open('src/scorescricbuzztest.json') as f:
    json_data = json.load(f)


match_info = {}
match_data = []
all_matches = {
    'match_data': match_data
}

for match in json_data['typeMatches']:
    type_match = match['matchType']

    for series in match['seriesMatches']:
        if 'seriesAdWrapper'  in series.keys():
            for match_details in series['seriesAdWrapper']['matches']:
                match_status = match_details['matchInfo']['status']
                city = match_details['matchInfo']['venueInfo']['city']
                ground = match_details['matchInfo']['venueInfo']['ground']

                team1_name = match_details['matchInfo']['team1']['teamName']
                team1_abr = match_details['matchInfo']['team1']['teamSName']

                team2_name = match_details['matchInfo']['team2']['teamName']
                team2_abr = match_details['matchInfo']['team2']['teamSName']
                if 'matchScore' in match_details:
                    if 'team1Score' in match_details['matchScore']:
                        team1_runs = match_details['matchScore']['team1Score']['inngs1']['runs']
                        if 'wickets' in match_details['matchScore']['team1Score']['inngs1']:
                            team1_wickets = match_details['matchScore']['team1Score']['inngs1']['wickets']
                        team1_overs = match_details['matchScore']['team1Score']['inngs1']['overs']
                    else: 
                        team1_runs = ""
                        team1_wickets = ""
                        team1_overs = ""
                        print("doesn't exist")

                    if 'team2Score' in match_details['matchScore']:
                        team2_runs = match_details['matchScore']['team2Score']['inngs1']['runs']
                        if 'wickets' in match_details['matchScore']['team2Score']['inngs1']:
                            team2_wickets = match_details['matchScore']['team2Score']['inngs1']['wickets']
                        team2_overs = match_details['matchScore']['team2Score']['inngs1']['overs']
                    else:
                        team2_runs = ""
                        team2_wickets = ""
                        team2_overs = ""

                match_info['status'] = match_status
                match_info['team1_name'] = team1_name
                match_info['team1_abr'] = team1_abr
                match_info['team1_runs'] = team1_runs
                match_info['team1_wickets'] = team1_wickets
                match_info['team1_overs'] = team1_overs
                match_info['team2_name'] =  team2_name
                match_info['team2_abr'] = team2_abr
                match_info['team2_runs'] = team2_runs
                match_info['team2_wickets'] = team2_wickets
                match_info['team2_overs'] = team2_overs

                all_matches['match_data'].append(match_info.copy())


# for match in all_matches['match_data']:
#     print(match)
#     print()


