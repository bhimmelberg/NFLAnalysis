import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import NFL stats database
df = pd.read_excel("C:/Users/bhimm/PycharmProjects/2410Assignments/useful_data.xlsx")
teams = pd.read_csv("C:/Users/bhimm/PycharmProjects/2410Assignments/nfl_teams.csv")

# Keep wanted columns of data
df = df[['schedule_date', 'schedule_season', 'schedule_week', 'schedule_playoff', 'team_home',
         'score_home', 'score_away', 'team_away', 'team_favorite_id', 'spread_favorite',
         'over_under_line', 'stadium', 'weather_temperature',
         'weather_wind_mph', 'weather_detail', 'stadium_neutral']]

# Make over/under column a float value
df['over_under_line'] = df.over_under_line.astype(float)

# Make stadium_neutral and schedule_playoff a series of 0s and 1s rather than true/false values
df['stadium_neutral'] = df.stadium_neutral.astype(int)
df['schedule_playoff'] = df.schedule_playoff.astype(int)

# mapping team_id to teams and Abbreviation
df['team_home'] = df.team_home.map(teams.set_index('Name')['ID'].to_dict())
df['team_away'] = df.team_away.map(teams.set_index('Name')['ID'].to_dict())
df['team_favorite_id'] = df.team_favorite_id.map(teams.set_index('Abbreviation')['ID'].to_dict())

# Enter -1 into cells where the team_favorite_id was PICK
df['team_favorite_id'] = df['team_favorite_id'].fillna(-1)

df.loc[df.team_favorite_id == df.team_home, 'home_favorite'] = 1
df.loc[df.team_favorite_id == df.team_away, 'away_favorite'] = 1
df['home_favorite'] = df['home_favorite'].fillna(0)
df['away_favorite'] = df['away_favorite'].fillna(0)

# Create a new column over_success to show if the game hit the over or under. Value = 1 if the over hit
df.loc[((df.score_home + df.score_away) > df.over_under_line), 'over_success'] = 1
# Value is 0 for a push
df.loc[((df.score_home + df.score_away) == df.over_under_line), 'over_success'] = 0
# Value is -1 for the under
df.over_success.fillna(-1, inplace=True)

# Make schedule_week column all ints instead of strings
df.loc[(df.schedule_week == 'Wildcard') | (df.schedule_week == 'WildCard'), 'schedule_week'] = '18'
df.loc[(df.schedule_week == 'Division'), 'schedule_week'] = '19'
df.loc[(df.schedule_week == 'Conference'), 'schedule_week'] = '20'
df.loc[(df.schedule_week == 'Superbowl') | (df.schedule_week == 'SuperBowl'), 'schedule_week'] = '21'
df['schedule_week'] = df.schedule_week.astype(int)

# Column to show if the home or away team won
df['result'] = (df.score_home < df.score_away).astype(int)

# Create dataframe for data since 2015
df2015 = pd.DataFrame()
df2015 = df[df['schedule_season'] > 2014]

# Create new excel file
writer = pd.ExcelWriter('kjh.xlsx')
df.to_excel(writer, sheet_name='Sheet1')
writer.close()

# Basic betting percentages since 2000
def data2000():
    neutralGames = sum(df.stadium_neutral == 1)
    neutralGames = neutralGames - 1
    homeWinPct = sum(((df.score_home > df.score_away) & (df.stadium_neutral == 0)) / len(df)) * 100
    homeWinPctStr = str(homeWinPct)
    awayWinPct = sum(((df.score_home < df.score_away) & (df.stadium_neutral == 0)) / len(df)) * 100
    awayWinPctStr = str(awayWinPct)
    underHit = sum(((df.score_home + df.score_away) < df.over_under_line) / len(df)) * 100
    underHitStr = str(underHit)
    overHit = sum(((df.score_home + df.score_away) > df.over_under_line) / len(df)) * 100
    overHitStr = str(overHit)
    pushHit = sum(((df.score_home + df.score_away) == df.over_under_line) / len(df)) * 100
    pushHitStr = str(pushHit)
    tiePct = sum((df.score_home == df.score_away) / len(df)) * 100
    tiePctStr = str(tiePct)
    stadiumNeutralPct = ((neutralGames / len(df)) * 100)
    stadiumNeutralPctStr = str(stadiumNeutralPct)

    # Ensure data is analyzed correctly
    overAddsUp = underHit + overHit + pushHit
    overAddsUpStr = str(overAddsUp)
    gamesAddsUp = homeWinPct + awayWinPct + tiePct + stadiumNeutralPct
    gamesAddsUpStr = str(gamesAddsUp)

    # Advanced Stats Since 2000
    favored = sum(
        (((df.home_favorite == 1) & (df.result == 0)) | ((df.away_favorite == 1) & (df.result == 1))) / len(df)) * 100
    favored = str(favored)
    favoredCover = sum((((df.home_favorite == 1) & ((df.score_away - df.score_home) < df.spread_favorite)) |
                        ((df.away_favorite == 1) & ((df.score_home - df.score_away) < df.spread_favorite)))
                       / len(df)) * 100
    favoredCover = str(favoredCover)
    dogCover = sum((((df.home_favorite == 1) & ((df.score_away - df.score_home) > df.spread_favorite)) |
                    ((df.away_favorite == 1) & ((df.score_home - df.score_away) > df.spread_favorite)))
                   / len(df)) * 100
    dogCover = str(dogCover)

    # print all percentages
    print("Number of Games Since 2000: " + str(len(df)))
    print("Home Team Straight Up Win Percentage Since 2000: " + homeWinPctStr + "%")
    print("Away Team Straight Up Win Percentage Since 2000: " + awayWinPctStr + "%")
    print("Under Hit Percentage Since 2000: " + underHitStr + "%")
    print("Over Hit Percentage Since 2000: " + overHitStr + "%")
    print("Push Percentage Since 2000: " + pushHitStr + "%")
    print("Over/Under data added = " + overAddsUpStr + "%")
    print("Games data added = " + gamesAddsUpStr + "%")
    print("Favored Win Percentage Since 2000: " + favored + "%")
    print("Favorite Covers The Spread Percentage Since 2000: " + favoredCover + "%")
    print("Underdog Covers The Spread Percentage Since 2000: " + dogCover + "%")

# Basic betting percentages since 2015
def data2015():
    neutralGames2015 = sum(df2015.stadium_neutral == 1)
    neutralGames2015 = neutralGames2015 - 1
    homeWinPct2015 = sum(((df2015.score_home > df2015.score_away) & (df2015.stadium_neutral == 0)) / len(df2015)) * 100
    homeWinPctStr2015 = str(homeWinPct2015)
    awayWinPct2015 = sum(((df2015.score_home < df2015.score_away) & (df2015.stadium_neutral == 0)) / len(df2015)) * 100
    awayWinPctStr2015 = str(awayWinPct2015)
    underHit2015 = sum(((df2015.score_home + df2015.score_away) < df2015.over_under_line) / len(df2015)) * 100
    underHitStr2015 = str(underHit2015)
    overHit2015 = sum(((df2015.score_home + df2015.score_away) > df2015.over_under_line) / len(df2015)) * 100
    overHitStr2015 = str(overHit2015)
    pushHit2015 = sum(((df2015.score_home + df2015.score_away) == df2015.over_under_line) / len(df2015)) * 100
    pushHitStr2015 = str(pushHit2015)
    tiePct2015 = sum((df2015.score_home == df2015.score_away) / len(df2015)) * 100
    tiePctStr2015 = str(tiePct2015)
    stadiumNeutralPct2015 = ((neutralGames2015 / len(df2015)) * 100)
    stadiumNeutralPctStr2015 = str(stadiumNeutralPct2015)

    # Ensure 2015 data is analyzed correctly
    overAddsUp2015 = underHit2015 + overHit2015 + pushHit2015
    overAddsUpStr2015 = str(overAddsUp2015)
    gamesAddsUp2015 = homeWinPct2015 + awayWinPct2015 + tiePct2015 + stadiumNeutralPct2015
    gamesAddsUpStr2015 = str(gamesAddsUp2015)

    # Advanced Stats Since 2015
    favored2015 = sum(
        (((df2015.home_favorite == 1) & (df2015.result == 0)) | ((df2015.away_favorite == 1) & (df2015.result == 1))) / len(
            df2015)) * 100
    favored2015 = str(favored2015)
    favoredCover2015 = sum(
        (((df2015.home_favorite == 1) & ((df2015.score_away - df2015.score_home) < df2015.spread_favorite)) |
         ((df2015.away_favorite == 1) & ((df2015.score_home - df2015.score_away) < df2015.spread_favorite)))
        / len(df2015)) * 100
    favoredCover2015 = str(favoredCover2015)
    dogCover2015 = sum((((df2015.home_favorite == 1) & ((df2015.score_away - df2015.score_home) > df2015.spread_favorite)) |
                        ((df2015.away_favorite == 1) & ((df2015.score_home - df2015.score_away) > df2015.spread_favorite)))
                       / len(df2015)) * 100
    dogCover2015 = str(dogCover2015)

    # Print all 2015 percentages
    print("\nNumber of Games Since 2015: " + str(len(df2015)))
    print("Home Team Straight Up Win Percentage Since 2015: " + homeWinPctStr2015 + "%")
    print("Away Team Straight Up Win Percentage Since 2015: " + awayWinPctStr2015 + "%")
    print("Under Hit Percentage Since 2015: " + underHitStr2015 + "%")
    print("Over Hit Percentage Since 2015: " + overHitStr2015 + "%")
    print("Push Percentage Since 2015: " + pushHitStr2015 + "%")
    print("Over/Under data added for 2015 = " + overAddsUpStr2015 + "%")
    print("Games data added for 2015 = " + gamesAddsUpStr2015 + "%")
    print("Favored Win Percentage Since 2015: " + favored2015 + "%")
    print("Favorite Covers The Spread Percentage Since 2015: " + favoredCover2015 + "%")
    print("Underdog Covers The Spread Percentage Since 2015: " + dogCover2015 + "%")

# Print basic data
data2000()
data2015()
