# NetRank
# Caltech
# Spring 2016
# Ricky Galliani and Shubhankar Jain

import util as u
# Algs
import hits as hi, pagerank as pr, newman_park as np, bfs
from math import log, sqrt

def borda_count(G):
    '''
    Aggregates rankings from two or more ranking sources using Borda's Simple
    Election Count mechanism.
    '''
    np_ranks, rank_length = np.newman_park(G)
    bfs_ranks, _ = bfs.BFS(G)
    ihi_ranks, _ = hi.indirect_hits(G)
    # Make sure rankings are of same length
    assert(rank_length == len(ihi_ranks) and len(ihi_ranks) == len(bfs_ranks))
    rankings = [u.get_rankings_as_dict(np_ranks), u.get_rankings_as_dict(ihi_ranks), u.get_rankings_as_dict(bfs_ranks)]
    # Aggregate
    totals = {}
    # For all rankings, count points
    for ranking in rankings:
        for team, rank in ranking.items():
            totals.setdefault(team, 0)
            totals[team] += rank_length - rank
    # Convert totals into points
    results = sorted(
        [(count, team) for team, count in totals.items()],
        reverse=True)
    rank, rankings = 1, []
    for team in results:
        rankings.append((rank, team[1]))
        rank += 1
    return rankings, len(rankings)

def fractional_borda_count(G):
    '''
    Aggregates rankings from two or more ranking sources using Borda's
    Fractional Election Count mechanism.
    '''
    np_ranks, rank_length = pr.indirect_pagerank(G)
    bfs_ranks, _ = hi.indirect_hits(G)
    ihi_ranks, _ = pr.indirect_weighted_pagerank(G)
    # Make sure rankings are of same length
    assert(rank_length == len(ihi_ranks) and len(ihi_ranks) == len(bfs_ranks))
    rankings = [u.get_rankings_as_dict(np_ranks), u.get_rankings_as_dict(ihi_ranks), u.get_rankings_as_dict(bfs_ranks)]
    # Aggregate
    totals = {}
    # For all rankings, count points
    for ranking in rankings:
        for team, rank in ranking.items():
            totals.setdefault(team, 0)
            totals[team] += 1/float(rank)
    # Convert totals into points
    results = sorted(
        [(count, team) for team, count in totals.items()],
        reverse=True)
    rank, rankings = 1, []
    for team in results:
        rankings.append((rank, team[1]))
        rank += 1
    return rankings, len(rankings)

def borda_count_3(G):
    '''
    Aggregates rankings from two or more ranking sources using Borda's
    Election Count mechanism with a cube root twist.
    '''
    np_ranks, rank_length = pr.indirect_pagerank(G)
    bfs_ranks, _ = hi.indirect_hits(G)
    ihi_ranks, _ = pr.indirect_weighted_pagerank(G)
    # Make sure rankings are of same length
    assert(rank_length == len(ihi_ranks) and len(ihi_ranks) == len(bfs_ranks))
    rankings = [u.get_rankings_as_dict(np_ranks), u.get_rankings_as_dict(ihi_ranks), u.get_rankings_as_dict(bfs_ranks)]
    # Aggregate
    totals = {}
    # For all rankings, count points
    for ranking in rankings:
        for team, rank in ranking.items():
            totals.setdefault(team, 0)
            totals[team] += rank_length - (rank ** (1. / 3))
    # Convert totals into points
    results = sorted(
        [(count, team) for team, count in totals.items()],
        reverse=True)
    rank, rankings = 1, []
    for team in results:
        rankings.append((rank, team[1]))
        rank += 1
    return rankings, len(rankings)
