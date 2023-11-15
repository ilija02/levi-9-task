import os
import pandas as pd

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from numpy import mean

from model import db, PlayerRecord
from db_utils import init_db

app = Flask(__name__)
# Configure the in memory SQLite DB
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.sort_keys = False

db.init_app(app)
# Load the csv data into database
init_db(app, db)


# Endpoint for retrieving player stats
@app.route("/stats/player/<playerFullName>/", methods=["GET"])
def get_player_stats(playerFullName):
    if not playerFullName:
        return jsonify({"error": "Player name is required"}), 400
    player_stats = calculate_player_stats(playerFullName)
    if player_stats.get("error"):
        return jsonify(player_stats), 404

    return jsonify(player_stats)


def get_mean_values(player_records):
    player_records_mean = {}
    player_records_mean["FTA"] = mean([r.free_throws_attempted for r in player_records])
    player_records_mean["FTM"] = mean([r.free_throws_made for r in player_records])
    player_records_mean["2PA"] = mean([r.two_points_attempted for r in player_records])
    player_records_mean["2PM"] = mean([r.two_points_made for r in player_records])
    player_records_mean["3PA"] = mean(
        [r.three_points_attempted for r in player_records]
    )
    player_records_mean["3PM"] = mean([r.three_points_made for r in player_records])
    player_records_mean["REB"] = mean([r.rebounds for r in player_records])
    player_records_mean["BLK"] = mean([r.blocks for r in player_records])
    player_records_mean["AST"] = mean([r.assists for r in player_records])
    player_records_mean["STL"] = mean([r.steals for r in player_records])
    player_records_mean["TOV"] = mean([r.turnovers for r in player_records])

    return player_records_mean


# Calculate stats for a given player
def calculate_player_stats(player_name):
    player_records = (
        db.session.query(PlayerRecord).filter_by(player_name=player_name).all()
    )
    if not player_records:
        return {"error": "Player not found"}

    player_records_mean = get_mean_values(player_records)

    response = {}
    response["playerName"] = player_name
    response["gamesPlayed"] = len(player_records)
    response["traditional"] = calculate_traditional_stats(player_records_mean)
    response["advanced"] = calculate_advanced_stats(player_records_mean)
    return response


def calculate_traditional_stats(player_records_mean):
    traditional_stats = {}
    traditional_stats["freeThrows"] = {}
    traditional_stats["twoPoints"] = {}
    traditional_stats["threePoints"] = {}

    traditional_stats["freeThrows"]["attempts"] = player_records_mean["FTA"].round(1)
    traditional_stats["freeThrows"]["made"] = player_records_mean["FTM"].round(1)

    traditional_stats["freeThrows"]["shootingPercentage"] = (
        player_records_mean["FTM"] / player_records_mean["FTA"] * 100
    ).round(1) if player_records_mean["FTA"] else 0

    traditional_stats["twoPoints"]["attempts"] = player_records_mean["2PA"].round(1)
    traditional_stats["twoPoints"]["made"] = player_records_mean["2PM"].round(1)
    traditional_stats["twoPoints"]["shootingPercentage"] = (
        player_records_mean["2PM"] / player_records_mean["2PA"] * 100
    ).round(1) if player_records_mean["2PA"] else 0

    traditional_stats["threePoints"]["attempts"] = player_records_mean["3PA"].round(1)
    traditional_stats["threePoints"]["made"] = player_records_mean["3PM"].round(1)
    traditional_stats["threePoints"]["shootingPercentage"] = (
        player_records_mean["3PM"] / player_records_mean["3PA"] * 100
    ).round(1) if player_records_mean["3PA"] else 0

    traditional_stats["points"] = (
        player_records_mean["FTM"]
        + 2 * player_records_mean["2PM"]
        + 3 * player_records_mean["3PM"]
    ).round(1)
    traditional_stats["rebounds"] = player_records_mean["REB"].round(1)
    traditional_stats["blocks"] = player_records_mean["BLK"].round(1)
    traditional_stats["assists"] = player_records_mean["AST"].round(1)
    traditional_stats["steals"] = player_records_mean["STL"].round(1)
    traditional_stats["turnovers"] = player_records_mean["TOV"].round(1)

    return traditional_stats


def calculate_advanced_stats(player_records_mean):
    advanced_stats = {}
    TPS = (
        player_records_mean["FTM"]
        + 2 * player_records_mean["2PM"]
        + 3 * player_records_mean["3PM"]
    )
    advanced_stats["valorization"] = (
        (
            player_records_mean["FTM"]
            + 2 * player_records_mean["2PM"]
            + 3 * player_records_mean["3PM"]
            + player_records_mean["REB"]
            + player_records_mean["BLK"]
            + player_records_mean["AST"]
            + player_records_mean["STL"]
        )
        - (
            player_records_mean["FTA"]
            - player_records_mean["FTM"]
            + player_records_mean["2PA"]
            - player_records_mean["2PM"]
            + player_records_mean["3PA"]
            - player_records_mean["3PM"]
            + player_records_mean["TOV"]
        )
    ).round(1)

    advanced_stats["effectiveFieldGoalPercentage"] = (
        (player_records_mean["2PM"] + 1.5 * player_records_mean["3PM"])
        / (player_records_mean["2PA"] + player_records_mean["3PA"])
        * 100
    ).round(1) if (player_records_mean["2PA"] + player_records_mean["3PA"]) else 0

    denominator = (
            player_records_mean["2PA"]
            + player_records_mean["3PA"]
            + 0.475 * player_records_mean["FTA"]
            )

    advanced_stats["trueShootingPercentage"] = (
        TPS
        / (
            2*denominator
        )
        * 100
    ).round(1) if denominator else 0

    denominator = ( 
            player_records_mean["2PA"]
            + player_records_mean["3PA"]
            + 0.475 * player_records_mean["FTA"]
            + player_records_mean["AST"]
            + player_records_mean["TOV"]
            )
    advanced_stats["hollingerAssistRatio"] = (
        player_records_mean["AST"]
        / (
           denominator
        )
        * 100
    ).round(1) if denominator else 0
    return advanced_stats


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
