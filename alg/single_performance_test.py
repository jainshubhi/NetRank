# NetRank
# Caltech 
# Spring 2016
# Ricky Galliani and Shubhankar Jain

import sys
import pandas as pd
import util as u

if __name__ == "__main__":

    # Process command-line arguments
    season_gamelog_file = sys.argv[1]
    us_rankings_file = sys.argv[2]
    them_rankings_file = sys.argv[3]

    # Get data from input files
    us_rankings = u.get_rankings_as_list(us_rankings_file)
    season = pd.read_csv(season_gamelog_file)

    # Compute Retrodictive Accuracy and Spearman Correlation Coefficent
    acc       = u.compute_weighted_retro_acc(season, -1, us_rankings)
    spearman  = u.compute_spearman(them_rankings_file, us_rankings, -1)
    print("Retrodictive Accuracy  : " + str(acc) + "%.")
    print("Spearman Coefficient   : " + str(spearman) + ".")