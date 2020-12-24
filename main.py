from bs4 import BeautifulSoup
import requests
import json
import csv

oddshark_odds = requests.get("https://www.oddsshark.com/ncaab/odds")
kenpom_rankings = requests.get("https://kenpom.com/")
kenpom_height_exp = requests.get("https://kenpom.com/height.php")

if oddshark.status_code == 200 & kenpom.status_code == 200:
  oddshark_soup = BeautifulSoup(oddshark.content, 'html.parser')
  kenpom_soup = BeautifulSoup(kenpom.content, 'html.parser')

matchups = oddshark_soup.find_all(class_="op-matchup-team-wrapper")
lines = oddshark_soup.find_all(class_="op-item-row-wrapper not-futures")
rankings = kenpom_soup.find_all("tbody")

kenpom_data = {}

for x in range(len(rankings)):
  temp = rankings[x].select("tr")
  for y in range(len(temp)):
    if len(temp[y].select("th")) == 0:
      key = temp[y].select("td")[1].select("a")[0].text
      kenpom_data[key] = {}
      kenpom_data[key]["ranking"] = temp[y].select("td")[0].text
      kenpom_data[key]["off_ranking"] = temp[y].select("td")[6].text
      kenpom_data[key]["def_ranking"] = temp[y].select("td")[8].text

line_data = []

for x in range(len(matchups)):
  temp = {}
  temp["away_team"] = json.loads(matchups[x].select("div.op-team-top")[0]["data-op-name"])["full_name"].replace("State", "St.").replace(" University", "").replace("St.-", "St. ")
  temp["home_team"] = json.loads(matchups[x].select("div.op-team-bottom")[0]["data-op-name"])["full_name"].replace("State", "St.").replace(" University", "").replace("St.-", "St. ")
  temp["away_spread"] = json.loads(lines[x].select("div.no-vegas > div.op-first-row > div.op-item")[0]['data-op-info'])["fullgame"]
  temp["home_spread"] = json.loads(lines[x].select("div.no-vegas > div.op-second-row > div.op-item")[0]['data-op-info'])["fullgame"]
  temp["away_open_spread"] = json.loads(lines[x].select("div.op-item-wrapper > div.op-first-row > div.op-item")[0]['data-op-info'])["fullgame"]
  temp["home_open_spread"] = json.loads(lines[x].select("div.op-item-wrapper > div.op-second-row > div.op-item")[0]['data-op-info'])["fullgame"]
  line_data.append(temp)

for x in range(len(line_data)):
  team1 = kenpom_data[line_data[x]['away_team']]["ranking"]
  team2 = kenpom_data[line_data[x]['home_team']]["ranking"]
  print(team1, line_data[x]['away_team'], "@" , team2, line_data[x]['home_team'])
  print("Opening Line:", line_data[x]['away_team'], line_data[x]['away_open_spread'])
  print("Current Line:", line_data[x]['away_team'], line_data[x]['away_spread'])
  print()
