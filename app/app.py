import os
import json
import csv

from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import secure_filename

################################# CONFIG #######################################
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import Ranking
from util import *

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
################################# ROUTES #######################################
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rankings/<ranking_id>')
def rankings_id(ranking_id):
    ranking = Ranking.query.filter_by(ranking=ranking_id + '.csv').first()
    ap = Ranking.query.filter_by(ranking=ranking_id + '-ap.csv').first()
    rpi = Ranking.query.filter_by(ranking=ranking_id + '-rpi.csv').first()
    if ranking:
        ranking_data = s3_access(ranking.ranking)
    else:
        ranking_data = []
    if ap:
        ap_data = s3_access(ap.ranking)
    else:
        ap_data = []
    if rpi:
        rpi_data = s3_access(rpi.ranking)
    else:
        rpi_data = []
    if ranking_data != []:
        return render_template('rankings.html', bball=ranking_data[1:],
                               ap=ap_data[1:], rpi=rpi_data[1:],
                               year=int(ranking_id),
                               length=len(rpi_data) - 1)
    return redirect(url_for('index'))

@app.route('/visualize')
def visualizations():
    ranking = Ranking.query.filter_by(ranking='2014.csv').first()
    tr = Ranking.query.filter_by(ranking='2014-tr.csv').first()
    if ranking:
        ranking_data = s3_access(ranking.ranking)
    else:
        ranking_data = []
    if tr:
        tr_data = s3_access(tr.ranking)
    else:
        tr_data = []
    rank_flow_data = get_rankings_as_dicts([ranking_data, tr_data])
    print json.dumps(rank_flow_data)
    return render_template('visualizations.html')

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        sport, season, email = request.values.get("sport"), request.values.get("season"), request.values.get("email")
        if file and allowed_file(file.filename):
            output = s3_upload(file)
            new_data = Ranking(sport=sport, season=season, upload=True,
                ranking=None, data=output, email=email, official=False)
            db.session.add(new_data)
            db.session.commit()
            return redirect(url_for('thanks'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run()
