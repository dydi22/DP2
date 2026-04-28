# DS 4320 Project 2: Do News Signals Explain Betting Market Movement in the Masters?

## Executive Summary

This project investigates whether player-specific news signals can explain short-term movement in betting market implied probabilities during the 2026 Masters Tournament. A document-model dataset was created using MongoDB by combining sportsbook odds data from The Odds API with player-level news articles from NewsAPI. Each document represents a player snapshot containing odds, odds changes, and recent news features. The analysis pipeline loads this data into a pandas DataFrame and evaluates whether news-based features can predict whether a player’s implied probability increases in the next snapshot. Results show that news signals alone perform at near-random accuracy, while market-based features provide stronger predictive power, suggesting that betting markets efficiently incorporate public information.

## Name

Dylan Dietrich  

## NetID  

atv7xh  

## DOI  

[INSERT DOI HERE]


---

## Repository Structure

```text
DS4320-Project2/
├── README.md                         
├── press_release.md                  
├── project2.ipynb                    
├── project2.md                   
├── LICENSE                   

├── background_readings/              
│   ├── odds_api_docs.pdf
│   ├── newsapi_docs.pdf
│   ├── mongodb_document_model.pdf
│   ├── market_efficiency.pdf
│   └── sports_analytics_paper.pdf

├── code/                             
│   ├── collect_odds.py               
│   ├── collect_news.py               
│   ├── build_player_snapshots.py     
│   └── mongo_helpers.py              

├── images/                          
│   ├── implied_prob_over_time.png
│   └── model_results.png

└── logs/                             
    └── project2_pipeline.log
```


## Problem Definition

### General Problem

Forecasting market movement.

### Refined Specific Problem

This project refines the general problem of forecasting market movement into predicting short-term changes in betting market implied probabilities for players in the Masters Tournament. Specifically, it tests whether recent news signals (such as article count and sentiment) help predict whether a player's normalized implied probability increases in the next odds snapshot.

### Motivation

Betting markets behave similarly to financial markets, continuously updating as new information becomes available. Understanding whether public information such as news coverage influences these movements provides insight into market efficiency and information flow. This problem is particularly interesting in sports analytics, where both performance and perception can impact betting odds.

### Rationale for Refinement

The broad problem of forecasting stock prices was refined to sports betting markets because they provide structured, high-frequency probability updates and a clear outcome. The Masters Tournament was selected due to its well-defined timeframe and active betting markets. This problem also fits naturally into a document model, as each player snapshot contains nested data such as odds, news features, and changes over time.

### Press Release

[Do News Signals Drive Betting Market Movement?](press_release.md)

---

## Domain Exposition

### Terminology

| Term | Meaning | Why it matters |
|------|---------|----------------|
| American Odds | Betting odds format | Raw market price |
| Implied Probability | Probability derived from odds | Comparable metric |
| Normalized Probability | Adjusted probability across players | Market-relative measure |
| Odds Snapshot | Market state at a timestamp | Time-series unit |
| News Sentiment | Score from article text | Potential signal |
| Odds Change | Change in probability over time | Target variable |

### Domain Description

This project operates in the sports betting and analytics domain. Betting odds reflect collective expectations about outcomes and adjust rapidly as new information becomes available. By combining structured betting data with unstructured news data, this project evaluates whether public information can explain short-term market behavior.

### Background Readings

The project is grounded in concepts from document databases and sports analytics. In particular, MongoDB’s document model allows data to be stored as flexible JSON-like documents rather than rigid tables, enabling easier integration of heterogeneous data such as odds and news features.

Additional background readings, including API documentation and supporting materials, are available here:  
[Background Readings Folder](https://myuva-my.sharepoint.com/:f:/g/personal/atv7xh_virginia_edu/IgA9YYliVdAuQolmQCzFfmG2AQ1rk_q6XUvspxfxyhNS6GE?e=fqkpwE)

| Title | Description | Link |
|------|-------------|------|
| Odds API Docs | Odds data collection | [Open](background_readings/odds_api_docs.pdf) |
| NewsAPI Docs | News data collection | [Open](background_readings/newsapi_docs.pdf) |
| MongoDB Docs | Document model structure | [Open](background_readings/mongodb_document_model.pdf) |
| Market Efficiency | How markets process information | [Open](background_readings/market_efficiency.pdf) |
| Sports Analytics | Context for prediction | [Open](background_readings/sports_analytics_paper.pdf) |

---

## Data Creation

### Data Acquisition

Odds data was collected from The Odds API at regular intervals during the Masters Tournament. News data was collected from NewsAPI using player-specific queries. These datasets were merged into player-level snapshot documents, each representing a player’s state at a given time.

### Code Table

| File | Description | Link |
|------|-------------|------|
| project2.ipynb | Main analysis pipeline | project2.ipynb |
| collect_odds.py | Odds collection script | code/collect_odds.py |
| collect_news.py | News collection script | code/collect_news.py |
| build_player_snapshots.py | Builds final merged documents | code/build_player_snapshots.py |
| mongo_helpers.py | MongoDB connection and upload helpers | code/mongo_helpers.py |

### Rationale for Decisions

A document model was chosen because it allows each player snapshot to store nested information, including odds, odds changes, and news features. This structure simplifies querying and aligns with time-series analysis.

### Bias Identification

Bias may arise from unequal news coverage across players, sportsbook pricing strategies, and missing data.

### Bias Mitigation

Normalization of probabilities and inclusion of multiple features (counts, sentiment, sources) helps reduce bias and provides a more balanced representation of information.

---

## Metadata

### Schema

```json
{
  "player_name": "Rory McIlroy",
  "snapshot_time_utc": "...",
  "feature_vector": {
    "normalized_implied_prob": 0.07,
    "odds_change_normalized_implied_prob": 0.002,
    "article_count_24h": 3,
    "avg_sentiment_24h": 0.01
  }
}
```

### Data Summary

| Collection | Description | Approx Size |
|------------|------------|-------------|
| odds_snapshots | Raw odds collected over time | 35,000+ |
| news_articles | Player-specific news articles | 700+ |
| player_snapshots | Final merged dataset | 35,000+ |


### Data Dictionary

| Feature | Type | Description | Example |
|--------|------|------------|--------|
| player_name | string | Player name | Scottie Scheffler |
| snapshot_time_utc | datetime | Time of snapshot | 2026-04-09T00:00:00Z |
| normalized_implied_prob | float | Market probability | 0.084 |
| odds_change_normalized_implied_prob | float | Change from previous snapshot | 0.002 |
| article_count_24h | int | Number of recent articles | 4 |
| avg_sentiment_24h | float | Average sentiment score | 0.01 |
| distinct_sources_24h | int | Number of unique sources | 3 |
| latest_article_age_hours | float | Age of most recent article | 2.5 |

### Uncertainty Quantification

| Feature | Missing % | Notes |
|--------|----------|------|
| avg_sentiment_24h | Low | Based on simple NLP |
| article_count_24h | Medium | Depends on API coverage |
| normalized_implied_prob | Low | Derived from odds |
| odds_change_normalized_implied_prob | Medium | First observation missing |
| latest_article_age_hours | Medium | Depends on timing of news |

