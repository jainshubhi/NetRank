# CS 145
# Shubhi Jain and Ricky Galliani

import urllib2
import pandas as pd
import sys
import requests
import datetime as dt
from bs4 import BeautifulSoup

USAGE = '''
python ap_poll_rankings.py [season] (only 2011 - 2016)
e.g.
python ap_poll_rankings.py 2011
'''
FILE = "../data/basketball/ap/"

URLS = ['http://espn.go.com/mens-college-basketball/rankings/_/year/2011/week/18/seasontype/2',
'http://espn.go.com/mens-college-basketball/rankings/_/year/2011/week/17/seasontype/2',
'http://espn.go.com/mens-college-basketball/rankings/_/year/2011/week/16/seasontype/2',
'http://espn.go.com/mens-college-basketball/rankings/_/year/2011/week/15/seasontype/2',
'http://espn.go.com/mens-college-basketball/rankings/_/year/2011/week/14/seasontype/2',
'http://espn.go.com/mens-college-basketball/rankings/_/year/2011/week/13/seasontype/2',
'http://espn.go.com/mens-college-basketball/rankings/_/year/2011/week/12/seasontype/2',
'http://espn.go.com/mens-college-basketball/rankings/_/year/2011/week/11/seasontype/2',
'http://espn.go.com/mens-college-basketball/rankings/_/year/2011/week/10/seasontype/2',
'http://espn.go.com/mens-college-basketball/rankings/_/year/2011/week/9/seasontype/2',
'http://espn.go.com/mens-college-basketball/rankings/_/year/2011/week/8/seasontype/2',
'http://espn.go.com/mens-college-basketball/rankings/_/year/2011/week/7/seasontype/2',
'http://espn.go.com/mens-college-basketball/rankings/_/year/2011/week/6/seasontype/2',
'http://espn.go.com/mens-college-basketball/rankings/_/year/2011/week/5/seasontype/2',
'http://espn.go.com/mens-college-basketball/rankings/_/year/2011/week/4/seasontype/2',
'http://espn.go.com/mens-college-basketball/rankings/_/year/2011/week/3/seasontype/2',
'http://espn.go.com/mens-college-basketball/rankings/_/year/2011/week/2/seasontype/2']

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print USAGE
        exit(1)
    for url in URLS:
        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, 'html.parser')
        
