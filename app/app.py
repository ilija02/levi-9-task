import os
import pandas as pd

from flask import Flask, jsonify

app = Flask(__name__)
app.json.sort_keys = False


# Load the file data into memory
basketball_data = pd.read_csv("L9HomeworkChallengePlayersInput.csv")


# Endpoint for retrieving player stats
@app.route("/stats/player/<playerFullName>/", methods=["GET"])
def get_player_stats(playerFullName):
    if not playerFullName:
        return jsonify({"error": "Player name is required"}), 400
    player_stats = calculate_player_stats(playerFullName)
    if player_stats.get("error"):
        return jsonify(player_stats), 404

    return jsonify(player_stats)

def get_mean_values(player_rows):
    numerical_columns = player_rows.drop(['PLAYER', 'POSITION'], axis=1)
    return numerical_columns.mean()

# Calculate stats for a given player
def calculate_player_stats(player_name):
    player_rows = basketball_data[basketball_data["PLAYER"] == player_name]
    if player_rows.empty:
        return {"error": "Player not found"}

    player_rows_mean = get_mean_values(player_rows)

    response = {}
    response["playerName"] = player_name
    response["gamesPlayed"] = len(player_rows)
    response["traditional"] = calculate_traditional_stats(player_rows_mean)
    response["advanced"] = calculate_advanced_stats(player_rows_mean)
    return response


def calculate_traditional_stats(player_rows_mean: pd.DataFrame):
    traditional_stats = {}
    traditional_stats["freeThrows"] = {}
    traditional_stats["twoPoints"] = {}
    traditional_stats["threePoints"] = {}

    traditional_stats["freeThrows"]["attempts"] = player_rows_mean["FTA"].round(1)
    traditional_stats["freeThrows"]["made"] = player_rows_mean["FTM"].round(1)
    traditional_stats["freeThrows"]["shootingPercentage"] = (
        player_rows_mean["FTM"] / player_rows_mean["FTA"] * 100
    ).round(1)

    traditional_stats["twoPoints"]["attempts"] = player_rows_mean["2PA"].round(1)
    traditional_stats["twoPoints"]["made"] = player_rows_mean["2PM"].round(1)
    traditional_stats["twoPoints"]["shootingPercentage"] = (
        player_rows_mean["2PM"] / player_rows_mean["2PA"] * 100
    ).round(1)

    traditional_stats["threePoints"]["attempts"] = player_rows_mean["3PA"].round(1)
    traditional_stats["threePoints"]["made"] = player_rows_mean["3PM"].round(1)
    traditional_stats["threePoints"]["shootingPercentage"] = (
        player_rows_mean["3PM"] / player_rows_mean["3PA"] * 100
    ).round(1)

    traditional_stats["points"] = (
        player_rows_mean["FTM"]
        + 2 * player_rows_mean["2PM"]
        + 3 * player_rows_mean["3PM"]
    ).round(1)
    traditional_stats["rebounds"] = player_rows_mean["REB"].round(1)
    traditional_stats["blocks"] = player_rows_mean["BLK"].round(1)
    traditional_stats["assists"] = player_rows_mean["AST"].round(1)
    traditional_stats["steals"] = player_rows_mean["STL"].round(1)
    traditional_stats["turnovers"] = player_rows_mean["TOV"].round(1)

    return traditional_stats


def calculate_advanced_stats(player_rows_mean: pd.DataFrame):
    advanced_stats = {}
    TPS = (
        player_rows_mean["FTM"]
        + 2 * player_rows_mean["2PM"]
        + 3 * player_rows_mean["3PM"]
    )
    advanced_stats["valorization"] = (
        (
            player_rows_mean["FTM"]
            + 2 * player_rows_mean["2PM"]
            + 3 * player_rows_mean["3PM"]
            + player_rows_mean["REB"]
            + player_rows_mean["BLK"]
            + player_rows_mean["AST"]
            + player_rows_mean["STL"]
        )
        - (
            player_rows_mean["FTA"]
            - player_rows_mean["FTM"]
            + player_rows_mean["2PA"]
            - player_rows_mean["2PM"]
            + player_rows_mean["3PA"]
            - player_rows_mean["3PM"]
            + player_rows_mean["TOV"]
        )
    ).round(1)

    advanced_stats["effectiveFieldGoalPercentage"] = (
        (player_rows_mean["2PM"] + 1.5 * player_rows_mean["3PM"])
        / (player_rows_mean["2PA"] + player_rows_mean["3PA"])
        * 100
    ).round(1)

    advanced_stats["trueShootingPercentage"] = (
        TPS
        / (
            2
            * (
                player_rows_mean["2PA"]
                + player_rows_mean["3PA"]
                + 0.475 * player_rows_mean["FTA"]
            )
        )
        * 100
    ).round(1)

    advanced_stats["hollingerAssistRatio"] = (
        player_rows_mean["AST"]
        / (
            player_rows_mean["2PA"]
            + player_rows_mean["3PA"]
            + 0.475 * player_rows_mean["FTA"]
            + player_rows_mean["AST"]
            + player_rows_mean["TOV"]
        )
        * 100
    ).round(1)
    return advanced_stats




if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port = port)
