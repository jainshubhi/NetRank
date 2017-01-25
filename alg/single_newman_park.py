# NetRank
# Caltech 
# Spring 2016
# Ricky Galliani and Shubhankar Jain

import sys, os
import pandas as pd, networkx as nx
import util as u, newman_park as np


if __name__ == "__main__":
    season = pd.read_csv("../data/basketball/season_log/2011_full.csv")
    official_rankings_file = "../data/basketball/team_ranking/2010_2011/03_14_2011.csv"
    G, _ = u.build_season_graph(season, -1, "margin_of_vic")
    rankings = np.weighted_newman_park(G)
    output_dir = "../results/basketball/wnp/2010_2011/"
    file = output_dir + "03_14_2011_margin_of_vic.csv"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    u.write_rankings(-1, rankings, file)

    acc = u.compute_retro_acc(season, -1, rankings)
    spearman = u.compute_spearman(official_rankings_file, rankings, -1)
    print("Retrodictive Accuracy  : " + str(acc) + "%.")
    print("Spearman Coefficient   : " + str(spearman) + ".")
