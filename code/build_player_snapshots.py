"""
Build final player-level snapshot documents by combining odds and news features.
"""

import logging
import pandas as pd


logging.basicConfig(
    filename="logs/project2_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def aggregate_odds(odds_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sportsbook-level odds into player-level odds snapshots."""
    grouped = (
        odds_df
        .groupby(["player_name", "event_id", "event_name", "commence_time"], as_index=False)
        .agg(
            average_american_price=("american_price", "mean"),
            raw_implied_prob=("raw_implied_prob", "mean"),
            sportsbook_quote_count=("sportsbook", "nunique")
        )
    )

    total_prob = grouped["raw_implied_prob"].sum()

    if total_prob > 0:
        grouped["normalized_implied_prob"] = grouped["raw_implied_prob"] / total_prob
    else:
        grouped["normalized_implied_prob"] = None

    return grouped


def add_odds_change_features(odds_df: pd.DataFrame) -> pd.DataFrame:
    """Add change features for implied probability and odds."""
    odds_df = odds_df.sort_values(["player_name", "commence_time"]).copy()

    odds_df["odds_change_avg_american_price"] = (
        odds_df.groupby("player_name")["average_american_price"].diff()
    )

    odds_df["odds_change_raw_implied_prob"] = (
        odds_df.groupby("player_name")["raw_implied_prob"].diff()
    )

    odds_df["odds_change_normalized_implied_prob"] = (
        odds_df.groupby("player_name")["normalized_implied_prob"].diff()
    )

    return odds_df


def aggregate_news(news_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate news articles into player-level news features."""
    if news_df.empty:
        return pd.DataFrame(columns=[
            "player_name",
            "article_count_24h",
            "avg_sentiment_24h",
            "distinct_sources_24h"
        ])

    grouped = (
        news_df
        .groupby("player_name", as_index=False)
        .agg(
            article_count_24h=("title", "count"),
            avg_sentiment_24h=("sentiment_score", "mean"),
            distinct_sources_24h=("source", "nunique")
        )
    )

    return grouped


def build_player_snapshots(odds_df: pd.DataFrame, news_df: pd.DataFrame) -> pd.DataFrame:
    """
    Combine odds and news data into the final player snapshot dataset.
    """
    odds_agg = aggregate_odds(odds_df)
    odds_agg = add_odds_change_features(odds_agg)

    news_agg = aggregate_news(news_df)

    player_df = odds_agg.merge(
        news_agg,
        on="player_name",
        how="left"
    )

    news_cols = [
        "article_count_24h",
        "avg_sentiment_24h",
        "distinct_sources_24h"
    ]

    for col in news_cols:
        if col in player_df.columns:
            player_df[col] = player_df[col].fillna(0)

    player_df["tournament"] = "Masters Tournament"
    player_df["snapshot_time_utc"] = pd.Timestamp.utcnow()

    logging.info(f"Built player snapshot dataframe with shape {player_df.shape}")

    return player_df


if __name__ == "__main__":
    print("This file is intended to be imported by the notebook pipeline.")
