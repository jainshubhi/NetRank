'''
CS 145 NetRank
Shubhi Jain
Ricky Galliani
'''

import pandas as pd
import sys


USAGE = '''
python postprocess_bball_data.py [season]
e.g.
python postprocess_bball_data.py 2011
'''
FILE      = '../data/basketball/season_log/'
url_file  = ''

def grab_features(row):
    url = url_file[url_file['pageUrl'] == row['url']]
    if len(url) > 0:
        if row['url_team'] == row['team_1']:
            a, b = 1, 0
        else:
            b, a = 1, 0
        row['margin_of_2pa'] = url.iloc[a]['margin_of_2pa'] - url.iloc[b]['margin_of_2pa']
        row['margin_of_2pp'] = url.iloc[a]['margin_of_2pp'] - url.iloc[b]['margin_of_2pp']
        row['margin_of_3pa'] = url.iloc[a]['margin_of_3pa'] - url.iloc[b]['margin_of_3pa']
        row['margin_of_3pp'] = url.iloc[a]['margin_of_3pp'] - url.iloc[b]['margin_of_3pp']
        row['margin_of_fta'] = url.iloc[a]['margin_of_fta'] - url.iloc[b]['margin_of_fta']
        row['margin_of_ftp'] = url.iloc[a]['margin_of_ftp'] - url.iloc[b]['margin_of_ftp']
        row['margin_of_off_reb'] = url.iloc[a]['margin_of_off_reb'] - url.iloc[b]['margin_of_off_reb']
        row['margin_of_def_reb'] = url.iloc[a]['margin_of_def_reb'] - url.iloc[b]['margin_of_def_reb']
        row['margin_of_stl'] = url.iloc[a]['margin_of_stl'] - url.iloc[b]['margin_of_stl']
        row['margin_of_ast'] = url.iloc[a]['margin_of_ast'] - url.iloc[b]['margin_of_ast']
        row['margin_of_blk'] = url.iloc[a]['margin_of_blk'] - url.iloc[b]['margin_of_blk']
        row['margin_of_tov'] = url.iloc[a]['margin_of_tov'] - url.iloc[b]['margin_of_tov']
        return row



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print USAGE
        exit(1)
    season = sys.argv[1]
    URL_FILE = FILE + season + '_pre_full.csv'
    DATA_FILE = FILE + season + '_url.csv'
    url_file = pd.read_csv(URL_FILE)
    data_file = pd.read_csv(DATA_FILE)
    data_file['margin_of_2pa'] = 0
    data_file['margin_of_2pp'] = 0
    data_file['margin_of_3pa'] = 0
    data_file['margin_of_3pp'] = 0
    data_file['margin_of_fta'] = 0
    data_file['margin_of_ftp'] = 0
    data_file['margin_of_off_reb'] = 0
    data_file['margin_of_def_reb'] = 0
    data_file['margin_of_stl'] = 0
    data_file['margin_of_ast'] = 0
    data_file['margin_of_blk'] = 0
    data_file['margin_of_tov'] = 0
    data_file = data_file.apply(grab_features, axis=1)
    data_file.to_csv(FILE + season + '_full.csv', index=False, sep=',')
