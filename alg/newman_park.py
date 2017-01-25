# NetRank
# Caltech
# Spring 2016
# Ricky Galliani and Shubhankar Jain

from itertools import groupby
import networkx as nx, sys, json, util

LEVEL_CUTOFF             = 3 # Considering all paths of this length or less
LAMBDA                   = 0.8 # Attenuation factor

def newman_park(G):
    '''
    Runs the Newman Park algorithm on the input graph to compute power
    rankings.
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
        w_l_differential  = ((2 - LAMBDA) * G.in_degree(team_a)) - G.out_degree(team_a)
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
                contribution = LAMBDA ** (level - 1)
                # Team A won, hand them points for an indirect victory
                SCORES[team_a]      += (2 - LAMBDA) * contribution
                LEVELS[team_a][ind] += (2 - LAMBDA) * contribution
                # Team B lost, hand them points for an indirect loss
                SCORES[team_b]      -= contribution
                LEVELS[team_b][ind] -= contribution

        # Print progress of computation to the console
        # util.print_simulation_progress(team_a, i, NUM_TEAMS)

    SCORES_LST = sorted(SCORES.items(), key = lambda x : x[1], reverse = True)
    for teams, scores in groupby(SCORES_LST, lambda x : x[1]):
        grp = [(RANK, tup[0]) for tup in scores if not tup[0][2:].isdigit()]
        RANKINGS += grp
        RANK += len(grp) # Increase rank for next grouping

    return RANKINGS, len(RANKINGS)

def weighted_newman_park(G):
    '''
    Runs the Newman Park algorithm on the input graph to compute power
    rankings.
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
                    contribution = util.get_weight(G, team_b, team_a)
                # A win of degree greater than 2 for team A
                else:
                    contribution = 0
                    for team_source, team_dest in zip(path[:-1], path[1:]):
                        e_weight = util.get_weight(G, team_source, team_dest)
                        contribution += e_weight
                    # Multiply the contributions by the attentuation factor
                    contribution *= LAMBDA ** level

                # Team A won, hand them points for an indirect victory
                SCORES[team_a]      += contribution
                LEVELS[team_a][ind] += contribution
                # Team B lost, hand them points for an indirect loss
                SCORES[team_b]      -= (2 - LAMBDA) * contribution
                LEVELS[team_b][ind] -= (2 - LAMBDA) * contribution

        # Print progress of computation to the console
        # util.print_simulation_progress(team_a, i, NUM_TEAMS)

    SCORES_LST = sorted(SCORES.items(), key = lambda x : x[1], reverse = True)
    for teams, scores in groupby(SCORES_LST, lambda x : x[1]):
        grp = [(RANK, tup[0]) for tup in scores if not tup[0][2:].isdigit()]
        RANKINGS += grp
        RANK += len(grp) # Increase rank for next grouping

    return RANKINGS, len(RANKINGS)
