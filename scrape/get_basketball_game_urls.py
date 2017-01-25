# CS 145
# NetRank
# Shubhi Jain & Ricky Galliani


import urllib2
import pandas as pd
import sys
import requests
import datetime as dt
from bs4 import BeautifulSoup


USAGE = '''
python get_basketball_features.py [season] (only 2011 - 2016)
e.g.
python get_basketball_features.py 2011
'''

FILE      = '../data/basketball/season_log/'
URL       = 'http://www.sports-reference.com/cbb/boxscores/'
ERROR     = 'http://www.sports-reference.com/cbb/errors/404.html?redir'

def string_date_to_datetime(date):
    '''
    Convert a string of date to a datetime date
    '''
    date = date.split('/')
    return dt.date(int(date[2]), int(date[0]), int(date[1]))

def is_team_in_link(team_1, team_2, link):
    if team_1 in link or team_2 in link:
        return True
    return False

def add_data(row):
    now = string_date_to_datetime(row['date'])
    # Grabbing new page
    try:
        r = requests.get(URL + str(now) + '-' + row['team_1'] + '.html', allow_redirects=True).url
        if r != ERROR:
            row['url'] = URL + str(now) + '-' + row['team_1'] + '.html'
            row['url_team'] = row['team_1']
        else:
            row['url'] = URL + str(now) + '-' + row['team_2'] + '.html'
            row['url_team'] = row['team_2']
        print row['url']
        return row
    except:
        print row['url']
        return row

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print USAGE
        exit(1)
    FILE += sys.argv[1] + '.csv'
    data = pd.read_csv(FILE)
    data['url'] = ''
    data['url_team'] = ''
    data = data.apply(add_data, axis=1)
    data.to_csv('../data/basketball/season_log/' + sys.argv[1] + '_url.csv', sep=',', index=False)
