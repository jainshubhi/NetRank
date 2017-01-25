# NetRank
# Caltech
# Spring 2016
# Ricky Galliani and Shubhankar Jain

import networkx as nx, pandas as pd, numpy as np, random as r
import datetime as dt, sys, operator, time
import util as u

DAMPING = 0.6

def eigenvector(G):
    '''
    Computes rankings on the input graph using eigenvector centrality
    as a ranking mechanism.
    '''
    eigenvectors = nx.eigenvector_centrality_numpy(G)
    eigenvectors = sorted(eigenvectors.items(), key = lambda x : x[1], \
                          reverse=True)
    rank = 1
    rankings = []
    for team, aut in eigenvectors:
        if not team[0].isdigit():
            rankings.append((rank, team))
            rank += 1
    return rankings, len(rankings)

def indirect_eigenvector(G, level=1):
    '''
    Computes rankings on the input graph with the specified level of 
    indirection using eigenvector centrality as a ranking mechanism.
    '''
    if level == 2:
        ALG = u.create_indirect_graph_2
    else:
        ALG = u.create_indirect_graph_1
    return eigenvector(ALG(G, DAMPING))
