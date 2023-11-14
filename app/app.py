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


def calculate_traditional_stats(player_rows: pd.DataFrame):
    traditional_stats = {}
    traditional_stats["freeThrows"] = {}
    traditional_stats["twoPoints"] = {}
    traditional_stats["threePoints"] = {}

    traditional_stats["freeThrows"]["attempts"] = player_rows["FTA"].round(1)
    traditional_stats["freeThrows"]["made"] = player_rows["FTM"].round(1)
    traditional_stats["freeThrows"]["shootingPercentage"] = (
        player_rows["FTM"] / player_rows["FTA"] * 100
    ).round(1)

    traditional_stats["twoPoints"]["attempts"] = player_rows["2PA"].round(1)
    traditional_stats["twoPoints"]["made"] = player_rows["2PM"].round(1)
    traditional_stats["twoPoints"]["shootingPercentage"] = (
        player_rows["2PM"] / player_rows["2PA"] * 100
    ).round(1)

    traditional_stats["threePoints"]["attempts"] = player_rows["3PA"].round(1)
    traditional_stats["threePoints"]["made"] = player_rows["3PM"].round(1)
    traditional_stats["threePoints"]["shootingPercentage"] = (
        player_rows["3PM"] / player_rows["3PA"] * 100
    ).round(1)

    traditional_stats["points"] = (
        player_rows["FTM"]
        + 2 * player_rows["2PM"]
        + 3 * player_rows["3PM"]
    ).round(1)
    traditional_stats["rebounds"] = player_rows["REB"].round(1)
    traditional_stats["blocks"] = player_rows["BLK"].round(1)
    traditional_stats["assists"] = player_rows["AST"].round(1)
    traditional_stats["steals"] = player_rows["STL"].round(1)
    traditional_stats["turnovers"] = player_rows["TOV"].round(1)

    return traditional_stats


def calculate_advanced_stats(player_rows: pd.DataFrame):
    advanced_stats = {}
    TPS = (
        player_rows["FTM"]
        + 2 * player_rows["2PM"]
        + 3 * player_rows["3PM"]
    )
    advanced_stats["valorization"] = (
        (
            player_rows["FTM"]
            + 2 * player_rows["2PM"]
            + 3 * player_rows["3PM"]
            + player_rows["REB"]
            + player_rows["BLK"]
            + player_rows["AST"]
            + player_rows["STL"]
        )
        - (
            player_rows["FTA"]
            - player_rows["FTM"]
            + player_rows["2PA"]
            - player_rows["2PM"]
            + player_rows["3PA"]
            - player_rows["3PM"]
            + player_rows["TOV"]
        )
    ).round(1)

    advanced_stats["effectiveFieldGoalPercentage"] = (
        (player_rows["2PM"] + 1.5 * player_rows["3PM"])
        / (player_rows["2PA"] + player_rows["3PA"])
        * 100
    ).round(1)

    advanced_stats["trueShootingPercentage"] = (
        TPS
        / (
            2
            * (
                player_rows["2PA"]
                + player_rows["3PA"]
                + 0.475 * player_rows["FTA"]
            )
        )
        * 100
    ).round(1)

    advanced_stats["hollingerAssistRatio"] = (
        player_rows["AST"]
        / (
            player_rows["2PA"]
            + player_rows["3PA"]
            + 0.475 * player_rows["FTA"]
            + player_rows["AST"]
            + player_rows["TOV"]
        )
        * 100
    ).round(1)
    return advanced_stats




if __name__ == "__main__":
    app.run(debug=True)
