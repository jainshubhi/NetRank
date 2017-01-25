# NetRank
# Caltech
# Spring 2016
# Ricky Galliani and Shubhankar Jain

from itertools import groupby
import networkx as nx, pandas as pd, visualize_performance as viz
import datetime as dt
import time, sys, os, util

LEVEL_CUTOFF             = 3 # Considering all paths of this length or less
LAMBDA                   = 0.25

def newman_park(G):
    '''
    Runs the Newman Park algorithm on the input graph to compute power
    rankings.
    '''
    SCORES                   = {}
    LEVELS                   = {}
    RANKINGS                 = []
    RANK                     = 1 # Rankings start at 1
    NUM_TEAMS                = len(G.nodes())

    for team in G.nodes():
        SCORES[team] = 0.0 # Init a score for each team
        LEVELS[team] = [0.0] * LEVEL_CUTOFF

    for i, team_a in enumerate(G.nodes()):
        # Compute direct win-loss differential as in-degree - out-degree
        w_l_differential = G.in_degree(team_a) - G.out_degree(team_a)
        SCORES[team_a]   += w_l_differential
        LEVELS[team_a][0] = w_l_differential

        for team_b in G.nodes():
            # Find all paths (indirect victories) of Team A over Team B
            # which are represented on the graph as directed edges from
            # Team B to Team A
            paths = nx.all_simple_paths(G, source=team_b, target=team_a, \
                                           cutoff=LEVEL_CUTOFF)

            for path in paths:
                level = len(path)
                ind = level - 2 # Index within LEVELS list
                if ind == 0:
                    continue
                contribution = LAMBDA ** level
                # Team A won, hand them points for an indirect victory
                SCORES[team_a]      += contribution
                LEVELS[team_a][ind] += contribution
                # Team B lost, hand them points for an indirect loss
                SCORES[team_b]      -= contribution
                LEVELS[team_b][ind] -= contribution

        # Print progress of computation to the console
        util.print_simulation_progress(team_a, i, NUM_TEAMS)

    SCORES_LST = sorted(SCORES.items(), key = lambda x : x[1], reverse = True)
    for teams, scores in groupby(SCORES_LST, lambda x : x[1]):
        grp = [(RANK, tup[0]) for tup in scores]
        RANKINGS += grp
        RANK += len(grp) # Increase rank for next grouping

    return RANKINGS

def get_date_from_filename(f):
    '''
    Returns 10/16/2000 from "2000_10_16.csv."
    '''
    year = f[-14:-10]
    day  = f[-6:-4]
    mon  = f[-9:-7]
    return (mon + "/" + day + "/" + year)

def print_simulation_progress(team, i, NUM_TEAMS):
    '''
    Writes the computation progress to the console.
    '''
    progress = str(round(((1.0 * i) / NUM_TEAMS) * 100, 1))
    bar = progress + "%. " + team + ".                      \r"
    sys.stdout.write(bar)
    sys.stdout.flush()

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("python netrank.py <YEAR>")
        exit(1)

    SEASON      = int(sys.argv[1])
    prev_season = str(SEASON - 1)
    SEASON      = str(SEASON)
    SEASON_DIR  = "team_rankings/" + prev_season + "_" + SEASON + "/"
    if not os.path.exists(SEASON_DIR):
        os.makedirs(SEASON_DIR)
    try:
        INPUT_FILE_NAME = "basketball/seasons/" + SEASON + "_pro.csv"
    except:
        print("[ERROR]: input file " + INPUT_FILE + " does not exist.")
        exit(1)

    pr_files = [f for f in os.listdir(SEASON_DIR) \
                                            if os.path.isfile(SEASON_DIR + f)]
    DATES    = [get_date_from_filename(f) for f in pr_files]

    ACCURACIES          = []
    SPEARMANS           = []
    COMPUTATION_TIMES   = []

    for f, date in zip(pr_files, DATES):

        # Start the timer for computing power rankings for this date.
        START = time.time()

        DATE_CMP = dt.datetime.strptime(date, "%m/%d/%Y")
        if DATE_CMP.month == 3 and DATE_CMP.day >= 20:
            break

        if not os.path.exists("results"):
            os.makedirs("results")

        # Build the graph for the input season
        G        = util.build_season_graph(INPUT_FILE_NAME, DATE_CMP)
        # Run the Newman Park algorithm
        RANKINGS = newman_park(G)
        # Write out the rankings to an output file
        util.write_rankings(date, SEASON_DIR, RANKINGS)
        # Compute and report quality of rankings (retro accuracy and spearman)
        acc  = util.compute_retro_acc(date, DATE_CMP, INPUT_FILE_NAME, RANKINGS)
        spearman  = util.compute_spearman(f, date, SEASON_DIR)
        comp      = str(round(time.time() - START, 3))
        num_teams = str(len(G))
        bar1 = date + ": " + str(acc) + "%, " + str(spearman)
        bar2 = " (" + str(comp) + " secs) [" + num_teams + "]              \n"
        print(bar1 + bar2)

        ACCURACIES.append(acc)
        SPEARMANS.append(spearman)
        COMPUTATION_TIMES.append(comp)

    VIZ_DATES = []
    for i, date in enumerate(DATES):
        if i >= len(ACCURACIES):
            break
        VIZ_DATES.append(dt.datetime.strptime(date, "%m/%d/%Y"))

    viz.visualize_results(VIZ_DATES, ACCURACIES, SPEARMANS, COMPUTATION_TIMES)

    write_rankings() # Write out the rankings to an output file
