# NetRank
# Caltech 
# Spring 2016
# Ricky Galliani and Shubhankar Jain

import numpy as nmp, pandas as pd, matplotlib.pyplot as plt
import util as u
from sklearn import linear_model

def linearly_combine(rankings, seeds):
    """
    Runs the PageRank and Newman Park algorithms and then finds the optimal 
    linear combination of the two rankings and outputs this optimal linear 
    combination as the rankings.
    """

    """
    # First make sure every set of feature rankings has the same length
    len_rankings = len(rankings.keys()[0])
    for feature in rankings:
        assert(len(rankings[feature]) == len_rankings)

    # No need to linearly combine the rankings if they have no length
    if len_rankings == 0:
        print("[ERROR]: linearly_combine() returning the NP MOV rankings.")
        return rankings["mov"]
    """

    lc_rankings = {} # A dictionary to store the rankings

    # Loop through each ranking and assign 
    for feature, feature_rankings in enumerate(rankings):
        # Get the beta to multiply each ranking by for this future
        beta = seeds[feature] 
        for (rank, team) in feature_rankings:
            contribution = beta * rank
            if team not in lc_rankings:
                lc_rankings[team] = contribution
            else: # Team is already in the linear combination dictionary
                lc_rankings[team] += contribution

    # Sort the items by their rank but take only the team names because ranks
    # will be rest
    lc_rankings = [x for (x,y) in sorted(lc_rankings.items(), key = lambda x : x[1])]

    # Make the list of rankings with the new indices 
    lc_rankings = [(i + 1,tm) for (i,tm) in enumerate(lc_rankings)]

    return lc_rankings


