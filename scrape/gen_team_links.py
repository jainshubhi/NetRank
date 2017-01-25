# NetRank

"""
SAMPLE link: 
http://www.sports-reference.com/cbb/schools/north-carolina/2001-schedule.html
"""

TEAM_NAMES = open("teamnames.txt", "r").readlines()
YEARS = ["2009","2010","2011","2012","2013","2014","2015"]
BASE_URL = "http://www.sports-reference.com/cbb/schools/"
OUTPUT_FILE = open("team_urls.txt", "w")

if __name__ == "__main__":
    for year in YEARS:
        suffix = "/" + year + "-schedule.html"
        for team_name in TEAM_NAMES:
            team_name = str(team_name).replace("\n","").replace("\r", "")
            url = BASE_URL + team_name + suffix
            url = url.replace("\x00", "")
            print(str(url))
            OUTPUT_FILE.write(url + "\n")
    OUTPUT_FILE.close()