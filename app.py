from flask import Flask, render_template, jsonify
import requests
import random  # For placeholder predictions

app = Flask(__name__)

API_KEY = "f96d6d7c-2d7e-4466-b75a-2553c2009262"

# 🔹 Fetch live match data
# Fetch Live India Match (National Team only)
def fetch_live_match():
    url = f"https://api.cricapi.com/v1/cricScore?apikey={API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json().get("data", [])

    for match in data:
        team1 = match.get("t1", "").strip().lower()
        team2 = match.get("t2", "").strip().lower()
        match_status = match.get("ms", "").lower()

        # ✅ Check if "India" is in the team name but exclude "India Masters", "India A", etc.
        if "india" in team1 and "masters" not in team1 and "a" not in team1:
            is_india_match = True
        elif "india" in team2 and "masters" not in team2 and "a" not in team2:
            is_india_match = True
        else:
            is_india_match = False

        # 🔥 Ensure it's an **actual live match** involving the national team
        if is_india_match and "live" in match_status:
            return {
                "match_id": match["id"],
                "series": match.get("series", "Unknown Series"),
                "team1": match["t1"],
                "team2": match["t2"],
                "team1_score": match.get("t1s", ""),
                "team2_score": match.get("t2s", ""),
                "status": match["status"],
            }

    return None  # No live India national team match found

# 🔹 Predict final score
def predict_final_score(current_score, overs_played):
    if not current_score:
        return "N/A"

    runs = int(current_score.split("/")[0].split("(")[0])
    avg_run_rate = runs / overs_played if overs_played else 0
    projected_score = avg_run_rate * 50

    return round(projected_score)

# 🔹 Predict win probability
def predict_win_probability(team1_score, team2_score):
    if not team1_score:
        return {"team1": 50, "team2": 50}

    team1_win_prob = round(random.uniform(40, 60), 2)
    team2_win_prob = 100 - team1_win_prob

    return {"team1": team1_win_prob, "team2": team2_win_prob}

# 🔹 Main Page Route
@app.route("/")
def home():
    return render_template("index.html")

# 🔹 API Endpoint for Live Updates (Called by AJAX)
@app.route("/live-score")
def live_score():
    match = fetch_live_match()
    
    if not match:
        return jsonify({"error": "No live India match found"})

    team1 = match["team1"]
    team2 = match["team2"]
    team1_score = match["team1_score"]
    team2_score = match["team2_score"]
    status = match["status"]

    projected_score = predict_final_score(team1_score, overs_played=30)
    win_probabilities = predict_win_probability(team1_score, team2_score)

    return jsonify({
        "series": match["series"],
        "team1": team1,
        "team2": team2,
        "team1_score": team1_score,
        "team2_score": team2_score,
        "status": status,
        "projected_score": projected_score,
        "win_probability": win_probabilities
    })

if __name__ == "__main__":
    app.run(debug=True)
