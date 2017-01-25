# CS 145
# NetRank
# Shubhi Jain & Ricky Galliani


import urllib2
import pandas as pd
from bs4 import BeautifulSoup

BASE_URL = 'http://www.sports-reference.com'
YEARS = range(2015, 2016)

def fuck_me(mine, theirs):
    '''
    Miami is different in our data because Pandas keeps on screwing up with
    Miami (FL) and Miami (OH) so I changed it to Miami-OH.
    '''
    if mine == "Miami-OH" and theirs == "Miami (OH)":
        return True
    return False

def add_data(row):
    '''
    Add Margin Data for other features to Football Season Log Data
    '''
    page = urllib2.urlopen(BASE_URL + row['url']).read()
    soup = BeautifulSoup(page, 'html.parser')
    item_counter, col, t1, t2 = 0, '', 0, 0
    for item in soup.find_all(class_='align_center bold_text'):
        if item_counter % 3 is 0:
            col = item.br.string
        elif item_counter % 3 is 1:
            t1 = int(item.br.string)
        else:
            t2 = int(item.br.string)
            if col:
                theirs = soup.find_all('h1')[0].a.string
                if theirs == row['team_1'] or fuck_me(row['team_1'], theirs):
                    res = t1 - t2
                else:
                    res = t2 - t1
                row['margin_of_' + '_'.join(col.lower().split())] = res
        item_counter += 1
    if col:
        print 'Finished ' + row['url'] + '.'
    else:
        print 'Finished ' + row['url'] + ' but no data.'
    return row


if __name__ == '__main__':
    for year in YEARS:
        data = pd.read_csv('../data/football/season_log/' + str(year) + '.csv')
        # Add columns
        data['margin_of_total_yards'] = 0
        data['margin_of_passing'] = 0
        data['margin_of_rushing'] = 0
        data['margin_of_first_downs'] = 0
        data['margin_of_penalties'] = 0
        data['margin_of_turnovers'] = 0
        data = data.apply(add_data, axis=1)
        data.to_csv('../data/football/season_log/' + str(year) + '_pro.csv', sep=',', index=False)
