"""
Collect Masters odds data from The Odds API.

This script is written as a reusable structure for the project.
The main notebook contains the final executed collection workflow.
"""

import os
import logging
from typing import List, Dict, Any

import requests
import pandas as pd
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(
    filename="logs/project2_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def american_to_implied_probability(price: float) -> float:
    """Convert American odds into implied probability."""
    if price is None:
        return None

    if price > 0:
        return 100 / (price + 100)

    return abs(price) / (abs(price) + 100)


def fetch_odds(api_key: str, sport_key: str, region: str = "us") -> Dict[str, Any]:
    """Fetch odds data from The Odds API."""
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds"

    params = {
        "apiKey": api_key,
        "regions": region,
        "markets": "outrights",
        "oddsFormat": "american"
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    return response.json()


def flatten_odds_response(raw_data: List[Dict[str, Any]]) -> pd.DataFrame:
    """Flatten raw odds API response into player-level rows."""
    rows = []

    for event in raw_data:
        event_id = event.get("id")
        event_name = event.get("home_team") or event.get("sport_title")
        commence_time = event.get("commence_time")

        for bookmaker in event.get("bookmakers", []):
            sportsbook = bookmaker.get("title")

            for market in bookmaker.get("markets", []):
                for outcome in market.get("outcomes", []):
                    player_name = outcome.get("name")
                    american_price = outcome.get("price")

                    rows.append({
                        "event_id": event_id,
                        "event_name": event_name,
                        "commence_time": commence_time,
                        "sportsbook": sportsbook,
                        "player_name": player_name,
                        "american_price": american_price,
                        "raw_implied_prob": american_to_implied_probability(american_price)
                    })

    return pd.DataFrame(rows)


def collect_odds_dataframe() -> pd.DataFrame:
    """Main function to collect and return odds data as a DataFrame."""
    api_key = os.getenv("ODDS_API_KEY")

    if not api_key:
        raise ValueError("ODDS_API_KEY is missing. Add it to your .env file.")

    sport_key = "golf_masters_tournament_winner"

    raw_data = fetch_odds(api_key, sport_key)
    odds_df = flatten_odds_response(raw_data)

    logging.info(f"Collected odds dataframe with shape {odds_df.shape}")
    return odds_df


if __name__ == "__main__":
    df = collect_odds_dataframe()
    print(df.head())
    print(df.shape)
