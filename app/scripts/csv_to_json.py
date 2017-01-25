'''
CS 145 NetRank
Shubhi Jain & Ricky Galliani
This script converts csv files to json
'''


import csv
import json
import sys
import subprocess

USAGE = '''
python csv_to_json.py [sport] [season]
e.g.
python csv_to_json.py football 2004
'''

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print USAGE
        exit(1)
    else:
        arg = 'csvjson -i 4 ../../data/' + sys.argv[1] + '/season_log/' + sys.argv[2] + '_pro.csv > ../../data/' + sys.argv[1] + '/season_log/' + sys.argv[2] + '_pro.json'
        subprocess.Popen(arg, shell=True)
