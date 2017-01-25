# NetRank
# Caltech
# Spring 2016
# Ricky Galliani and Shubhankar Jain

# --- MODULE IMPORTS ---

import sys, os, time
import pandas as pd, datetime as dt
import newman_park as np, pagerank as pr, hits as hi, eigenvector as e, bfs
import borda_count as bc, copeland as co
import linear_combination as lc, netrank as nr, kemeny_young as ky, idk_agg as idk
import visualize_performance as viz,  util as u

# ----------------------

SPORTS = ["-b", "-f"] # Basketball and football
ALGS   = { # All algorithm modules
            "-np"  : np.newman_park, \
            "-wnp" : np.weighted_newman_park, \
            "-pr"  : pr.pagerank, \
            "-ipr" : pr.indirect_pagerank, \
            "-wpr" : pr.weighted_pagerank, \
            "-iwpr": pr.indirect_weighted_pagerank, \
            "-hi"  : hi.hits, \
            "-ihi" : hi.indirect_hits, \
            "-sub" : hi.sub_hub, \
            "-e"   : e.eigenvector, \
            "-ie"  : e.indirect_eigenvector, \
            "-bfs" : bfs.BFS, \
            "-wbfs": bfs.weighted_BFS, \
            "-bc"  : bc.borda_count, \
            "-fbc" : bc.fractional_borda_count, \
            "-lbc" : bc.borda_count_3, \
            "-co"  : co.copeland, \
            "-col" : co.copeland_log, \
            "-ky"  : ky.kemeny_young, \
            "-idk" : idk.idk_agg\
         }

# "margin_of_vic", "margin_of_2pa", "margin_of_2pp", "margin_of_3pa"
# "margin_of_3pp" 
FEATURES = ["margin_of_fta", "margin_of_ftp", \
            "margin_of_orb", "margin_of_drb", "margin_of_stl", \
            "margin_of_ast", "margin_of_blk", "margin_of_tov"]

SEASONS = [("2010","2011"), ("2011","2012"), ("2012","2013"), ("2013","2014")]

# ----------------------

def USAGE():
    '''
    Usage statement.
    '''
    print("""\nUSAGE:
    $ python season_simulation.py -b <ALG> <SEASON_END_YEAR>; or
    """)

if __name__ == "__main__":

    # Sanity check command-line arguments
    if len(sys.argv) != 4:
        USAGE()
        exit(1)
    if sys.argv[1] not in SPORTS or sys.argv[2] not in ALGS:
        USAGE()
        exit(1)

    # Process command-line arguments (sports, algorithm to run, season)
    SPORT        = "basketball" if sys.argv[1] == "-b" else "football"
    ALG          = ALGS[sys.argv[2]]
    NUM_RANKINGS = int(sys.argv[3]) # Number of rankings for this season

    # Loop through the last NUM_RANKINGS of the season
    for feat in FEATURES:

        retro_accs = []
        weighted_retro_accs = []
        spearmans = []
        comp_times = []

        for PREV_SEASON, SEASON in SEASONS:
            # Specify output directories and create them, if necessary
            SEASON_DIR_NAME  = PREV_SEASON + "_" + SEASON + "/"
            OUTPUT_DIR       = "../results/" + SPORT + "/" + sys.argv[2][1:] + \
                                 "/" + SEASON_DIR_NAME
            if not os.path.exists(OUTPUT_DIR):
                os.makedirs(OUTPUT_DIR)

            # Locate season log input file, report an error and terminate if there is
            # a problem
            try:
                SEASON_LOG   = "../data/" + SPORT + "/season_log/" + SEASON + ".csv"
                SEASON       = pd.read_csv(SEASON_LOG)
            except:
                print("[ERROR]: season log " + SEASON_LOG + " does not exist.")
                print(sys.exc_info())
                exit(1)

            # Locate the published power rankings input files for this season, report
            # an error and terminate if there is a problem
            try:
                D             = "../data/" + SPORT + "/team_ranking/" + SEASON_DIR_NAME
                PUB_RANKINGS  = [D + f for f in os.listdir(D) if os.path.isfile(D + f)]
                RANKING_DATES = [u.get_date_from_filename(f[-14:]) for f in PUB_RANKINGS]
                RANKING_DATES.sort()
            except:
                print("[ERROR]: could not find power ranking directory " + D)
                print(sys.exc_info())
                exit(1)

                # Compute rankings, retrodictive accuracy, weighted accuracy, 
                # for each feature

            for date in [RANKING_DATES[-NUM_RANKINGS]]:

                season = PREV_SEASON + "_" + str(int(PREV_SEASON) + 1) + "/"
                if date.month < 10:
                    mon = "0" + str(date.month)
                else:
                    mon = str(date.month)
                if date.day < 10:
                    day = "0" + str(date.day)
                else:
                    day = str(date.day)
                
                date_str = mon + "_" + day + "_" + str(date.year)
                f = "../data/basketball/team_ranking/" + season + \
                    date_str + ".csv"

                # Start the timer for computing power rankings for this date.
                start = time.time()

                # Return the graph and the number of nodes (teams)
                G, N        = u.build_season_graph(SEASON, date, feat)

                # Run the user-specified algorithm
                rankings, _ = ALG(G)

                # Write out the rankings to an output file
                rankings    = u.prune_rankings(rankings)
                date_str    = date.strftime('%m/%d/%Y').replace("/","_")
                output_file = OUTPUT_DIR + date_str + "/" + feat + ".csv"
                u.write_rankings(date, rankings, output_file)

                # Compute and report quality of rankings (retro accuracy and spearman)
                acc          = u.compute_retro_acc(SEASON, date, rankings)
                weighted_acc = u.compute_weighted_retro_acc(SEASON, date, rankings)
                spearman     = u.compute_spearman(f, rankings, -1)
                comp         = str(round(time.time() - start, 3))

                # Print progress of simulation to console
                # u.print_simulation_results(date_str, acc, weighted_acc, spearman, \
                #                    comp, len(G.nodes()), len(rankings), output_file)

                # Add the metrics to the list
                retro_accs.append(acc)
                weighted_retro_accs.append(weighted_acc)
                spearmans.append(spearman)
                comp_times.append(comp)

        retro_acc = sum(retro_accs) / len(retro_accs)
        w_retro_acc = sum(weighted_retro_accs) / len(weighted_retro_accs)
        spearman = sum(spearmans) / len(spearmans)
        season = str(int(PREV_SEASON) + 1)
        print("        --- " + feat + " (" + sys.argv[2] + ") ---")
        print("AVG RETRODICTIVE ACCURACY           : " + str(retro_acc))
        print("AVG WEIGHTED RETRODICTIVE ACCURACY  : " + str(w_retro_acc))
        print("AVG SPEARMAN CORRELATION COEFFICIENT: " + str(spearman) + "\n")
