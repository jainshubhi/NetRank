
import sys, pandas as pd

if __name__ == "__main__":

    invalid_file = sys.argv[1]
    output_file = open(invalid_file.replace(".csv", ".out"), "w")
    output_file.write("rank,team\n")
    cur_rank = 1
    for ind, row in pd.read_csv(invalid_file).iterrows():
        team = row['team']
        if team != "#VALUE!":
            output_file.write(str(cur_rank) + "," + team + "\n")
            cur_rank += 1