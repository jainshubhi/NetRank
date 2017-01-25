# NetRank
# Caltech 
# Spring 2016
# Ricky Galliani and Shubhankar Jain

# --- MODULE IMPORTS ---

import sys, os, time, fnmatch 
import pandas as pd
import newman_park as np, pagerank as pr
import linear_combination as lc, netrank as nr
import visualize_performance as viz, datetime as dt, random as r, util as u

# ----------------------

# SEASON_DIRS = ["2000_2001", "2001_2002", "2002_2003", "2003_2004", \
#                "2004_2005", "2005_2006", "2006_2007", "2007_2008", \
#                "2008_2009", "2009_2010", "2010_2011", "2011_2012", \
#                "2012_2013", "2013_2014"]

SEASON_DIRS = ["2010_2011", "2011_2012", "2012_2013", "2013_2014"]

FEATURES    = ["margin_of_vic", "margin_of_2pa", "margin_of_2pp", \
               "margin_of_3pa", "margin_of_fta", "margin_of_drb", \
               "margin_of_ast", "margin_of_stl"]

SEEDS = [0.8087098929852137, 0.01887112106694777, 0.005082496446958503, \
         0.0007623744670437753, 0.01140738091428464, 0.04049055502743607, \
         0.09270850000470601, 0.014409818630173087, 0.00755786045723644]

OPTIMAL_SEEDS = SEEDS
OPTIMAL_ACC = 0.0

NUM_ITER = 10000
MAX_STEP = 0.1

# SEEDS = [0.70, # NP
#          0.06, # Margin of victory
#          0.03, # Margin of 2PA
#          0.03, # Margin of 2P%
#          0.03, # Margin of 3PA
#          0.03, # Margin of 3P%
#          0.03, # Margin of FTA
#          0.03, # Margin of FT%
#          0.03, # Margin of ORB
#          0.03] # Margin of DRB
#          0.01, # Margin of Ast
#          0.01, # Margin of Stl
#          0.01, # Margin of Blk
#          0.01, # Margin of TOV
#          ]

if __name__ == "__main__":

    # Set the intial beta values according to the SEEDS list
    INIT_BETA_NP, \
    INIT_BETA_MOV,   \
    INIT_BETA_MO2PA, \
    INIT_BETA_MO2PP, \
    INIT_BETA_MO3PA, \
    INIT_BETA_MOFTA, \
    INIT_BETA_MODRB, \
    INIT_BETA_MOAST, \
    INIT_BETA_MOSTL = SEEDS 

    # INIT_BETA_NP, \
    # INIT_BETA_MOV,   \
    # INIT_BETA_MO2PA, \
    # INIT_BETA_MO2PP, \
    # INIT_BETA_MO3PA, \
    # INIT_BETA_MO3PP, \
    # INIT_BETA_MOFTA, \
    # INIT_BETA_MOFTP, \
    # INIT_BETA_MOORB, \
    # INIT_BETA_MODRB, \
    # INIT_BETA_MOAST, \
    # INIT_BETA_MOSTL, \
    # INIT_BETA_MOBLK, \
    # INIT_BETA_MOTOV = SEEDS

    # Set the current beta values according to the SEEDS list
    CUR_BETAS = SEEDS

    # Store a dictionary storing lists of all the files for each feature 
    # ranking
    US_FILES = {"np"  : [], \
                "vic" : [], \
                "2pa" : [], \
                "2pp" : [], \
                "3pa" : [], \
                # "3pp" : [], \
                "fta" : [], \
                # "ftp" : [], \
                # "orb" : [], \
                "drb" : [], \
                "ast" : [], \
                "stl" : [] } # , \
                # "blk" : [], \
                # "tov" : []}
    RPI_FILES = [] # List of RPI rankings
    
    us_dir = "../results/basketball/"
    rpi_dir = "../data/basketball/team_ranking/"

    # Organize all of our ranking files...
    for root, dirnames, filenames in os.walk(us_dir):
        for filename in fnmatch.filter(filenames, '*.csv'):
            if filename.startswith("log"):
                continue

            # Get the season and date of the rankings for the current rankings
            # file
            season = u.get_season_from_filename(filename)
            date = u.get_date_from_filename(filename)
            if season not in SEASON_DIRS or \
                (date.month != 3 or date.day < 14 or date.day > 19):
                continue
            date_str = date.strftime('%m/%d/%Y').replace("/","_")

            # Get the filename of the NP margin of victory rankings file
            if "np" in root:
                f_name = us_dir + "np/" + season + "/" + date_str + ".csv"
                US_FILES["np"].append(f_name)

            # Get the filename for the rankings file we're currently traversing 
            # and add it to the appropriate list
            feat = filename[-7:][:3] # Extract feature from name
            if "margin_of_" + feat not in FEATURES:
                continue
            elif feat in filename:
                f_name = us_dir + "pr/" + season + "/" + date_str + \
                         "_margin_of_" + feat + ".csv"
                US_FILES[feat].append(f_name)

            # Add the official RPI file to the list of RPI files if it hasn't
            # already been added
            rpi_f_name = rpi_dir + season + "/" + date_str + ".csv"
            if rpi_f_name not in RPI_FILES:
                RPI_FILES.append(rpi_f_name)

    # Will be compared after each iteration to control where to go next in the
    # search space
    PREV_ACC  = 0
    CUR_ACC   = 0
    # PREV_CORR = 0.0
    # CUR_CORR  = 0.0
    # PREV_SCORE = 0.0
    # CUR_SCORE = 0.0
    NUM_RANKINGS = 0
    NUM_CONVERGE = 0
    CUR_DIR = [1,0,0,0,0,0,0,0,0] # ,0,0,0,0,0,0]

    for i in range(NUM_ITER):

        up_size   = MAX_STEP / (i + 1)
        down_size = up_size / 8.0 # Split among the other 12 parameters

        for c, (f_sample, f_rpi) in enumerate(zip(US_FILES["vic"], RPI_FILES)):

            # Get rankings as list for each feature network and pass them 
            # as a list of lists to the linearly_combine() method
            rankings = []
            rankings.append(u.get_rankings_as_list(US_FILES["np"][c]))
            rankings.append(u.get_rankings_as_list(US_FILES["vic"][c]))
            rankings.append(u.get_rankings_as_list(US_FILES["2pa"][c]))
            rankings.append(u.get_rankings_as_list(US_FILES["2pp"][c]))
            rankings.append(u.get_rankings_as_list(US_FILES["3pa"][c]))
            # rankings.append(u.get_rankings_as_list(US_FILES["3pp"][c]))
            rankings.append(u.get_rankings_as_list(US_FILES["fta"][c]))
            # rankings.append(u.get_rankings_as_list(US_FILES["ftp"][c]))
            # rankings.append(u.get_rankings_as_list(US_FILES["orb"][c]))
            rankings.append(u.get_rankings_as_list(US_FILES["drb"][c]))
            rankings.append(u.get_rankings_as_list(US_FILES["ast"][c]))
            rankings.append(u.get_rankings_as_list(US_FILES["stl"][c]))
            # rankings.append(u.get_rankings_as_list(US_FILES["blk"][c]))
            # rankings.append(u.get_rankings_as_list(US_FILES["tov"][c]))
            r_lc = lc.linearly_combine(rankings, CUR_BETAS)

            # Compute the retrodictive accuracy of the rankings formed by 
            # linear combination
            season_filename_prefix = "../data/basketball/season_log/"
            season_year = u.get_season_from_filename(f_sample)[-4:]
            season = pd.read_csv(season_filename_prefix + season_year + "_full.csv")
            acc = u.compute_weighted_retro_acc(season, -1, r_lc)

            # Compute the Spearman Correlation Coefficient of the rankings 
            # formed by the linear combination
            # corr = u.compute_spearman(f_rpi, r_lc, -1)

            CUR_ACC += acc
            # CUR_CORR += corr

            if acc > 0: #  and corr > 0.0:
                NUM_RANKINGS += 1

        # Compute the score for that set of betas
        # CUR_SCORE = (CUR_ACC / 100) + CUR_CORR

        # Print out a report of how the iterations went
        if NUM_RANKINGS == 0:
            continue
        betas = str([round(x, 5) for x in CUR_BETAS])
        avg_acc = str(round(CUR_ACC / NUM_RANKINGS, 7))
        avg_acc = " \n\tAVG ACC: " + avg_acc + "%"
        # avg_corr = ". \n\tAVG CORR: " + str(round(CUR_CORR / NUM_RANKINGS, 7))
        # avg_score = ". \n\tAVG SCORE: " + str(round(CUR_SCORE, 7)) + "."
        print(str(i + 1) + ": " + betas + avg_acc) # + avg_corr + avg_score)

        # We didn't improve with the betas, so pick a random new set of 
        # betas from a different direction
        # if CUR_SCORE < PREV_SCORE:
        #     CUR_DIR = [0] * 14
        #     CUR_DIR[r.randint(0,13)] = 1
        if CUR_ACC < PREV_ACC:
            CUR_DIR = [0] * 9
            CUR_DIR[r.randint(0,8)] = 1

        for i, (beta, dir) in enumerate(zip(CUR_BETAS, CUR_DIR)):
            if dir == 1: # This is the direction that led us to success
                CUR_BETAS[i] += up_size
            else: 
                CUR_BETAS[i] -= down_size

        # Make sure our parameters are still summing up to 1
        assert(abs(1 - (sum(CUR_BETAS)) <= .1)) 

        if CUR_ACC > OPTIMAL_ACC:
            OPTIMAL_ACC = CUR_ACC
            OPTIMAL_SEEDS = SEEDS

        # Check for convergence and terminate if it did!
        if abs(PREV_ACC - CUR_ACC) < 0.00000001:
            NUM_CONVERGE += 1
        else: 
            NUM_CONVERGE = 0
        if NUM_CONVERGE >= 3:
            print("Converged!")
            print("Optimal Seeds: " + str(OPTIMAL_SEEDS))
            exit(1)

        # Reset values for next iteration
        PREV_ACC = CUR_ACC
        # PREV_CORR = CUR_CORR
        # PREV_SCORE = CUR_SCORE
        CUR_ACC = 0
        # CUR_CORR = 0
        # CUR_SCORE = 0
        NUM_RANKINGS = 0

    print("Iterations commpleted: " + str(OPTIMAL_SEEDS))



