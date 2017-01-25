import datetime
import requests
import csv

from bs4 import BeautifulSoup


YEARS = range(2004, 2017)

def replace_year_in_years(year):
    return 'https://www.teamrankings.com/college-football/ranking/predictive-by-other?date=%s-01-07' % str(year)

def remove_record(string):
    return string.split('(')[0].strip()

if __name__ == '__main__':
    for year in YEARS:
        r = requests.get(replace_year_in_years(year))
        soup = BeautifulSoup(r.content, 'html.parser')
        # Grab Ranks
        ranks = soup.findAll('td', class_='rank', text=True)
        ranks = [int(rank.string) for rank in ranks]
        # Grab Team Name
        teams = soup.findAll('td', class_='nowrap')
        teams = [remove_record(team.text) for team in teams]
        # Team rankings
        team_rankings = zip(ranks, teams)
        # Write to CSV File
        with open('../data/football/rankings/'+ str(year) + '.csv', 'w') as f:
            csv_out = csv.writer(f)
            for row in team_rankings:
                csv_out.writerow(row)
