# NetRank
# Caltech
# Spring 2016
# Ricky Galliani and Shubhankar Jain
# Makes use of the material in this blog:
#   http://vene.ro/blog/kemeny-young-optimal-rank-aggregation-in-python.html

import numpy as nmp
import hits as hi, pagerank as pr, newman_park as np, bfs
from itertools import combinations, permutations
import util as u
from lpsolve55 import *

def kendalltau_dist(rnk_a, rnk_b):
    '''
    Computes the Tau Correlation Coefficient between two rankings.
    '''
    tau       = 0
    num_items = len(rank_a)
    for i, j in combinations(range(num_items), 2):
        tau += (nmp.sign(rnk_a[i] - rnk_a[j]) == -nmp.sign(rnk_b[i] - rnk_b[j]))
    return tau

def build_graph(ranks):
    '''
    Builds a "graph" with the teams as vertices and edge weights between nodes
    i and j that are the absolute value of the number of rankings that vote
    team i higher than team j. The edge is directed from the least preferred
    team's node to the more preferred team's node.
    '''
    n_rankings, n_teams = ranks.shape
    print("n_rankings = " + str(n_rankings))
    print("n_teams = " + str(n_teams))
    edge_weights = nmp.zeros((n_teams, n_teams))
    for i, j in combinations(range(n_teams), 2):
        # For each possible ranking combination between the sets of rankings,
        # compare the rankings and assign the edge weight in the graph between
        # node i and node j such that they're non-negative.
        preference = ranks[:, i] - ranks[:, j]
        h_ij = nmp.sum(preference < 0)  # prefers i to j
        h_ji = nmp.sum(preference > 0)  # prefers j to i
        if h_ij > h_ji:
            edge_weights[i, j] = h_ij - h_ji
        elif h_ij < h_ji:
            edge_weights[j, i] = h_ji - h_ij
    return edge_weights

def convert_ranking(cols, ranking):
    '''
    Convert ranking dictionary to ky-style of rankings
    '''
    rank = [0] * len(cols)
    r = 0
    for col in range(len(cols)):
        rank[col] = ranking[cols[col]]
    return rank

def kemeny_young(G):
    '''
    Aggregates two or more sets of rankings with Kemeny-Young optimal
    rank aggregation.
    '''
    np_ranks, rank_length = pr.indirect_pagerank(G)
    bfs_ranks, _ = hi.indirect_hits(G)
    ihi_ranks, _ = pr.indirect_weighted_pagerank(G)
    # Make sure rankings are of same length
    assert(rank_length == len(ihi_ranks) and len(ihi_ranks) == len(bfs_ranks))
    # Convert set of rankings into appropriate shape/style
    rankings = [u.get_rankings_as_dict(np_ranks), u.get_rankings_as_dict(ihi_ranks), u.get_rankings_as_dict(bfs_ranks)]
    cols = rankings[0].keys()
    ranks = nmp.array([convert_ranking(cols, ranking) for ranking in rankings])
    n_voters, n_candidates = ranks.shape
    # maximize c.T * x
    edge_weights = build_graph(ranks)
    c = -1 * edge_weights.ravel()
    idx = lambda i, j: n_candidates * i + j

    # constraints for every pair
    pairwise_constraints = nmp.zeros(((n_candidates * (n_candidates - 1)) / 2,
                                     n_candidates ** 2))
    for row, (i, j) in zip(pairwise_constraints,
                           combinations(range(n_candidates), 2)):
        row[[idx(i, j), idx(j, i)]] = 1

    # and for every cycle of length 3
    triangle_constraints = nmp.zeros(((n_candidates * (n_candidates - 1) *
                                     (n_candidates - 2)),
                                     n_candidates ** 2))
    for row, (i, j, k) in zip(triangle_constraints,
                              permutations(range(n_candidates), 3)):
        row[[idx(i, j), idx(j, k), idx(k, i)]] = 1

    constraints = nmp.vstack([pairwise_constraints, triangle_constraints])
    constraint_rhs = nmp.hstack([nmp.ones(len(pairwise_constraints)),
                                nmp.ones(len(triangle_constraints))])
    constraint_signs = nmp.hstack([nmp.zeros(len(pairwise_constraints)),  # ==
                                  nmp.ones(len(triangle_constraints))])  # >=

    obj, x, duals = lp_solve(c, constraints, constraint_rhs, constraint_signs,
                             xint=range(1, 1 + n_candidates ** 2))

    x = nmp.array(x).reshape((n_candidates, n_candidates))
    aggr_rank = x.sum(axis=1)

    rankings = [cols[i] for i in nmp.argsort(aggr)]
    rankings = [(i, rankings[i]) for i in range(len(rankings))]
    return rankings, len(rankings)
