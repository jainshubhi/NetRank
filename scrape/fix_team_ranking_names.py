import sys, os, pandas as pd

NO_MATCHES = {
    "fresno-st-bulldogs"            : "fresno-state", \
    "penn-st-nittany-lions"         : "penn-state", \
    "st-josephs-hawks"              : "saint-josephs", \
    "california-golden-bears"       : "california", \
    "detroit-titans"                : "detroit-mercy", \
    "csu-northridge-matadors"       : "cal-state-northridge", \
    "uc-irvine-anteaters"           : "california-irvine", \
    "charleston-cougars"            : "college-of-charleston", \
    "nc-wilmington-seahawks"        : "north-carolina-wilmington", \
    "st-johns-red-storm"            : "st-johns-ny", \
    "mcneese-st-cowboys"            : "mcneese-state", \
    "kent-st-golden-flashes"        : "kent-state", \
    "cleveland-st-vikings"          : "cleveland-state", \
    "murray-st-racers"              : "murray-state", \
    "unlv-runnin-rebels"            : "nevada-las-vegas", \
    "wis-milwaukee-panthers"        : "milwaukee", \
    "nc-state-wolfpack"             : "north-carolina-state", \
    "uab-blazers"                   : "alabama-birmingham", \
    "wright-st-raiders"             : "wright-state", \
    "boise-st-broncos"              : "boise-state", \
    "san-jose-st-spartans"          : "san-jose-state", \
    "vcu-rams"                      : "virginia-commonwealth", \
    "nc-greensboro-spartans"        : "north-carolina-greensboro", \
    "ball-st-cardinals"             : "ball-state", \
    "east-tennessee-st-buccaneers"  : "east-tennessee-state", \
    "bowling-green-falcons"         : "bowling-green-state", \
    "youngstown-st-penguins"        : "youngstown-state", \
    "long-beach-st-49ers"           : "long-beach-state", \
    "weber-st-wildcats"             : "weber-state", \
    "lipscomb-bison"                : "lipscomb", \
    "se-missouri-st-redhawks"       : "southeast-missouri-state", \
    "sam-houston-st-bearkats"       : "sam-houston-state", \
    "boston-u-terriers"             : "boston-university", \
    "uc-santa-barbara-gauchos"      : "california-santa-barbara", \
    "alcorn-st-braves"              : "alcorn-state", \
    "md-baltimore-cty-retrievers"   : "maryland-baltimore-county", \
    "umkc-kangaroos"                : "missouri-kansas-city", \
    "coppin-st-eagles"              : "coppin-state", \
    "the-citadel-bulldogs"          : "citadel", \
    "nc-asheville-bulldogs"         : "north-carolina-asheville", \
    "morehead-st-eagles"            : "morehead-state", \
    "wichita-st-shockers"           : "wichita-state", \
    "liu-brooklyn-blackbirds"       : "long-island-university", \
    "central-conn-st-blue-devils"   : "central-connecticut-state", \
    "nocarolina-at-aggies"          : "north-carolina-at", \
    "st-francis-pa-red-flash"       : "saint-francis-pa", \
    "tenn-martin-skyhawks"          : "tennessee-martin", \
    "loyola-chicago-ramblers"       : "loyola-il", \
    "appalachian-st-mountaineers"   : "appalachian-state", \
    "st-peters-peacocks"            : "saint-peters", \
    "loyola-maryland-greyhounds"    : "loyola-md", \
    "cal-st-fullerton-titans"       : "cal-state-fullerton", \
    "morgan-st-bears"               : "morgan-state", \
    "chicago-st-cougars"            : "chicago-state", \
    "vmi-keydets"                   : "virginia-military-institute", \
    "st-marys-gaels"                : "saint-marys-ca", \
    "albany-great-danes"            : "albany-ny", \
    "michigan-st-spartans"          : "michigan-state", \
    "iowa-st-cyclones"              : "iowa-state", \
    "georgia-st-panthers"           : "georgia-state", \
    "ohio-st-buckeyes"              : "ohio-state", \
    "utah-st-aggies"                : "utah-state", \
    "mississippi-st-bulldogs"       : "mississippi-state", \
    "oklahoma-st-cowboys"           : "oklahoma-state", \
    "indiana-st-sycamores"          : "indiana-state", \
    "illinois-st-redbirds"          : "illinois-state", \
    "kansas-st-wildcats"            : "kansas-state", \
    "colorado-st-rams"              : "colorado-state", \
    "alabama-st-hornets"            : "alabama-state", \
    "northwestern-st-demons"        : "northwestern-state", \
    "missouri-st-bears"             : "missouri-state", \
    "arkansas-st-red-wolves"        : "arkansas-state", \
    "oregon-st-beavers"             : "oregon-state", \
    "san-diego-st-aztecs"           : "san-diego-state", \
    "washington-st-cougars"         : "washington-state", \
    "florida-st-seminoles"          : "florida-state", \
    "new-mexico-st-aggies"          : "new-mexico-state", \
    "montana-st-bobcats"            : "montana-state", \
    "tennessee-st-tigers"           : "tennessee-state", \
    "jacksonville-st-gamecocks"     : "jacksonville-state", \
    "portland-st-vikings"           : "portland-state", \
    "maryland-e-shore-hawks"        : "maryland-eastern-shore", \
    "indiana-purdue-jaguars"        : "iupui", \
    "texas-am-cc-islanders"         : "texas-am-corpus-christi", \
    "southern-miss-golden-eagles"   : "southern-mississippi", \
    "texas-rio-grande-valley-vaqueros" : "texas-pan-american", \
    "gardner-webb-runnin-bulldogs"  : "gardner-webb", \
    "william--mary-tribe"           : "william-mary", \
    "western-carolina-catamounts"   : "western-carolina", \
    "uc-riverside-highlanders"      : "california-riverside", \
    "savannah-state-tigers"         : "savannah-state", \
    "iupu-ft-wayne-mastodons"       : "ipfw", \
    "uc-davis-aggies"               : "california-davis", \
    "gardner-webb-runnin-bulldogs"  : "gardner-webb", \
    "texas-am-cc-islanders"         : "texas-am-corpus-christi", \
    "lipscomb-bison"                : "lipscomb", \
    "kennesaw-st-fighting-owls"     : "kennesaw-state", \
    "new-jersey-tech-highlanders"   : "njit", \
    "siu-edwardsville-cougars"      : "southern-illinois-edwardsville", \
    "binghamton-bearcats"           : "binghamton", \
    "stetson-hatters"               : "stetson", \
    "nebraska-omaha-mavericks"      : "nebraska-omaha", \
    "north-carolina-central-eagles" : "north-carolina-central", \
    "presbyterian-blue-hose"        : "presbyterian", \
    "south-carolina-upstate-spartans" : "south-carolina-upstate", \
    "bryant-bulldogs"               : "bryant", \
    "north-dakota-fighting-hawks"   : "north-dakota", \
    "lamar-cardinals"               : "lamar", \
    "seattle-redhawks"              : "seattle", \
    "south-dakota-coyotes"          : "south-dakota", \
    "houston-baptist-huskies"       : "houston-baptist", \
    "california-davis"              : "california-davis", \
    "new-orleans-privateers"        : "new-orleans"
}

def hamming_score(string1, string2):
    a = string1[: min(len(string1), len(string2))]
    b = string2[: min(len(string1), len(string2))]
    ham = 0
    for char1, char2 in zip(a, b):
        if char1 != char2:
            ham += 1
        elif char1 == "-" and char2 == "-":
            ham += 1
    return ham + abs(len(string1) - len(string2))

def valid_name(suggested_name, raw_name, CUR_SEASON_RANKS):
    if raw_name not in CUR_SEASON_RANKS or raw_name == "#VALUE!":
        return True
    else:
        rank, existing_name = CUR_SEASON_RANKS[raw_name]
        ham1 = hamming_score(existing_name, raw_name)
        ham2 = hamming_score(suggested_name, raw_name)
        if ham1 > ham2:
            # print("Found better!")
            # print("Existing:  " + str(existing_name))
            # print("Suggested: " + str(suggested_name))
            # print("Raw Name:  " + raw_name)
            return True
            del CUR_SEASON_RANKS[raw_name]
        else:
            return False

def get_teams_in_this_season(COMPARE_FILE_NAME):
    '''
    Get a list of teams in this current season.
    '''
    list_of_teams = []
    compare_file = pd.read_csv(COMPARE_FILE_NAME)
    for ind, row in compare_file.iterrows():
        team_1 = row['team_1']
        team_2 = row['team_2']
        if team_1 not in list_of_teams:
            list_of_teams.append(team_1)
        if team_2 not in list_of_teams:
            list_of_teams.append(team_2)
    return list_of_teams

def make_new_season_dir(CUR_SEASON):
    '''
    Creates a new directory to store rankings for this season.
    '''
    SEASON_DIR = "team_rankings/" + CUR_SEASON.replace("-","_")
    if not os.path.exists(SEASON_DIR):
        os.makedirs(SEASON_DIR)
    return SEASON_DIR

def verify_and_write_season_rankings(CUR_SEASON_RANKS, TEAM_LIST, CUR_FILE, \
                            CUR_FILE_NAME):
    '''
    Performs some basic tests and writes the power rankings to the 
    current output file.
    '''
    # Sort by rank
    FINAL = []
    POWER_RANKS = zip(CUR_SEASON_RANKS.keys(), CUR_SEASON_RANKS.values())
    for team, (rank, parsed_team) in POWER_RANKS:
        FINAL.append((rank, parsed_team))

    FINAL_LIST = sorted(FINAL, key = lambda x : x[0])
    FINAL_LIST_COPY = []

    # Ensure one-to-one mapping of derived names and existing names
    matched_names = []
    num_shifts    = 0
    for i, (rank, new_name) in enumerate(FINAL_LIST):
        if num_shifts != 0:
            rank = rank - num_shifts
        found_match = False
        for team in TEAM_LIST:
            if new_name == team:
                if new_name not in matched_names:
                    found_match = True
                    matched_names.append(new_name)
                    FINAL_LIST_COPY.append((rank, new_name))
                else:
                    print("[ERROR] already matched! : " + new_name + " (" + \
                                CUR_FILE_NAME + ")")
        if not found_match:
            num_shifts += 1
            # print("[WARNING] new name, removed: " + new_name + " (" + \
            #         CUR_FILE_NAME + ")")

    FINAL_LIST = FINAL_LIST_COPY

    # Ensure each ranking shows up exactly once
    cur_rank = 1
    for rank, new_name in FINAL_LIST:
        if cur_rank != int(rank):
            print("[ERROR] rank: " + str(rank) + " (" + CUR_FILE_NAME + ")")
        cur_rank += 1

    for rank, new_name in FINAL_LIST:
        CUR_FILE.write(str(rank) + "," + new_name + "\n")

if __name__ == "__main__":

    INPUT_FILE        = pd.read_csv("team_rankings/main.csv").dropna(how="any")
    CUR_SEASON        = str(INPUT_FILE.iloc[0]["season"])
    CUR_DATE          = str(INPUT_FILE.iloc[0]["date"])
    SEASON_DIR        = make_new_season_dir(CUR_SEASON)
    CUR_FILE_NAME     = SEASON_DIR + "/" + CUR_DATE.replace("-","_") + ".csv"
    CUR_FILE          = open(CUR_FILE_NAME, "w")
    CUR_FILE.write("rank,team\n")
    COMPARE_FILE_NAME = "basketball/seasons/" + CUR_SEASON[-4:] + "_pro.csv"
    TEAM_LIST         = get_teams_in_this_season(COMPARE_FILE_NAME)
    CUR_SEASON_RANKS  = {}
    ACTUAL_RANK       = 1
    NUM_ROWS          = len(INPUT_FILE)

    for ind, row in INPUT_FILE.iterrows():
        rank   = str(int(row["rank"]))
        team   = str(row["team"])
        season = str(row["season"])
        date   = str(row["date"])

        if season != CUR_SEASON:
            CUR_SEASON = season
            if CUR_SEASON == "2014-2015":
                exit(1)
            SEASON_DIR = make_new_season_dir(CUR_SEASON)
            COMPARE_FILE_NAME = "basketball/seasons/" + CUR_SEASON[-4:] + \
                                "_pro.csv"
            TEAM_LIST = get_teams_in_this_season(COMPARE_FILE_NAME)

        if date != CUR_DATE:
            verify_and_write_season_rankings(CUR_SEASON_RANKS, TEAM_LIST, \
                            CUR_FILE, CUR_FILE_NAME)
            CUR_FILE.close() # Close existing ranking date file
            CUR_DATE      = date
            CUR_FILE_NAME = SEASON_DIR + "/" + CUR_DATE.replace("-","_") + \
                            ".csv"
            CUR_FILE      = open(CUR_FILE_NAME, "w") # Open up the new file
            CUR_FILE.write("rank,team\n") # Write header of the new file
            CUR_SEASON_RANKS = {}
            ACTUAL_RANK      = 1

        if team == "#VALUE!":
            pass

        elif team in NO_MATCHES:
            CUR_SEASON_RANKS[team] = (ACTUAL_RANK, NO_MATCHES[team])
            ACTUAL_RANK += 1

        else:
            for official_team in TEAM_LIST:
                parsed_team = team[: len(official_team)]
                if parsed_team == official_team:
                    if valid_name(parsed_team, team, CUR_SEASON_RANKS):
                        if parsed_team == "california" and \
                            CUR_SEASON == "2000-2001":
                            parsed_team = "university-of-california"
                        CUR_SEASON_RANKS[team] = (ACTUAL_RANK,parsed_team)
            ACTUAL_RANK += 1

        sys.stdout.write("Progress: " + str(round((1.0 * ind) / NUM_ROWS, 3)) + "\r")
        sys.stdout.flush()
