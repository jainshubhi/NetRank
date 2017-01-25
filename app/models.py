from app import db
from sqlalchemy.dialects.postgresql import JSON


class Ranking(db.Model):
    __tablename__ = 'rankings'

    id = db.Column(db.Integer, primary_key=True)
    sport = db.Column(db.String())
    upload = db.Column(db.Boolean())
    season = db.Column(db.Integer)
    ranking = db.Column(db.String(), nullable=True)
    official = db.Column(db.Boolean())
    data = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(), nullable=True)

    def __init__(self, sport, upload, season, ranking, data, email, official):
        self.sport = sport
        self.upload = upload
        self.season = season
        self.ranking = ranking
        self.data = data
        self.email = email
        self.official = official

    def __repr__(self):
        return '<sport: {}, season: {}>'.format(self.sport, self.season)
