# CS 145
# NetRank
# Shubhi Jain & Ricky Galliani


import urllib2
from bs4 import BeautifulSoup

URL = 'http://www.sports-reference.com/cfb/years/' # 2015-schedule.html
YEARS = range(2015, 2016)

if __name__ == '__main__':
    for year in YEARS:
        page = urllib2.urlopen(URL + str(year) + '-schedule.html').read()
        soup = BeautifulSoup(page, 'html.parser')
        for link in soup.find_all('a'):
            if 'boxscores' in link.get('href') and str(year) in link.get('href'):
                print link.get('href')
