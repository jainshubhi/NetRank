# NetRank
# Caltech
# Spring 2016
# Ricky Galliani and Shubhankar Jain

import networkx as nx, pandas as pd, numpy as np, random as r
import datetime as dt, sys, operator, time
import util as u
from itertools import groupby

LEVEL_CUTOFF = 3
LAMBDA       = 0.7

def BFS(G):
    '''
    Runs the unweighted BFS algorithm on the input graph to compute power
    rankings.
    http://snap.stanford.edu/class/cs224w-readings/borodin05pagerank.pdf.
    '''
    RANKINGS   = []
    LEVELS     = {}
    SCORES     = {}
    for team in G.nodes():
        SCORES[team] = 0.0 # Init a score for each team
        LEVELS[team] = [0.0] * LEVEL_CUTOFF

    RANK                     = 1 # Rankings start at 1
    NUM_TEAMS                = len(G.nodes())

    for i, team_a in enumerate(G.nodes()):
        # Compute direct win-loss differential as in-degree - out-degree
        w_l_differential  = G.in_degree(team_a) - G.out_degree(team_a)
        SCORES[team_a]   += w_l_differential
        LEVELS[team_a][0] = w_l_differential

        for team_b in G.nodes():
            # Find all paths (indirect victories) from team b to team a
            # which are represented on the graph as directed edges from
            # Team B to Team A
            paths = nx.all_simple_paths(G, source=team_b, target=team_a, \
                                           cutoff=LEVEL_CUTOFF)
            for path in paths:
                level = len(path)
                ind = level - 2 # Index within LEVELS list
                if ind == 0:
                    continue
                contribution = 1 / float(2 ** ((2 * ind) - 1))
                # Team A won, hand them points for an indirect victory
                SCORES[team_a]      += contribution
                LEVELS[team_a][ind] += contribution
                # Team B lost, hand them points for an indirect loss
                SCORES[team_b]      -= LAMBDA * contribution
                LEVELS[team_b][ind] -= LAMBDA * contribution

        # Print progress of computation to the console
        # u.print_simulation_progress(team_a, i, NUM_TEAMS)

    SCORES_LST = sorted(SCORES.items(), key = lambda x : x[1], reverse = True)
    for teams, scores in groupby(SCORES_LST, lambda x : x[1]):
        grp = [(RANK, tup[0]) for tup in scores if not tup[0][2:].isdigit()]
        RANKINGS += grp
        RANK += len(grp) # Increase rank for next grouping

    return RANKINGS, len(RANKINGS)

def weighted_BFS(G):
    '''
    This computes the rankings of teams according to the BFS algorithm 
    described at this web address
    http://snap.stanford.edu/class/cs224w-readings/borodin05pagerank.pdf.
    '''
    RANKINGS   = []
    LEVELS     = {}
    SCORES     = {}
    for team in G.nodes():
        SCORES[team] = 0.0 # Init a score for each team
        LEVELS[team] = [0.0] * LEVEL_CUTOFF

    RANK                     = 1 # Rankings start at 1
    NUM_TEAMS                = nx.number_of_nodes(G)

    for i, team_a in enumerate(G.nodes()):
        for team_b in G.nodes():
            # Find all paths (indirect victories) from team b to team a
            # which are represented on the graph as directed edges from
            # Team B to Team A
            paths = nx.all_simple_paths(G, source = team_b, target = team_a, \
                                           cutoff = LEVEL_CUTOFF)
            for path in paths:
                level = len(path)
                ind = level - 2 # Index within LEVELS list
                if ind == 0: # Direct win for team A
                    team_b, team_a = path
                    contribution = u.get_weight(G, team_b, team_a)
                # A win of degree greater than 2 for team A
                else:
                    contribution = 0
                    for team_source, team_dest in zip(path[:-1], path[1:]):
                        contribution += u.get_weight(G, team_source, team_dest)
                    # Multiply the contributions by the attentuation factor
                    contribution *= 1 / float(2 ** ((2 * ind) - 1))

                # Team A won, hand them points for an indirect victory
                SCORES[team_a]      += contribution
                LEVELS[team_a][ind] += contribution
                # Team B lost, hand them points for an indirect loss
                SCORES[team_b]      -= LAMBDA * contribution
                LEVELS[team_b][ind] -= LAMBDA * contribution

        # Print progress of computation to the console
        # u.print_simulation_progress(team_a, i, NUM_TEAMS)

    SCORES_LST = sorted(SCORES.items(), key = lambda x : x[1], reverse = True)
    for teams, scores in groupby(SCORES_LST, lambda x : x[1]):
        grp = [(RANK, tup[0]) for tup in scores if not tup[0][2:].isdigit()]
        RANKINGS += grp
        RANK += len(grp) # Increase rank for next grouping

    return RANKINGS, len(RANKINGS)
