'''
CS 145 NetRank
Shubhi Jain & Ricky Galliani
Insert JSON data into Postgres Table
'''
import sys
import json

from app import db
from models import Ranking

USAGE = '''
python json_to_table.py [path_from_current_dir_to_data] [path_from_current_dir_to_ranking] [sport] [season]
e.g.
python json_to_table.py ../data/football/season_log/2004_pro.json ../data/football/team_ranking/2004_np.json football 2004
'''


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print USAGE
        exit(1)
    with open(sys.argv[1], 'r') as json_file:
        with open(sys.argv[2], 'r') as json_rank:
            json_data = json.load(json_file)
            json_ranking = json.load(json_rank)
            data = Ranking(sport=sys.argv[3], upload=False, season=sys.argv[4],
                   ranking=json_ranking, data=json_data)
            db.session.add(data)
            db.session.commit()
