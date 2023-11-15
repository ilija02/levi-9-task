from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class PlayerRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String(3))
    free_throws_made = db.Column(db.Float)
    free_throws_attempted = db.Column(db.Float)
    two_points_made = db.Column(db.Float)
    two_points_attempted = db.Column(db.Float)
    three_points_made = db.Column(db.Float)
    three_points_attempted = db.Column(db.Float)
    rebounds = db.Column(db.Float)
    blocks = db.Column(db.Float)
    assists = db.Column(db.Float)
    steals = db.Column(db.Float)
    turnovers = db.Column(db.Float)
