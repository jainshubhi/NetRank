# NetRank
# Caltech
# Spring 2016
# Ricky Galliani and Shubhankar Jain

import util as u
# Algs
import hits as hi, pagerank as pr, newman_park as np, bfs
from math import log, sqrt
from itertools import combinations

def copeland(G):
    '''
    Aggregates rankings from two or more ranking sources using Copeland's
    Pairwise Aggregation Method.
    '''
    np_ranks, rank_length = pr.indirect_pagerank(G)
    bfs_ranks, _ = hi.indirect_hits(G)
    ihi_ranks, _ = pr.indirect_weighted_pagerank(G)
    # Make sure rankings are of same length
    assert(rank_length == len(ihi_ranks) and len(ihi_ranks) == len(bfs_ranks))
    rankings = [u.get_rankings_as_dict(np_ranks), u.get_rankings_as_dict(ihi_ranks), u.get_rankings_as_dict(bfs_ranks)]
    # Aggregate
    all_pairs = combinations(rankings[0].keys(), 2)
    totals = {}
    # For all rankings, conduct pairwise aggregations
    for ranking in rankings:
        for team_1, team_2 in all_pairs:
            totals.setdefault(team_1, 0)
            totals.setdefault(team_2, 0)
            if ranking[team_1] > ranking[team_2]:
                totals[team_1] -= 1
                totals[team_2] += 1
            else:
                totals[team_1] += 1
                totals[team_2] -= 1
    # Convert totals into points
    results = sorted(
        [(count, team) for team, count in totals.items()],
        reverse=True)
    rank, rankings = 1, []
    for team in results:
        rankings.append((rank, team[1]))
        rank += 1
    return rankings, len(rankings)

def copeland_log(G):
    '''
    Aggregates rankings from two or more ranking sources using Copeland's
    Pairwise Aggregation Method with a twist of log difference
    '''
    np_ranks, rank_length = pr.indirect_pagerank(G)
    bfs_ranks, _ = hi.indirect_hits(G)
    ihi_ranks, _ = pr.indirect_weighted_pagerank(G)
    # Make sure rankings are of same length
    assert(rank_length == len(ihi_ranks) and len(ihi_ranks) == len(bfs_ranks))
    rankings = [u.get_rankings_as_dict(np_ranks), u.get_rankings_as_dict(ihi_ranks), u.get_rankings_as_dict(bfs_ranks)]
    # Aggregate
    all_pairs = combinations(rankings[0].keys(), 2)
    totals = {}
    # For all rankings, conduct pairwise aggregations
    for ranking in rankings:
        for team_1, team_2 in all_pairs:
            totals.setdefault(team_1, 0)
            totals.setdefault(team_2, 0)
            if ranking[team_1] > ranking[team_2]:
                totals[team_1] -= log(ranking[team_1] - ranking[team_2])
                totals[team_2] += log(ranking[team_1] - ranking[team_2])
            else:
                totals[team_1] += log(ranking[team_2] - ranking[team_1])
                totals[team_2] -= log(ranking[team_2] - ranking[team_1])
    # Convert totals into points
    results = sorted(
        [(count, team) for team, count in totals.items()],
        reverse=True)
    rank, rankings = 1, []
    for team in results:
        rankings.append((rank, team[1]))
        rank += 1
    return rankings, len(rankings)
