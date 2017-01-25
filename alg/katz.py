# NetRank
# Caltech 
# Spring 2016
# Ricky Galliani and Shubhankar Jain

import networkx as nx, pandas as pd, numpy as np, random as r
import datetime as dt, sys, operator, time
import util as u

ALPHA  = 0.90

def katz_centrality(G):
    '''
    Computes rankings on the input graph using the Katz centrality measure.
    '''
    # First, make each edge have a weight of 1, remove multiple edges 
    # between two nodes
    simp_G = nx.DiGraph()
    for u in G.nodes():
        simp_G.add_node(u)
    for u, v, data in G.edges_iter(data = True):
        if not simp_G.has_edge(v, u):
            simp_G.add_edge(u, v, weight = 1)

    # Then compute the Katz Rankings
    katz_ranks = nx.katz_centrality_numpy(simp_G, alpha = ALPHA)
    katz_ranks = sorted(katz_ranks.items(), key = lambda x : x[1], reverse = True)
    rank = 1
    rankings = []
    for team, pr in katz_ranks:
        if not team[0].isdigit():
            rankings.append((rank, team))
            rank += 1
    return rankings