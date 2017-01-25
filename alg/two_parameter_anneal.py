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

ALGS        =  ["np", "pr"]

NUM_ITER = 1000
MAX_STEP = 0.1

OPTIMAL_ACC = 0.0

if __name__ == "__main__":

    INIT_BETA_NP = float(sys.argv[1]) # Get seed BETA_NP
    INIT_BETA_PR = float(sys.argv[2]) # Get seed BETA_PR
    BETA_NP = INIT_BETA_NP
    BETA_PR = INIT_BETA_PR

    OPTIMAL_BETAS = (BETA_NP, BETA_PR)

    US_PR_FILES = [] # List of our computed PageRank rankings
    US_NP_FILES = [] # List of our comptued Newman Park rankings
    RPI_FILES  = [] # List of RPI rankings
    us_dir = "../results/basketball/"
    rpi_dir = "../data/basketball/team_ranking/"
    for root, dirnames, filenames in os.walk(us_dir):
        for filename in fnmatch.filter(filenames, '*.csv'):
            if filename.startswith("log"):
                continue

            season = u.get_season_from_filename(filename)
            date = u.get_date_from_filename(filename)

            if season not in SEASON_DIRS or \
            (date.month != 3 or date.day < 14 or date.day > 19):
                continue

            if "pr" in root and filename.endswith("margin_of_vic.csv"): 
                fname = us_dir + "wpr/" + season + "/" + filename
                if fname not in US_PR_FILES:
                    US_PR_FILES.append(fname)
            elif "np" in root:
                fname = us_dir + "wnp/" + season + "/" + filename.replace(".csv", "") + \
                        "_margin_of_vic.csv"
                if fname not in US_NP_FILES:
                    US_NP_FILES.append(fname)

            if filename not in RPI_FILES:
                RPI_FILES.append(rpi_dir + season + "/" + filename)

    # Will be compared after each iteration to control where to go next in the
    # search space
    PREV_ACC = 0
    CUR_ACC  = 0
    # PREV_CORR = 0.0
    # CUR_CORR = 0.0
    # PREV_SCORE = 0
    # CURR_SCORE = 0

    NUM_RANKINGS = 0
    NUM_CONVERGE = 0
    UPPED_BETA_PR = r.choice([True, False])

    for i in range(NUM_ITER):

        step_size = MAX_STEP / (i + 1)
        num = ((1.0 * i) / (NUM_ITER)) * 100

        for c, (f_pr, f_np, f_rpi) in enumerate(zip(US_PR_FILES, \
                                                    US_NP_FILES, \
                                                    RPI_FILES)):

            # First verify everything seems right with the current comparison 
            # of files.
            b_pr = os.path.basename(f_pr).replace("_margin_of_vic", "")
            b_np = os.path.basename(f_np)
            b_rpi = os.path.basename(f_rpi)
            if b_pr != b_np or b_np != b_rpi: 
                # print("[ERROR]: inconsistency with files.")
                # print(str((b_pr, b_np, b_rpi)))
                pass

            # Get rankings as list for the PageRank, Newman Park, and RPI 
            # rankings
            r_pr = u.get_rankings_as_list(f_pr)
            r_np = u.get_rankings_as_list(f_np)
            r_lc = lc.linearly_combine([r_pr, r_np], [BETA_PR, BETA_NP])
            r_rpi = u.get_rankings_as_list(f_rpi)

            # Compute the retrodictive accuracy of the rankings formed by 
            # linear combination
            season_filename_prefix = "../data/basketball/season_log/"
            season_year = u.get_season_from_filename(f_pr)[-4:]
            season = pd.read_csv(season_filename_prefix + season_year + "_full.csv")
            acc = u.compute_weighted_retro_acc(season, -1, r_lc)

            # Compute the Spearman Correlation Coefficient of the rankings 
            # formed by the linear combination
            corr = u.compute_spearman(f_rpi, r_lc, -1)

            CUR_ACC += acc
            # CUR_CORR += corr

            if acc > 0 and corr > 0.0:
                NUM_RANKINGS += 1

            # Print out the progress of the annealing job to the console
            dec = (1.0 * c) / len(US_PR_FILES)
            progress = str(round(num + dec, 3))
            bar = "Annealing... " + progress + "%" + " " * 30 + "\r"
            sys.stdout.write(bar)
            sys.stdout.flush()

        # Compute the score for that set of betas
        # CUR_SCORE = (CUR_ACC / 100) + CUR_CORR

        # Print out a report of how the iterations went
        beta_np = "BETA_NP: " + str(round(BETA_NP, 5))
        beta_pr = ". BETA_PR: " + str(round(BETA_PR, 5)) + "."
        avg_acc = str(round(CUR_ACC / NUM_RANKINGS, 3))
        avg_acc = " \n\tAVG ACC: " + avg_acc + "%" 
        # avg_corr = ". \n\tAVG CORR: " + str(round(CUR_CORR / NUM_RANKINGS, 7))
        # avg_score = ". \n\tAVG SCORE: " + str(round(CUR_SCORE, 7)) + "."
        print(str(i + 1) + ": " + beta_np + beta_pr + avg_acc ) # + avg_corr + avg_score)

        if CUR_ACC > OPTIMAL_ACC:
            OPTIMAL_ACC = CUR_ACC
            OPTIMAL_SEEDS = BETA_NP, BETA_PR

        # Check for convergence and terminate if it did!
        if abs(PREV_ACC - CUR_ACC) < 0.0001:
            NUM_CONVERGE += 1
        else: 
            NUM_CONVERGE = 0
        if NUM_CONVERGE >= 3:
            print("Converged!")
            print("Seeds: " + str(BETA_NP, BETA_PR))
            exit(1)

        # Make sure we got initial direction correctly and fix it if we 
        # didn't
        if (i == 1) and (CUR_ACC < PREV_ACC) and (UPPED_BETA_PR):
            # We upped BETA_PR initially and we shouldn't have
            UPPED_BETA_PR = False
            BETA_PR = INIT_BETA_PR - MAX_STEP
            BETA_NP = INIT_BETA_NP + MAX_STEP
        elif (i == 1) and (CUR_ACC < PREV_ACC) and (not UPPED_BETA_PR):
            # We upped BETA_NP initially and we shouldn't have
            UPPED_BETA_PR = True
            BETA_PR = INIT_BETA_PR + MAX_STEP
            BETA_NP = INIT_BETA_NP - MAX_STEP
        else:
            # Increase BETA_PR and decrease BETA_NP if: 
            #   1) Last adjustment was increase of BETA_PR and we improved
            #   2) Last adjustment was increase of BETA_NP and we did not improve
            if (UPPED_BETA_PR and CUR_ACC > PREV_ACC) or \
               (not UPPED_BETA_PR and CUR_ACC <= PREV_ACC): 
                UPPED_BETA_PR = True
                BETA_PR += step_size
                BETA_NP -= step_size
            # In the opposite cases, we decrease BETA_PR and increase BETA_NP
            else: 
                UPPED_BETA_PR = False
                BETA_PR -= step_size
                BETA_NP += step_size

        # Make sure our parameters are still summing up to 1
        assert(abs(1 - (BETA_PR + BETA_NP)) <= .00001) 

        # Make the current accuracy the previous one for the next iteration
        PREV_ACC = CUR_ACC
        CUR_ACC = 0
        # PREV_CORR = CUR_CORR
        # CUR_CORR = 0.0
        # PREV_SCORE = CUR_SCORE
        # CUR_SCORE = 0
        NUM_RANKINGS = 0

    print("Iterations completed!")
    print("Seeds: " + str(BETA_NP, BETA_PR))



