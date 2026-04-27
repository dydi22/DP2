# DS 4320 Project 2: Forecasting Masters Betting Market Movement with Odds and News Data

## Executive Summary

This repository contains a document-model data project that studies how betting market expectations changed during the 2026 Masters Tournament. The project builds a secondary dataset by combining historical sportsbook odds from The Odds API with player-specific news articles from NewsAPI. The final MongoDB database stores odds snapshots, news articles, and merged player-level snapshot documents. The analysis pipeline queries MongoDB into a pandas DataFrame, engineers news and odds-change features, and visualizes how implied win probabilities moved over time.

## Name

Dylan Dietrich

## NetID

atv7xh

## DOI

[Add DOI here]

## Project Materials

- [Press Release](press_release.md)
- [Pipeline Notebook](project2.ipynb)
- [Pipeline Markdown](project2.md)
- [License](LICENSE)

---

## Problem Definition

### General Problem

Forecasting stock prices / forecasting market movement.

### Refined Specific Problem

This project refines the general problem of forecasting market movement into the specific problem of forecasting changes in Masters Tournament betting odds. Instead of predicting a stock price, the project analyzes whether player-specific news signals are associated with changes in sportsbook-implied win probabilities.

### Motivation

Betting markets are useful because they continuously update based on public expectations, news, injuries, performance trends, and bettor behavior. In golf, tournament winner odds can change quickly as new information becomes available. Understanding these movements can help analysts study how information enters the market and how public signals, such as news coverage, relate to changes in implied probabilities.

### Rationale for Refinement

I refined the broad problem of forecasting stock prices into sports betting market movement because both settings involve time-series market prices, changing probabilities, and information-driven updates. The Masters Tournament is a useful case study because it has a clear outcome, many competitors, and active betting markets. This also fits naturally into a document model because each player snapshot can store nested odds data, odds-change fields, and news features together in one document.

### Press Release

[Can News Signals Explain Masters Betting Market Movement?](press_release.md)

---

## Domain Exposition

### Terminology

| Term | Meaning | Why it matters |
|---|---|---|
| American Odds | Betting odds format used in U.S. sportsbooks | Raw market price from bookmakers |
| Implied Probability | Probability converted from betting odds | Makes odds comparable across players |
| Normalized Implied Probability | Implied probability adjusted so probabilities sum across the market | Better reflects relative market expectations |
| Odds Snapshot | A record of player odds at one point in time | Main time-series unit |
| News Sentiment | Simple score based on positive/negative words in player news | Used as an explanatory feature |
| Lookback Window | Time period before each odds snapshot used to collect news | Connects recent news to market movement |
| Odds Change | Difference in odds or implied probability from the previous snapshot | Target movement being analyzed |

### Domain Description

This project lives in the sports analytics and betting market domain. Betting odds act like market prices because they reflect the current expectations of bookmakers and bettors. When new information appears, such as player injuries, strong performance, or tournament news, betting prices may shift. By combining odds data with player-specific news data, this project studies whether public information can help explain movement in implied win probabilities.

### Background Readings

| Title | Description | Link |
|---|---|---|
| The Odds API Documentation | Explains how sportsbook odds are collected and returned | `background_readings/odds_api_documentation.pdf` |
| NewsAPI Documentation | Explains how news articles are queried by topic and time range | `background_readings/newsapi_documentation.pdf` |
| MongoDB Document Model | Explains why nested document structures are useful | `background_readings/mongodb_document_model_article.pdf` |
| Sports Betting Market Efficiency | Background on how betting markets react to information | `background_readings/sports_betting_market_efficiency.pdf` |
| Golf Prediction / Betting Article | Domain context for golf tournament forecasting | `background_readings/golf_prediction_article.pdf` |

---

## Data Creation

### Raw Data Acquisition

The dataset was created by collecting historical Masters Tournament outright winner odds from The Odds API and player-specific news articles from NewsAPI. Odds were requested every 15 minutes from April 9, 2026 through April 12, 2026. Each odds response was transformed into player-level documents containing sportsbook prices, average American odds, raw implied probability, and normalized implied probability. News articles were collected for each player using queries that combined the player name with Masters, Augusta, or golf-related terms.

### Code Table

| File | Description | Link |
|---|---|---|
| `project2.ipynb` | Main data creation and analysis notebook | `project2.ipynb` |
| `src/collect_odds.py` | Fetches historical odds data from The Odds API | `src/collect_odds.py` |
| `src/collect_news.py` | Fetches player-specific articles from NewsAPI | `src/collect_news.py` |
| `src/build_player_snapshots.py` | Merges odds and news into final documents | `src/build_player_snapshots.py` |
| `src/mongo_helpers.py` | MongoDB connection, indexes, and helper functions | `src/mongo_helpers.py` |

### Rationale for Critical Decisions

The document model was chosen because each player snapshot naturally contains nested information: tournament metadata, odds data, odds-change data, and news features. This makes each document self-contained and easy to query for analysis. The 24-hour news lookback window was chosen to connect recent news coverage to each odds snapshot without using information from the future. Normalized implied probability was used instead of raw odds because it gives a clearer measure of each player’s relative market expectation.

### Bias Identification

Bias may enter the dataset through sportsbook coverage, NewsAPI coverage, and player popularity. More famous players are likely to have more news articles, which could make their news features appear more important than those of lesser-known players. Sportsbook odds also include bookmaker margin and may reflect betting behavior rather than true win probability.

### Bias Mitigation

To reduce bias, the project normalizes implied probabilities across players and tracks article counts separately from sentiment. This makes it possible to distinguish between the amount of coverage and the tone of coverage. The analysis also reports missing or zero-news cases so that players with limited media coverage are not treated the same as players with active news signals.

---

## Metadata

### Implicit Schema Guidelines

The final MongoDB document model uses a player-level snapshot structure. Each document represents one player at one timestamp.

```json
{
  "snapshot_time_utc": "2026-04-09T00:00:00Z",
  "tournament": "Masters Tournament Winner",
  "player_name": "Scottie Scheffler",
  "odds": {
    "average_american_price": 620,
    "raw_implied_prob": 0.1389,
    "normalized_implied_prob": 0.0842
  },
  "odds_change": {
    "average_american_price": -20,
    "raw_implied_prob": 0.003,
    "normalized_implied_prob": 0.001
  },
  "news_features": {
    "article_count_24h": 4,
    "avg_sentiment_24h": 0.015,
    "distinct_sources_24h": 3
  }
}
