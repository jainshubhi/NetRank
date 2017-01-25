# NetRank
# Caltech 
# Spring 2016
# Ricky Galliani and Shubhankar Jain

# --- MODULE IMPORTS ---

import sys, os, time
import pandas as pd
import pagerank as pr, katz as kz 
import linear_combination as lc, netrank as nr
import visualize_performance as viz, datetime as dt, util as u

# ----------------------

def USAGE():
    '''
    Usage statement.
    '''
    print("""\nUSAGE:
    $ python season_simulation.py -b <SEASON_END_YEAR>;   OR
    $ python season_simulation.py -f <SEASON_START_YEAR>; 
    """)

FEATURES = ["margin_of_vic", "margin_of_2pa", "margin_of_2pp", \
            "margin_of_3pa", "margin_of_3pp", "margin_of_fta", \
            "margin_of_ftp", "margin_of_orb", "margin_of_drb", \
            "margin_of_ast", "margin_of_stl", "margin_of_blk", "margin_of_tov"]

if __name__ == "__main__":

    if len(sys.argv) != 3:
        USAGE()
        exit(1)     
    bad_spt = sys.argv[1] != "-b"  and sys.argv[1] != "-f"
    if bad_spt:
        USAGE()
        exit(1)

    # Process command-line arguments (sports, algorithm to run, season)
    SPORT       = "basketball" if sys.argv[1] == "-b" else "football"
    SEASON      = int(sys.argv[2])
    PREV_SEASON = str(SEASON - 1)
    SEASON      = str(SEASON)

    # Specify output directories and create them, if necessary
    SEASON_DIR_NAME  = PREV_SEASON + "_" + SEASON + "/"
    OUTPUT_DIR_PR    = "../results/" + SPORT + "/pr/" + SEASON_DIR_NAME 
    OUTPUT_DIR_WPR   = "../results/" + SPORT + "/wpr/" + SEASON_DIR_NAME

    # Make the output directories if they don't already exist
    if not os.path.exists(OUTPUT_DIR_PR):
        os.makedirs(OUTPUT_DIR_PR)
    if not os.path.exists(OUTPUT_DIR_WPR):
        os.makedirs(OUTPUT_DIR_WPR)

    # Locate season log input file, report an error and terminate if there is 
    # a problem
    try:
        SEASON_LOG = "../data/" + SPORT + "/season_log/" + SEASON + "_full.csv"
        SEASON     = pd.read_csv(SEASON_LOG)
    except:
        print("[ERROR]: season log " + SEASON_LOG + " does not exist.")
        exit(1)

    # Locate the published power rankings input files for this season, report
    # an error and terminate if there is a problem
    try:
        D             = "../data/" + SPORT + "/team_ranking/" + SEASON_DIR_NAME
        PUB_RANKINGS  = [D + f for f in os.listdir(D) if os.path.isfile(D + f)]
        RANKING_DATES = [u.get_date_from_filename(f[-14:]) for f in PUB_RANKINGS]
        RANKING_DATES.sort()
    except:
        print("[ERROR]: could not find power ranking directory " + D )
        print(sys.exc_info())
        exit(1)

    # Keep track of the previous date
    prev_date = RANKING_DATES[0]

    for date in RANKING_DATES:
        if date.month == 3 and date.day >= 20 and SPORT == "basketball":
            # Restrict rankings to rankings before the NCAA tournament
            break
        
        # Create a feature network for each feature for each date in the 
        # season
        for feat in FEATURES:
            # Return the graph and the number of nodes (teams)
            G, _     = u.build_season_graph(SEASON, date, feat) 

            # Generate a set of rankings with a non-weighted season graph
            rankings_pr  = pr.pagerank(G)
            # Generate a set of rankings with a weighted season graph
            rankings_wpr = pr.weighted_pagerank(G)

            # Write out the rankings to an output file
            rankings        = u.prune_rankings(rankings_pr)
            rankings_wpr    = u.prune_rankings(rankings_wpr)
            date_str        = date.strftime('%m/%d/%Y').replace("/","_")
            output_file_pr  = OUTPUT_DIR_PR + date_str + "_" + feat + ".csv"
            output_file_wpr = OUTPUT_DIR_WPR + date_str + "_" + feat + ".csv"
            u.write_rankings(date, rankings_pr, output_file_pr) 
            u.write_rankings(date, rankings_wpr, output_file_wpr)

            # Update the console with what just happened
            print(feat + ": " + str(date_str) + ".")



