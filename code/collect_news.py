"""
Collect player-specific news articles from NewsAPI.
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


POSITIVE_WORDS = ["win", "strong", "favorite", "surge", "healthy", "confident", "leader"]
NEGATIVE_WORDS = ["injury", "struggle", "miss", "poor", "withdraw", "concern", "bad"]


def simple_sentiment(text: str) -> float:
    """
    Compute a simple sentiment score from article text.

    Positive score means more positive words.
    Negative score means more negative words.
    """
    if not text:
        return 0.0

    text = text.lower()

    positive_count = sum(word in text for word in POSITIVE_WORDS)
    negative_count = sum(word in text for word in NEGATIVE_WORDS)

    return positive_count - negative_count


def fetch_player_news(api_key: str, player_name: str, page_size: int = 20) -> List[Dict[str, Any]]:
    """Fetch news articles for a single player."""
    url = "https://newsapi.org/v2/everything"

    query = f'"{player_name}" AND (Masters OR Augusta OR golf)'

    params = {
        "apiKey": api_key,
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    return response.json().get("articles", [])


def collect_news_for_players(player_names: List[str]) -> pd.DataFrame:
    """Collect news articles for a list of player names."""
    api_key = os.getenv("NEWS_API_KEY")

    if not api_key:
        raise ValueError("NEWS_API_KEY is missing. Add it to your .env file.")

    rows = []

    for player_name in player_names:
        try:
            articles = fetch_player_news(api_key, player_name)

            for article in articles:
                title = article.get("title") or ""
                description = article.get("description") or ""
                content = f"{title} {description}"

                rows.append({
                    "player_name": player_name,
                    "title": title,
                    "description": description,
                    "source": article.get("source", {}).get("name"),
                    "url": article.get("url"),
                    "published_at": article.get("publishedAt"),
                    "sentiment_score": simple_sentiment(content)
                })

        except Exception as error:
            logging.warning(f"Failed to collect news for {player_name}: {error}")

    news_df = pd.DataFrame(rows)
    logging.info(f"Collected news dataframe with shape {news_df.shape}")

    return news_df


if __name__ == "__main__":
    sample_players = ["Scottie Scheffler", "Rory McIlroy", "Jon Rahm"]
    df = collect_news_for_players(sample_players)
    print(df.head())
    print(df.shape)
