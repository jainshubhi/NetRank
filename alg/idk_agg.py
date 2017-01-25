# NetRank
# Caltech
# Spring 2016
# Ricky Galliani and Shubhankar Jain

import util as u
# Algs
import hits as hi, pagerank as pr, newman_park as np, bfs
from math import log, sqrt, factorial
from itertools import permutations

def get_score(rank_1, rank_2):
    '''
    Returns log of difference between two rankings. In other works, this is the
    ranking distance between two ranks.
    '''
    if rank_1 == rank_2:
        return 0
    return log(abs(rank_1 - rank_2))

def generate_permutations(rankings):
    '''
    Generate all logical permutations of rankings given all of the sets of
    rankings
    '''

def idk_agg(G):
    '''
    Aggregates rankings from two or more ranking sources using something random
    Shubhi thought up of at 2:22AM. lol.
    '''
    np_ranks, rank_length = pr.indirect_pagerank(G)
    bfs_ranks, _ = hi.indirect_hits(G)
    ihi_ranks, _ = pr.indirect_weighted_pagerank(G)
    # Make sure rankings are of same length
    assert(rank_length == len(ihi_ranks) and len(ihi_ranks) == len(bfs_ranks))
    rankings = [u.get_rankings_as_dict(np_ranks), u.get_rankings_as_dict(ihi_ranks), u.get_rankings_as_dict(bfs_ranks)]
    # Define all possible rankings
    all_rankings = permutations(rankings[0].keys())
    best_rankings = {}
    # Determine score for each possible ranking compared to existing rankings
    poss = 0
    for possible_ranking in all_rankings:
        rank = 1
        for team in possible_ranking:
            for ranking in rankings:
                best_rankings.setdefault(possible_ranking, 0)
                best_rankings[possible_ranking] += get_score(rank, ranking[team])
            rank += 1
        poss += 1
        u.print_simulation_progress("", 0.01, poss)
    return min(best_rankings.items(), lambda x: x[1])
