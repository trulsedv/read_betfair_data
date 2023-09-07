import os
import bz2
import json
import sys


def getMarketDefinitionKeyValue(file_path, key):
    with open(file_path, 'rb') as bz2_file:
        compressed_data = bz2_file.read()
        decompressed_data = bz2.decompress(compressed_data)
        lines = decompressed_data.splitlines()
        for line in reversed(lines):
            try:
                json_data = json.loads(line)
                value = json_data['mc'][0]['marketDefinition'][key]
                return value
            except KeyError:
                continue


def getFixtureOdds(file_path):
    with open(file_path, 'rb') as bz2_file:
        compressed_data = bz2_file.read()
        decompressed_data = bz2.decompress(compressed_data)
        lines = decompressed_data.splitlines()
        for i, line in enumerate(lines):
            json_data = json.loads(line)
            try:
                inPlay = json_data['mc'][0]['marketDefinition']['inPlay']
                if inPlay:
                    runners = json_data['mc'][0]['marketDefinition']['runners']
                    home_odds = -1
                    draw_odds = -1
                    away_odds = -1
                    while home_odds == -1 or draw_odds == -1 or away_odds == -1:
                        json_data = json.loads(lines[i])
                        i -= 1
                        try:
                            rc = json_data['mc'][0]['rc']
                            for change in rc:
                                if change['id'] == runners[0]['id'] and home_odds == -1:
                                    home_odds = change['ltp']
                                if change['id'] == runners[1]['id'] and away_odds == -1:
                                    away_odds = change['ltp']
                                if change['id'] == runners[2]['id'] and draw_odds == -1:
                                    draw_odds = change['ltp']
                        except KeyError:
                            continue
                    fixture_odds = {
                        'home_team': runners[0]['name'],
                        'away_team': runners[1]['name'],
                        'home_odds': home_odds,
                        'draw_odds': draw_odds,
                        'away_odds': away_odds
                    }
                    return fixture_odds
            except KeyError:
                continue


directory = "C:/Users/truls/Downloads/data/BASIC/"

teams = [
    "Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton",
    "Chelsea", "Crystal Palace", "Everton", "Fulham", "Leeds",
    "Leicester", "Liverpool", "Man City", "Man Utd", "Newcastle",
    "Nottm Forest", "Southampton", "Tottenham", "West Ham", "Wolves"
]

fixtures = []
for team1 in teams:
    for team2 in teams:
        if team1 == team2:
            continue
        fixture = f"{team1} v {team2}"
        fixtures.append(fixture)

fixtures_odds = []
years = [item for item in os.listdir(directory) if os.path.isdir(os.path.join(directory, item))]
for year in years:
    dirYear = os.path.join(directory, year)
    months = [item for item in os.listdir(dirYear) if os.path.isdir(os.path.join(dirYear, item))]
    for month in months:
        dirMonth = os.path.join(dirYear, month)
        days = [item for item in os.listdir(dirMonth) if os.path.isdir(os.path.join(dirMonth, item))]
        for day in days:
            dirDay = os.path.join(dirMonth, day)
            events = [item for item in os.listdir(dirDay) if os.path.isdir(os.path.join(dirDay, item))]
            for event in events:
                dirEvent = os.path.join(dirDay, event)
                marketFiles = [item for item in os.listdir(dirEvent) if item.endswith(".bz2") and not item.startswith(event)]
                eventName0 = getMarketDefinitionKeyValue(os.path.join(dirEvent, marketFiles[0]), 'eventName')
                if eventName0 in fixtures:
                    for marketFile in marketFiles:
                        marketType = getMarketDefinitionKeyValue(os.path.join(dirEvent, marketFile), 'marketType')
                        if marketType == 'MATCH_ODDS':
                            fixture_odds = getFixtureOdds(os.path.join(dirEvent, marketFile))
                            if fixture_odds is None:
                                continue
                            print(f"\n{os.path.join(dirEvent, marketFile)}")
                            fixture_odds['date'] = f'{day}.{month}.{year}'
                            if fixture_odds is None:
                                sys.exit()
                            print(f"{fixture_odds}", flush=True)
                            fixtures_odds.append(fixture_odds)

with open("output.txt", "w") as file:
    for item in fixtures_odds:
        file.write(str(item) + "\n")
