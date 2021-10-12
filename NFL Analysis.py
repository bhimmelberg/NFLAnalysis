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

# Put Clear for games with no weather detail
df.weather_detail.fillna('CLEAR', inplace=True)

# Create dataframe for data since 2010
df2010 = pd.DataFrame()
df2010 = df[df['schedule_season'] > 2009]

# Basic betting percentages since 2000
def basicData(x):
    if x == 2000:
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
        print("Number of Games Since 2000: " + str(len(df) - 1))
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
    elif x == 2010:
        neutralGames2010 = sum(df2010.stadium_neutral == 1)
        neutralGames2010 = neutralGames2010 - 1
        homeWinPct2010 = sum(
            ((df2010.score_home > df2010.score_away) & (df2010.stadium_neutral == 0)) / len(df2010)) * 100
        homeWinPctStr2010 = str(homeWinPct2010)
        awayWinPct2010 = sum(
            ((df2010.score_home < df2010.score_away) & (df2010.stadium_neutral == 0)) / len(df2010)) * 100
        awayWinPctStr2010 = str(awayWinPct2010)
        underHit2010 = sum(((df2010.score_home + df2010.score_away) < df2010.over_under_line) / len(df2010)) * 100
        underHitStr2010 = str(underHit2010)
        overHit2010 = sum(((df2010.score_home + df2010.score_away) > df2010.over_under_line) / len(df2010)) * 100
        overHitStr2010 = str(overHit2010)
        pushHit2010 = sum(((df2010.score_home + df2010.score_away) == df2010.over_under_line) / len(df2010)) * 100
        pushHitStr2010 = str(pushHit2010)
        tiePct2010 = sum((df2010.score_home == df2010.score_away) / len(df2010)) * 100
        tiePctStr2010 = str(tiePct2010)
        stadiumNeutralPct2010 = ((neutralGames2010 / len(df2010)) * 100)
        stadiumNeutralPctStr2010 = str(stadiumNeutralPct2010)

        # Ensure 2010 data is analyzed correctly
        overAddsUp2010 = underHit2010 + overHit2010 + pushHit2010
        overAddsUpStr2010 = str(overAddsUp2010)
        gamesAddsUp2010 = homeWinPct2010 + awayWinPct2010 + tiePct2010 + stadiumNeutralPct2010
        gamesAddsUpStr2010 = str(gamesAddsUp2010)

        # Advanced Stats Since 2010
        favored2010 = sum(
            (((df2010.home_favorite == 1) & (df2010.result == 0)) | (
                        (df2010.away_favorite == 1) & (df2010.result == 1))) / len(
                df2010)) * 100
        favored2010 = str(favored2010)
        favoredCover2010 = sum(
            (((df2010.home_favorite == 1) & ((df2010.score_away - df2010.score_home) < df2010.spread_favorite)) |
             ((df2010.away_favorite == 1) & ((df2010.score_home - df2010.score_away) < df2010.spread_favorite)))
            / len(df2010)) * 100
        favoredCover2010 = str(favoredCover2010)
        dogCover2010 = sum(
            (((df2010.home_favorite == 1) & ((df2010.score_away - df2010.score_home) > df2010.spread_favorite)) |
             ((df2010.away_favorite == 1) & ((df2010.score_home - df2010.score_away) > df2010.spread_favorite)))
            / len(df2010)) * 100
        dogCover2010 = str(dogCover2010)

        # Print all 0 percentages
        print("\nNumber of Games Since 2010: " + str(len(df2010) - 1))
        print("Home Team Straight Up Win Percentage Since 2010: " + homeWinPctStr2010 + "%")
        print("Away Team Straight Up Win Percentage Since 2010: " + awayWinPctStr2010 + "%")
        print("Under Hit Percentage Since 2010: " + underHitStr2010 + "%")
        print("Over Hit Percentage Since 2010: " + overHitStr2010 + "%")
        print("Push Percentage Since 2010: " + pushHitStr2010 + "%")
        print("Over/Under data added for 2010 = " + overAddsUpStr2010 + "%")
        print("Games data added for 2010 = " + gamesAddsUpStr2010 + "%")
        print("Favored Win Percentage Since 2010: " + favored2010 + "%")
        print("Favorite Covers The Spread Percentage Since 2010: " + favoredCover2010 + "%")
        print("Underdog Covers The Spread Percentage Since 2010: " + dogCover2010 + "%")

# Weather Based Over/Under Percentages
def weatherInfluence(x):
    # Calculate data since 2000
    if x == 2000:
        # Variables to count how many games of each weather type has happened since 2000
        domeCount, openCount, domeOpenCount, rainCount, fogCount, rainFogCount, snowFogCount, snowCount = 0,0,0,0,0,0,0,0
        # Variables to hold how often a game hit the over or under depending on weather
        # Open dome games are treated as regular domes, rainFog is treated just as rain, snowFog is treated just as snow
        domeOver, domeUnder, openOver, openUnder, rainOver, rainUnder, fogOver, fogUnder, snowOver, snowUnder = 0,0,0,0,0,0,0,0,0,0
        # Variables for if the game was a push
        domePush, openPush, rainPush, fogPush, snowPush = 0,0,0,0,0

        for index in df.index:
            # For each if statement simply add if the game hit the over, under, or push depending on the type of weather
            if df.loc[index, 'weather_detail'] == "DOME":
                domeCount = domeCount + 1
                if df.loc[index, 'score_home'] + df.loc[index, 'score_away'] > df.loc[index, 'over_under_line']:
                    domeOver = domeOver + 1
                elif df.loc[index, 'score_home'] + df.loc[index, 'score_away'] < df.loc[index, 'over_under_line']:
                    domeUnder = domeUnder + 1
                else:
                    domePush = domePush + 1
            elif df.loc[index, 'weather_detail'] == "CLEAR":
                openCount = openCount + 1
                if df.loc[index, 'score_home'] + df.loc[index, 'score_away'] > df.loc[index, 'over_under_line']:
                    openOver = openOver + 1
                elif df.loc[index, 'score_home'] + df.loc[index, 'score_away'] < df.loc[index, 'over_under_line']:
                    openUnder = openUnder + 1
                else:
                    openPush = openPush + 1
            elif df.loc[index, 'weather_detail'] == "DOME (Open Roof)":
                domeOpenCount = domeOpenCount + 1
                if df.loc[index, 'score_home'] + df.loc[index, 'score_away'] > df.loc[index, 'over_under_line']:
                    domeOver = domeOver + 1
                elif df.loc[index, 'score_home'] + df.loc[index, 'score_away'] < df.loc[index, 'over_under_line']:
                    domeUnder = domeUnder + 1
                else:
                    domePush = domePush + 1
            elif df.loc[index, 'weather_detail'] == "Rain":
                rainCount = rainCount + 1
                if df.loc[index, 'score_home'] + df.loc[index, 'score_away'] > df.loc[index, 'over_under_line']:
                    rainOver = rainOver + 1
                elif df.loc[index, 'score_home'] + df.loc[index, 'score_away'] < df.loc[index, 'over_under_line']:
                    rainUnder = rainUnder + 1
                else:
                    rainPush = rainPush + 1
            elif df.loc[index, 'weather_detail'] == "Fog":
                fogCount = fogCount + 1
                if df.loc[index, 'score_home'] + df.loc[index, 'score_away'] > df.loc[index, 'over_under_line']:
                    fogOver = fogOver + 1
                elif df.loc[index, 'score_home'] + df.loc[index, 'score_away'] < df.loc[index, 'over_under_line']:
                    fogUnder = fogUnder + 1
                else:
                    fogPush = fogPush + 1
            elif df.loc[index, 'weather_detail'] == "Snow":
                snowCount = snowCount + 1
                if df.loc[index, 'score_home'] + df.loc[index, 'score_away'] > df.loc[index, 'over_under_line']:
                    snowOver = snowOver + 1
                elif df.loc[index, 'score_home'] + df.loc[index, 'score_away'] < df.loc[index, 'over_under_line']:
                    snowUnder = snowUnder + 1
                else:
                    snowPush = snowPush + 1
            elif df.loc[index, 'weather_detail'] == "Rain | Fog":
                rainFogCount = rainFogCount + 1
                if df.loc[index, 'score_home'] + df.loc[index, 'score_away'] > df.loc[index, 'over_under_line']:
                    rainOver = rainOver + 1
                elif df.loc[index, 'score_home'] + df.loc[index, 'score_away'] < df.loc[index, 'over_under_line']:
                    rainUnder = rainUnder + 1
                else:
                    rainPush = rainPush + 1
            elif df.loc[index, 'weather_detail'] == "Snow | Fog":
                snowFogCount = snowFogCount + 1
                if df.loc[index, 'score_home'] + df.loc[index, 'score_away'] > df.loc[index, 'over_under_line']:
                    snowOver = snowOver + 1
                elif df.loc[index, 'score_home'] + df.loc[index, 'score_away'] < df.loc[index, 'over_under_line']:
                    snowUnder = snowUnder + 1
                else:
                    snowPush = snowPush + 1

        total = domeCount + openCount + domeOpenCount + rainCount + fogCount + snowCount + rainFogCount + snowFogCount

        print("\nNumber of games in a dome since 2000: " + str(domeCount))
        print("Number of clear games since 2000: " + str(openCount))
        print("Number of Games in a open dome since 2000: " + str(domeOpenCount))
        print("Number of rain games since 2000: " + str(rainCount))
        print("Number of fog games since 2000: " + str(fogCount))
        print("Number of snow games since 2000: " + str(snowCount))
        print("Number of rainy fog games since 2000: " + str(rainFogCount))
        print("Number of snowy fog games since 2000: " + str(snowFogCount))
        print("Total number of games since 2000: " + str(total))

        # Print weather over/under/push percentages
        print("Since 2000, Clear games have hit the over " + str((openOver/openCount) * 100) + "% of the time and the under " + str((openUnder/openCount) * 100)
              + "% of the time with " + str((openPush/openCount) * 100) + "% of games being a push")
        print("Since 2000, Dome games have hit the over " + str((domeOver / (domeCount + domeOpenCount)) * 100) + "% of the time and the under " + str((domeUnder / (domeCount + domeOpenCount)) * 100)
              + "% of the time with " + str((domePush / (domeCount + domeOpenCount)) * 100) + "% of games being a push")
        print("Since 2000, Rain games have hit the over " + str((rainOver / (rainCount + rainFogCount)) * 100) + "% of the time and the under " + str((rainUnder / (rainCount + rainFogCount)) * 100)
              + "% of the time with " + str((rainPush / (rainCount + rainFogCount)) * 100) + "% of games being a push")
        print("Since 2000, Fog games have hit the over " + str((fogOver / fogCount) * 100) + "% of the time and the under " + str((fogUnder / fogCount) * 100)
              + "% of the time with " + str((fogPush / fogCount) * 100) + "% of games being a push")
        print("Since 2000, Snow games have hit the over " + str((snowOver / (snowCount + snowFogCount)) * 100) + "% of the time and the under " + str((snowUnder / (snowCount + snowFogCount)) * 100)
              + "% of the time with " + str((snowPush / (snowCount + snowFogCount)) * 100) + "% of games being a push")

    elif x == 2010:
        # Variables to count how many games of each weather type has happened since 2010
        domeCount, openCount, domeOpenCount, rainCount, fogCount, rainFogCount, snowFogCount, snowCount = 0, 0, 0, 0, 0, 0, 0, 0
        # Variables to hold how often a game hit the over or under depending on weather
        # Open dome games are treated as regular domes, rainFog is treated just as rain, snowFog is treated just as snow
        domeOver, domeUnder, openOver, openUnder, rainOver, rainUnder, fogOver, fogUnder, snowOver, snowUnder = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        # Variables for if the game was a push
        domePush, openPush, rainPush, fogPush, snowPush = 0, 0, 0, 0, 0

        for index in df2010.index:
            if df2010.loc[index, 'weather_detail'] == "DOME":
                domeCount = domeCount + 1
                if df2010.loc[index, 'score_home'] + df2010.loc[index, 'score_away'] > df2010.loc[index, 'over_under_line']:
                    domeOver = domeOver + 1
                elif df2010.loc[index, 'score_home'] + df2010.loc[index, 'score_away'] < df2010.loc[index, 'over_under_line']:
                    domeUnder = domeUnder + 1
                else:
                    domePush = domePush + 1
            elif df2010.loc[index, 'weather_detail'] == "CLEAR":
                openCount = openCount + 1
                if df2010.loc[index, 'score_home'] + df2010.loc[index, 'score_away'] > df2010.loc[index, 'over_under_line']:
                    openOver = openOver + 1
                elif df2010.loc[index, 'score_home'] + df2010.loc[index, 'score_away'] < df2010.loc[index, 'over_under_line']:
                    openUnder = openUnder + 1
                else:
                    openPush = openPush + 1
            elif df2010.loc[index, 'weather_detail'] == "DOME (Open Roof)":
                domeOpenCount = domeOpenCount + 1
                if df2010.loc[index, 'score_home'] + df2010.loc[index, 'score_away'] > df2010.loc[index, 'over_under_line']:
                    domeOver = domeOver + 1
                elif df2010.loc[index, 'score_home'] + df2010.loc[index, 'score_away'] < df2010.loc[index, 'over_under_line']:
                    domeUnder = domeUnder + 1
                else:
                    domePush = domePush + 1
            elif df2010.loc[index, 'weather_detail'] == "Rain":
                rainCount = rainCount + 1
                if df2010.loc[index, 'score_home'] + df2010.loc[index, 'score_away'] > df2010.loc[index, 'over_under_line']:
                    rainOver = rainOver + 1
                elif df2010.loc[index, 'score_home'] + df2010.loc[index, 'score_away'] < df2010.loc[index, 'over_under_line']:
                    rainUnder = rainUnder + 1
                else:
                    rainPush = rainPush + 1
            elif df2010.loc[index, 'weather_detail'] == "Fog":
                fogCount = fogCount + 1
                if df2010.loc[index, 'score_home'] + df2010.loc[index, 'score_away'] > df2010.loc[index, 'over_under_line']:
                    fogOver = fogOver + 1
                elif df2010.loc[index, 'score_home'] + df2010.loc[index, 'score_away'] < df2010.loc[index, 'over_under_line']:
                    fogUnder = fogUnder + 1
                else:
                    fogPush = fogPush + 1
            elif df2010.loc[index, 'weather_detail'] == "Snow":
                snowCount = snowCount + 1
                if df2010.loc[index, 'score_home'] + df2010.loc[index, 'score_away'] > df2010.loc[index, 'over_under_line']:
                    snowOver = snowOver + 1
                elif df2010.loc[index, 'score_home'] + df2010.loc[index, 'score_away'] < df2010.loc[index, 'over_under_line']:
                    snowUnder = snowUnder + 1
                else:
                    snowPush = snowPush + 1
            elif df2010.loc[index, 'weather_detail'] == "Rain | Fog":
                rainFogCount = rainFogCount + 1
                if df2010.loc[index, 'score_home'] + df2010.loc[index, 'score_away'] > df2010.loc[index, 'over_under_line']:
                    rainOver = rainOver + 1
                elif df2010.loc[index, 'score_home'] + df2010.loc[index, 'score_away'] < df2010.loc[index, 'over_under_line']:
                    rainUnder = rainUnder + 1
                else:
                    rainPush = rainPush + 1
            elif df2010.loc[index, 'weather_detail'] == "Snow | Fog":
                snowFogCount = snowFogCount + 1
                if df2010.loc[index, 'score_home'] + df2010.loc[index, 'score_away'] > df2010.loc[index, 'over_under_line']:
                    snowOver = snowOver + 1
                elif df2010.loc[index, 'score_home'] + df2010.loc[index, 'score_away'] < df2010.loc[index, 'over_under_line']:
                    snowUnder = snowUnder + 1
                else:
                    snowPush = snowPush + 1

        total = domeCount + openCount + domeOpenCount + rainCount + fogCount + snowCount + rainFogCount + snowFogCount

        print("\nNumber of games in a dome since 2010: " + str(domeCount))
        print("Number of clear games since 2010: " + str(openCount))
        print("Number of Games in a open dome since 2010: " + str(domeOpenCount))
        print("Number of rain games since 2010: " + str(rainCount))
        print("Number of fog games since 2010: " + str(fogCount))
        print("Number of snow games since 2010: " + str(snowCount))
        print("Number of rainy fog games since 2010: " + str(rainFogCount))
        print("Number of snowy fog games since 2010: " + str(snowFogCount))
        print("Total number of games since 2010: " + str(total))

        print("Since 2010, Clear games have hit the over " + str((openOver / openCount) * 100) + "% of the time and the under " + str((openUnder / openCount) * 100)
              + "% of the time with " + str((openPush / openCount) * 100) + "% of games being a push")
        print("Since 2010, Dome games have hit the over " + str((domeOver / (domeCount + domeOpenCount)) * 100) + "% of the time and the under " + str((domeUnder / (domeCount + domeOpenCount)) * 100)
              + "% of the time with " + str((domePush / (domeCount + domeOpenCount)) * 100) + "% of games being a push")
        print("Since 2010, Rain games have hit the over " + str((rainOver / (rainCount + rainFogCount)) * 100) + "% of the time and the under " + str((rainUnder / (rainCount + rainFogCount)) * 100)
              + "% of the time with " + str((rainPush / (rainCount + rainFogCount)) * 100) + "% of games being a push")
        print("Since 2010, Fog games have hit the over " + str((fogOver / fogCount) * 100) + "% of the time and the under " + str((fogUnder / fogCount) * 100)
              + "% of the time with " + str((fogPush / fogCount) * 100) + "% of games being a push")
        print("Since 2010, Snow games have hit the over " + str((snowOver / (snowCount + snowFogCount)) * 100) + "% of the time and the under " + str((snowUnder / (snowCount + snowFogCount)) * 100)
              + "% of the time with " + str((snowPush / (snowCount + snowFogCount)) * 100) + "% of games being a push")



# Print basic data
basicData(2000)
basicData(2010)
weatherInfluence(2000)
weatherInfluence(2010)
