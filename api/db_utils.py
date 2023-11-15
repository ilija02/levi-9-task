# db_utils.py
import os
import pandas as pd

from flask_sqlalchemy import SQLAlchemy

from model import PlayerRecord

db = SQLAlchemy()

csv_filename = "data.csv"
basedir = os.path.dirname(os.path.abspath(__file__))
csv_file = "data.csv"
csv_absolute_path = os.path.join(basedir, csv_filename)


def init_db(app, db):
    with app.app_context():
        db.create_all()
        load_csv_data(db)


def load_csv_data(db):
    basketball_data = pd.read_csv(csv_absolute_path)

    for _, row in basketball_data.iterrows():
        player_record = PlayerRecord(
            player_name=row["PLAYER"],
            position=row["POSITION"],
            free_throws_made=row["FTM"],
            free_throws_attempted=row["FTA"],
            two_points_made=row["2PM"],
            two_points_attempted=row["2PA"],
            three_points_made=row["3PM"],
            three_points_attempted=row["3PA"],
            rebounds=row["REB"],
            blocks=row["BLK"],
            assists=row["AST"],
            steals=row["STL"],
            turnovers=row["TOV"],
        )
        db.session.add(player_record)

    db.session.commit()
