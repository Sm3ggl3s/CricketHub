# from bs4 import BeautifulSoup
# import requests
# import time

# class Livescore:

#     html_text = requests.get('https://www.cricbuzz.com/cricket-match/live-scores').text

#     soup = BeautifulSoup(html_text, 'lxml')

#     matches = soup.find_all('div', class_='cb-mtch-lst cb-col cb-col-100 cb-tms-itm')

#     results_of_matches = {}

#     count = 0

#     for match in matches:
        
#         header = match.find('a', class_='text-hvr-underline text-bold').text.replace(',', '')
#         match_type = match.find('span', class_='text-gray').text

#         bol_team_name = match.find('div', class_='cb-hmscg-bwl-txt').find('div', class_='cb-ovr-flo cb-hmscg-tm-nm').text.replace('..', '')
#         bol_team_score = match.find('div', class_='cb-hmscg-bwl-txt').find('div', style='display:inline-block; width:140px').text
#         bat_team_name = match.find('div', class_='cb-hmscg-bat-txt').find('div', class_='cb-ovr-flo cb-hmscg-tm-nm').text.replace('..', '')
#         bat_team_score = match.find('div', class_='cb-hmscg-bat-txt').find('div', style='display:inline-block; width:140px').text
#         live_comment = match.find('div', class_='cb-text-live').text

#         match_details = {
#             "header": header,
#             "match_type": match_type,
#             "bol_team_name": bol_team_name,
#             "bol_team_score": bol_team_score,
#             "bat_team_name": bat_team_name,
#             "bat_team_score": bat_team_score,
#             "live_comment": live_comment,
#         }

#         results_of_matches[count] = match_details
        
#         count += 1


#     print(results_of_matches)
