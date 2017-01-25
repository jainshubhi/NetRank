# NetRank
# Caltech
# Spring 2016
# Ricky Galliani and Shubhankar Jain

import networkx as nx, pandas as pd, numpy as np, random as r
import datetime as dt, sys, operator, time
import util as u

ALPHA = 0.5

def hits(G):
    '''
    Computes rankings on the input graph using a HITS algorithm and grabbing
    the authority as a ranking mechanism.
    '''
    hubs, authorities = nx.hits_numpy(G)
    authorities = sorted(authorities.items(), key = lambda x : x[1], \
                        reverse=True)
    rank = 1
    rankings = []
    for team, aut in authorities:
        if not team[0].isdigit():
            rankings.append((rank, team))
            rank += 1
    return rankings, len(rankings)

def sub_hub(G):
    '''
    Computes rankings on the input graph using a SUB_HUB algorithm and grabbing
    the authority as a ranking mechanism. Each node's authority however is
    subtracted by surrounding node's hub score.
    '''
    hubs, authorities = nx.hits_numpy(G)
    NUM_TEAMS = nx.number_of_nodes(G)
    i = 1
    for team in G.nodes():
        # Print progress of computation to the console
        # u.print_simulation_progress(team, i, NUM_TEAMS)
        total_surrounding_authority = 0
        for neighbor in G[team].keys():
            authorities[team] -= hubs[neighbor]
        i += 1
    # Sort new authorities
    authorities = sorted(authorities.items(), key = lambda x : x[1], \
                         reverse=True)
    rank = 1
    rankings = []
    for team, aut in authorities:
        if not team[0].isdigit():
            rankings.append((rank, team))
            rank += 1
    return rankings, len(rankings)

def indirect_hits(G, level=1):
    '''
    Computes rankings on the input graph with the specified level of 
    indirection using a HITS algorithm and grabbing the authority as a ranking 
    mechanism.
    '''
    if level == 2:
        ALG = u.create_indirect_graph_2
    else:
        ALG = u.create_indirect_graph_1
    return hits(ALG(G, ALPHA))
