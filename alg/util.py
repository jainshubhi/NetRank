# NetRank
# Caltech
# Spring 2016
# Ricky Galliani and Shubhankar Jain

import pandas as pd, networkx as nx, datetime as dt, random as r, os
import numpy as np, sys
from scipy.stats import spearmanr

def get_date_from_filename(f):
    '''
    Returns 10/16/2000 from '../data/basketball/team_ranking/10_16_2000.csv'
    '''
    for i, char in enumerate(f):
        if char.isdigit():
            break
    f        = f[i : i + 10] # Only get the date part of the filename
    mon      = f[5:7]
    day      = f[8:10]
    year     = f[:4]
    date_str = mon + "/" + day + "/" + year
    return dt.datetime.strptime(date_str, "%m/%d/%Y")

def get_season_from_filename(f):
    '''
    Returns 2000_2001 from '../data/basketball/team_ranking/10_16_2000.csv'
    '''
    for i, char in enumerate(f):
        if char.isdigit():
            if char == "2":
                return f[i : i + 9]
            else:
                break
    f    = f[i : i + 10] # Only get the date part of the filename
    mon  = f[:2]
    year = f[6:10]
    if int(mon) >= 5:
        prev_year = year
        year = str(int(year) + 1)
    else:
        prev_year = str(int(year) - 1)
    return prev_year + "_" + year

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + dt.timedelta(n)

def is_ranking_day(date):
    '''
    Returns true if the input date is a Monday during basketball season.
    '''
    return ((date.month == 10 and date.day >= 15) or \
            (date.month >= 11 or date.month <= 3) or \
            (date.month == 4 and date.day <= 10)) and \
            (date.isoweekday() == 1)

def get_ranking_dates(df):
    '''
    Determines the time points for which PageRank iterates in a basketball
    season which are every Monday during the course of the season.
    '''
    ranking_dates = []
    first_date = dt.datetime.strptime(df.iloc[0]['date'], "%m/%d/%Y")
    end_date   = dt.datetime.strptime(df.iloc[len(df) - 1]['date'], \
                                        "%m/%d/%Y")
    while first_date.isoweekday() != 1:
        first_date += dt.timedelta(days = 1)
    for date in daterange(first_date, end_date):
        if is_ranking_day(date):
            ranking_dates.append(date)
    ranking_dates.append(end_date)
    return ranking_dates

def build_season_graph(season, date, feature):
    '''
    Builds a season graph from an input season DataFrame and weights the
    edges with the margins of the specified feature.
    '''
    # Multi-graph because two teams can matchup more than once
    G = nx.MultiDiGraph()
    for i, game in season.iterrows():
        game_date = dt.datetime.strptime(game['date'], "%m/%d/%Y")
        if date != -1 and game_date > date:
            # Only building the graph up to the desired.
            break
        team_1 = game['team_1']
        team_2 = game['team_2']
        feature_value = game[feature]
        add_matchup(G, team_1, team_2, feature_value)
    return G, len(G.nodes())

def build_graph_for_range(season, prev_date, date):
    '''
    Builds a graph for the games that occurred within the input season
    and within the provided range of dates.
    '''
    G = nx.MultiDiGraph()
    for i, game in season.iterrows():
        game_date = dt.datetime.strptime(game['date'], "%m/%d/%Y")
        if game_date > date:
            break
        if date != -1 and game_date > prev_date:
            team_1            = game['team_1']
            team_2            = game['team_2']
            margin_of_victory = game['margin_of_victory']
            add_matchup(G, team_1, team_2, margin_of_victory)
    return G

def add_matchup(G, team_1, team_2, margin_of_victory):
    '''
    Adds the matchup between team_1 and team_2 to the graph G with an
    edge pointing from the losing team to the winning team and the
    weight of the edge being margin_of_victory.
    '''
    if team_1 not in G.nodes():
        G.add_node(team_1)
    if team_2 not in G.nodes():
        G.add_node(team_2)
    if margin_of_victory > 0:
        # Team 1 beat Team 2 so make edge from Team 2 to Team 1
        G.add_edge(team_2, team_1, weight = abs(margin_of_victory))
    else:
        # Team 2 beat Team 1 so make edge from Team 1 to Team 2
        G.add_edge(team_1, team_2, weight = abs(margin_of_victory))

def compute_retro_acc(season, date, rankings):
    '''
    Computes the fraction of games in the season that were won by the
    higher ranked team.
    '''
    r_dict = dict((v,k) for k,v in rankings)
    total_games = 0
    correct_games = 0
    for i, row in season.iterrows():
        game_date = dt.datetime.strptime(row['date'], "%m/%d/%Y")
        if (date != -1 and game_date > date):
            break

        team_1 = row['team_1']
        team_2 = row['team_2']

        # Too early in the season both teams haven't played so we don't
        # consider them yet
        if team_1 not in r_dict or team_2 not in r_dict:
            continue

        margin_of_victory = row['margin_of_victory']
        total_games += 1
        c1 = r_dict[team_1] < r_dict[team_2] and margin_of_victory > 0
        c2 = r_dict[team_2] < r_dict[team_1] and margin_of_victory < 0
        if c1 or c2:
           correct_games += 1

    if correct_games != 0:
        return round((1.0 * correct_games) / total_games, 5) * 100
    else:
        return 0.0

def compute_weighted_retro_acc(season, date, rankings):
    '''
    Computes the weighted retrodictive accuracy of a set of rankings on a
    given season.
    '''
    r_dict = dict((v,k) for k,v in rankings)
    points_earned = 0.0
    points_possible = 0.0
    for i, row in season.iterrows():
        game_date   = dt.datetime.strptime(row['date'], "%m/%d/%Y")
        if (date != -1 and game_date > date):
            break

        team_1 = row['team_1']
        team_2 = row['team_2']

        # Too early in the season both teams haven't played so we don't
        # consider them yet
        if team_1 not in r_dict or team_2 not in r_dict:
            continue

        team_1_rank = r_dict[team_1]
        team_2_rank = r_dict[team_2]

        # If the team's haven't even been separated yet in the rankings,
        # just skip to the next game, too early in the season
        if team_1_rank - team_2_rank == 0:
            continue
        log_rank_disparity = np.log(abs(team_1_rank - team_2_rank))
        # Add the points possible for this matchup to the sum of possible
        # points
        points_possible += log_rank_disparity

        margin_of_victory = row['margin_of_victory']
        c1 = team_1_rank < team_2_rank and margin_of_victory > 0
        c2 = team_2_rank < team_1_rank and margin_of_victory < 0
        # If our rankings indicate the correct winning team for this game
        if c1 or c2:
            points_earned += log_rank_disparity

    if points_earned == 0.0:
        return 0.0
    else:
        # Accuracy is ratio of earned points
        return round((points_earned / points_possible) * 100, 3)

def compute_spearman(off_ranking_fname, rankings, top_x):
    '''
    Computes the Spearman rank correlation coefficient between our
    computed rankings and official rankings.
    '''
    # Populate a dictionary storing the rank for each team
    off_rankings = {}
    off_ranking_file = pd.read_csv(off_ranking_fname)
    for ind, row in off_ranking_file.iterrows():
        rank = row['rank']
        team = row['team']
        off_rankings[team] = rank

    D_SUM = 0

    if top_x > 0: # Rank only the top x teams, specified as argument
        N = top_x
    else: #
        N = len(off_rankings)

    '''
    if len(off_rankings) != len(our_rankings):
        print("Official Rankings: " + str(len(off_rankings)) + " entries")
        print("Our Rankings:      " + str(len(our_rankings)) + " entries")
        exit(1)
    '''

    for our_rank, our_team in rankings:
        if our_rank > N:
            break

        if our_team[3].isdigit():
            continue

        if our_team in off_rankings:
            D_SUM += (our_rank - off_rankings[our_team]) ** 2

    if D_SUM == 0 or len(rankings) < 300:
        return 0.0

    return round(1 - (6.0 * D_SUM) / (N * (N ** 2 - 1)), 3)

def prune_rankings(rankings):
    '''
    Removes all exhibition teams from the rankings. That is, all teams with
    team names that are just floats.
    '''
    ret = []
    rank = 1
    for rank, team in rankings:
        if not team[0].isdigit():
            ret.append((rank, team))
            rank += 1
    return ret

def prune_pr_list(pr):
    '''
    Removes all exhibition teams from the current pr list. That is, all teams
    with team names that are just floats.
    '''
    ret = []
    for team, pr in pr:
        if not team[0].isdigit():
            ret.append((team, pr))
    return ret

def write_rankings(date, rankings, output_file):
    '''
    Writes the computed rankings to an output file.
    '''
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))
    output_file = open(output_file, "w")
    output_file.write("rank,team\n")
    for rank, team in rankings:
        row = str(rank) + "," + team + "\n"
        output_file.write(row)
    output_file.close()

def get_rankings_as_list(filename):
    '''
    Reads in the rankings written to the given file and returns the rankings
    as a list of (rank, team) entries.
    '''
    rankings = pd.read_csv(filename)
    rankings_list = []
    for ind, row in rankings.iterrows():
        rank = row['rank']
        team = row['team']
        rankings_list.append((rank, team))
    return rankings_list

def get_rankings_as_dict(rankings):
    '''
    Takes in a list of tuples of rankings and returns them as a dictionary
    with the key as the team name and the value as the rank.
    '''
    rankings_dict = {}
    for rank in rankings:
        rankings_dict[rank[1]] = rank[0]
    return rankings_dict

def get_weight(G, team_1, team_2):
    '''
    Returns the average weight between two edges in a MultiDiGraph.
    '''
    weights = list(G[team_1][team_2].items())
    return float(sum([val[1]['weight'] for val in weights])) / len(weights)

def create_indirect_graph_1(G, ALPHA):
    '''
    Takes in an input graph and returns another graph with one level of
    indirection added with the specified alpha damping constant.
    '''
    H = G.copy()
    for node in G.nodes():
        for neighbor in G[node].keys():
            for n_node in G[neighbor].keys():
                if node != n_node:
                    H.add_edge(node, n_node,
                               weight=(get_weight(G, node, neighbor) +
                               get_weight(G, neighbor, n_node)) * ALPHA)
    return H

def create_indirect_graph_2(G, ALPHA):
    '''
    Takes in an input graph and returns another graph with two levels of
    indirection added with the specified alpha damping constant.
    '''
    H = G.copy()
    for node in G.nodes():
        for neighbor in G[node].keys():
            for n_node in G[neighbor].keys():
                if node != n_node:
                    H.add_edge(node, n_node,
                               weight=(get_weight(G, node, neighbor) +
                               get_weight(G, neighbor, n_node)) * ALPHA)
                for n_n_node in G[n_node].keys():
                    if node != n_n_node:
                        H.add_edge(node, n_node,
                                   weight=(get_weight(G, node, neighbor) +
                                   get_weight(G, neighbor, n_node) +
                                   get_weight(G, n_node, n_n_node)) *
                                   (ALPHA ** 2))
    return H

def print_simulation_progress(team, i, NUM_TEAMS):
    '''
    Writes the computation progress to the console.
    '''
    progress = str(round(((1.0 * i) / NUM_TEAMS) * 100, 1))
    bar = progress + "%. " + team + ".                      \r"
    sys.stdout.write(bar)
    sys.stdout.flush()

def print_simulation_results(date_str, acc, weighted_acc, spearman, comp, \
                             n_nodes, ranking_size, output_file):
    '''
    Write the results of a running a season simulation.
    '''
    bar1 = date_str.replace("_","/") + ":" + "                       \n"
    bar2 = "\tRetrodictive Accuracy         : " + str(acc) + "%\n"
    bar3 = "\tWeighted Retrodictive Accuracy: " + str(weighted_acc) + "%\n"
    bar4 = "\tSpearman Coefficient          : " + str(spearman) + "\n"
    bar5 = "\tComputation Time              : " + str(comp) + " secs\n"
    bar6 = "\tNumber of Teams Scanned       : " + str(n_nodes) + "\n"
    bar7 = "\tNumber of Teams Ranked        : " + str(ranking_size) + "\n"
    bar8 = "\tOutput File                   : " + output_file + "\n"
    print(bar1 + bar2 + bar3 + bar4 + bar5 + bar6 + bar7 + bar8 + "\n")
