# import requests

# API_KEY = "f96d6d7c-2d7e-4466-b75a-2553c2009262"
# url = f"https://api.cricapi.com/v1/currentMatches?apikey={API_KEY}"

# def get_live_score():
#     response = requests.get(url).json()

#     match = response["data"][0]
#     team1 = match["team1"]["name"]
#     team2 = match["team2"]["name"] 
#     score = match["score"]

#     return f"{team1} vs {team2}: {score}"

# print(get_live_score())


# import requests

# API_KEY = "f96d6d7c-2d7e-4466-b75a-2553c2009262"
# url = f"https://api.cricapi.com/v1/currentMatches?apikey={API_KEY}"

# def get_live_score():
#     response = requests.get(url).json()
#     print(response)  # Print to check the API response structure

#     if "data" not in response or not response["data"]:
#         return "No live matches found."

#     match = response["data"][0]  # Taking the first live match

#     # Extracting team names
#     if "teams" in match:
#         team1, team2 = match["teams"]
#     else:
#         return "Team data not found."

#     # Extracting scores
#     score_data = match.get("score", [])

#     if score_data:
#         scores = "\n".join([f"{s['inning']}: {s['r']}/{s['w']} in {s['o']} overs" for s in score_data])
#     else:
#         scores = "Score not available."

#     return f"Match: {team1} vs {team2}\n{scores}"

# print(get_live_score())  # Run and check

# import requests

# # API Endpoint & API Key (Replace with your actual API key)
# API_URL = "https://api.cricapi.com/v1/currentMatches"
# API_KEY = "f96d6d7c-2d7e-4466-b75a-2553c2009262"  # Replace with your actual API key

# # Fetch live match data
# params = {"apikey": API_KEY}
# response = requests.get(API_URL, params=params)
# data = response.json()

# # Check if API request was successful
# if data.get("status") == "success" and "data" in data:
#     matches = data["data"]

#     # Look for the India vs Australia match
#     found_match = False
#     for match in matches:
#         if "India" in match["teams"] and "Australia" in match["teams"] and not match["matchEnded"]:
#             found_match = True
#             print(f"\n🏏 Match: {match['name']}")
#             print(f"📍 Venue: {match['venue']}")
#             print(f"🕒 Status: {match['status']}\n")
            
#             # Print current score details
#             for score in match.get("score", []):
#                 print(f"➡️ {score['inning']}: {score['r']}/{score['w']} in {score['o']} overs")
#             break  # Stop after finding the first live India vs Australia match

#     if not found_match:
#         print("⚠️ No live India vs Australia match found.")

# else:
#     print("❌ Failed to fetch match data. Please check your API key or network connection.")


import requests
import time

# API Endpoint & API Key (Replace with your actual API key)
API_URL = "https://api.cricapi.com/v1/currentMatches"
API_KEY = "f96d6d7c-2d7e-4466-b75a-2553c2009262"  # Replace with your actual API key

def fetch_match_data():
    """Fetch live match data from the API."""
    params = {"apikey": API_KEY}
    response = requests.get(API_URL, params=params)
    return response.json()

def display_live_score():
    """Continuously fetch and display the India vs Australia match score."""
    last_score = None  # Store the last fetched score to detect changes
    
    while True:
        data = fetch_match_data()
        
        if data.get("status") == "success" and "data" in data:
            matches = data["data"]
            found_match = False

            for match in matches:
                if "India" in match["teams"] and "Australia" in match["teams"] and not match["matchEnded"]:
                    found_match = True
                    print("\n" + "="*50)
                    print(f"🏏 Match: {match['name']}")
                    print(f"📍 Venue: {match['venue']}")
                    print(f"🕒 Status: {match['status']}\n")

                    # Get latest score details
                    latest_score = []
                    for score in match.get("score", []):
                        latest_score.append(f"➡️ {score['inning']}: {score['r']}/{score['w']} in {score['o']} overs")

                    # Only update the screen if the score has changed
                    if latest_score != last_score:
                        for line in latest_score:
                            print(line)
                        last_score = latest_score  # Update last score

                    break  # Stop after finding the first live India vs Australia match
            
            if not found_match:
                print("⚠️ No live India vs Australia match found.")
        
        else:
            print("❌ Failed to fetch match data. Please check your API key or network connection.")

        # Wait for a few seconds before fetching new data
        time.sleep(10)  # Update every 10 seconds

# Run the live score updater
display_live_score()
