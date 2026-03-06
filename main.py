import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# load api key from env
load_dotenv()
API_KEY = os.getenv("THE_ODDS_API_KEY")

# api request config
SPORT = "upcoming"
REGIONS = "us"
MARKETS = "h2h" # head to head market

def test_api_extraction():
    print(f"Fetching {SPORT} odds from The-Odds-API")
    
    url = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds/"
    params = {
        "apiKey": API_KEY,
        "regions": REGIONS,
        "markets": MARKETS,
    }
    
    response = requests.get(url, params=params)
    
    # check for api errors
    if response.status_code != 200:
        print(f"API error {response.status_code}")
        print(response.text)
        return
        
    data = response.json()
    print(f"Success fetched {len(data)} events")
    
    # save raw json locally
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"raw_test_{timestamp}.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        
    print(f"Saved to {filename}")

if __name__ == "__main__":
    test_api_extraction()
