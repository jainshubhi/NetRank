# NetRank
# Caltech
# Spring 2016
# Ricky Galliani and Shubhankar Jain

import networkx as nx, pandas as pd, numpy as np, random as r
import datetime as dt, sys, operator, time
import util as u

ALPHA  = 0.85
DAMPING = 0.6

def weighted_pagerank(G):
    '''
    Computes rankings on the input graph using a Weighted PageRank algorithm.
    '''
    pageranks = nx.pagerank_numpy(G, alpha = ALPHA)
    pageranks = sorted(pageranks.items(), key = lambda x : x[1], reverse = True)
    rank = 1
    rankings = []
    for team, pr in pageranks:
        if not team[0].isdigit():
            rankings.append((rank, team))
            rank += 1
    return rankings, len(rankings)

def pagerank(G):
    '''
    Computes rankings on the input graph using the PageRank algorithm and edges
    of an equal weight of just 1.
    '''
    di_G = nx.DiGraph()
    for u,v,d in G.edges(data = True):
        if u not in di_G.nodes():
            di_G.add_node(u)
        if v not in di_G.nodes():
            di_G.add_node(v)
        if di_G.has_edge(u, v):
            di_G[u][v]['weight'] = di_G[u][v]['weight'] + 1
        else:
            di_G.add_edge(u, v, weight = 1)
    pageranks = nx.pagerank_numpy(di_G, alpha = ALPHA)
    pageranks = sorted(pageranks.items(), key = lambda x : x[1], reverse = True)
    rank = 1
    rankings = []
    for team, pr in pageranks:
        if not team[0].isdigit():
            rankings.append((rank, team))
            rank += 1
    return rankings, len(rankings)

def indirect_pagerank(G, level=1):
    '''
    Computes rankings on the input graph with the specified level of
    indirection using the PageRank algorithm and edges of an equal weight of
    just 1.
    '''
    if level == 2:
        ALG = u.create_indirect_graph_2
    else:
        ALG = u.create_indirect_graph_1
    return pagerank(ALG(G, DAMPING))

def indirect_weighted_pagerank(G, level=1):
    '''
    Computes rankings on the input graph with the specified level of
    indirection using a Weighted PageRank algorithm.
    '''
    if level == 2:
        ALG = u.create_indirect_graph_2
    else:
        ALG = u.create_indirect_graph_1
    return weighted_pagerank(ALG(G, DAMPING))
