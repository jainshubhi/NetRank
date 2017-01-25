# NetRank

import pandas as pd

DATA        = pd.read_csv("main.csv")
DATA        = DATA.fillna(" ")
OUTPUT_FILE = open("main_out.csv", "w")
CUR_DATE    = -1
CUR_GAMES   = {}

def write_games(CUR_GAMES):
    '''
    '''
    for date, team_1, team_2, margin in CUR_GAMES.values():
        row = date + "," + team_1 + "," + team_2 + "," + str(margin) + "\n"
        OUTPUT_FILE.write(row)

if __name__ == "__main__":
    OUTPUT_FILE.write("date,team_1,team_2,margin_of_victory\n")
    for ind, row in DATA.iterrows():
        DATE            = row['date']
        TEAM_1          = row['team_1']
        TEAM_2          = row['team_2']
        MARGIN          = row['margin_of_victory']
        if CUR_DATE == -1:
            CUR_DATE = DATE
        if DATE != CUR_DATE:
            write_games(CUR_GAMES)
            # Switching days!
            CUR_DATE = DATE
            CUR_GAMES = {}
        else:
            potential_existing_key = (DATE, TEAM_2, TEAM_1)
            key = (DATE, TEAM_1, TEAM_2)
            if key in CUR_GAMES:
                continue
            if potential_existing_key not in CUR_GAMES:
                # Found a new game!
                CUR_GAMES[key] = [DATE,TEAM_1,TEAM_2,MARGIN]

    OUTPUT_FILE.close()
