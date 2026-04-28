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
├── project2_data_collection.ipynb                  
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

The project is grounded in concepts from sports analytics and betting market behavior. These readings provide context on how implied probabilities, market efficiency, and news signals may influence betting markets.

Additional background readings and supporting materials are available here:  
[Background Readings Folder](https://myuva-my.sharepoint.com/:f:/g/personal/atv7xh_virginia_edu/IgA9YYliVdAuQolmQCzFfmG2AQ1rk_q6XUvspxfxyhNS6GE?e=fqkpwE)

| Title | Description | Link |
|------|-------------|------|
| Golf Betting Strategy | Overview of betting approaches and market behavior in golf | [Open](background_readings/golf_betting_strategy.pdf) |
| Market Efficiency | Explains how markets incorporate information into prices | [Open](background_readings/market_efficiency.pdf) |
| News Impact on Odds | Examines how news and media coverage influence betting markets | [Open](background_readings/news_impact_odds.pdf) |
| Implied Probability | Explains how odds are converted into probabilities | [Open](background_readings/odds_implied_probability.pdf) |
| Sports Analytics Introduction | General introduction to data-driven sports analysis | [Open](background_readings/sports_analytics_intro.pdf) |

---

## Data Creation

### Data Acquisition

The dataset was created by combining two secondary data sources: sportsbook betting odds and player-specific news coverage. Odds data was collected from The Odds API for the Masters Tournament outright winner market. Each odds snapshot captured the available sportsbook prices for individual golfers at a specific point in time. News data was collected from NewsAPI using player-specific search queries related to the Masters, Augusta, and golf.

The raw odds data and raw news data were then transformed into a player-level document dataset. Each final document represents one golfer at one market snapshot and includes betting market features, odds-change features, and recent news features. This created the final MongoDB collection `player_snapshots`, which serves as the main dataset for modeling and visualization.

### Code Table

| File | Description | Link |
|------|-------------|------|
| Data Collection Notebook | Original notebook used to collect odds/news data and upload MongoDB collections | [Open](project2_data_collection.ipynb) |
| Analysis Notebook | Structured notebook used to load MongoDB data, build models, and visualize results | [Open](project2.ipynb) |
| Pipeline Markdown | Markdown export of the structured analysis notebook | [Open](project2.md) |
| collect_odds.py | Odds collection script | [Open](code/collect_odds.py) |
| collect_news.py | News collection script | [Open](code/collect_news.py) |
| build_player_snapshots.py | Builds final merged documents | [Open](code/build_player_snapshots.py) |
| mongo_helpers.py | MongoDB connection and upload helpers | [Open](code/mongo_helpers.py) |

### Rationale for Critical Decisions

A document model was chosen because the project combines heterogeneous data sources that do not fit neatly into one flat table. Each player snapshot contains nested information about the player, tournament, odds, odds changes, and news features. MongoDB is a good fit because each document can store all relevant information for one player at one point in time without requiring many relational joins.

Another important decision was to use normalized implied probability rather than raw betting odds as the main market feature. Raw American odds are difficult to compare directly across players, while implied probability converts odds into a probability-like measure. Normalizing those probabilities within each market snapshot makes the values more comparable across players and over time.

The project also uses recent news features, such as article count, average sentiment, source diversity, and article recency. These features were included because the main research question asks whether public news signals can explain short-term movement in betting markets. The final target variable, `target_prob_up_next`, was created to indicate whether a player’s normalized implied probability increased in the next snapshot.

### Bias Identification

Several forms of bias may be introduced during the data collection process. First, media coverage is not evenly distributed across players. More famous golfers are more likely to receive articles, which can make their news features appear more active or meaningful than those of less-covered players. This introduces popularity bias.

Second, NewsAPI may not capture every relevant article, especially if articles are behind paywalls, published on smaller sites, or not indexed by the API. This creates coverage bias in the news dataset. Third, sportsbook odds may reflect bettor behavior and bookmaker risk management rather than true win probability. Betting odds are not pure estimates of athletic performance because they also include bookmaker margins and market demand.

There may also be timing bias. A news article may be published after the market has already reacted, or the market may move before the article appears publicly. This makes it difficult to prove that news caused odds movement, even if the two are correlated.

### Bias Mitigation

Several steps were used to reduce or account for these biases. First, the project uses normalized implied probability instead of raw odds, which helps make market probabilities more comparable across players and snapshots. Second, news activity is separated into multiple features, including article count, sentiment, distinct sources, and article recency. This prevents the analysis from treating all news coverage as the same.

The analysis also compares a news-only model against a combined market-and-news model. This helps avoid overstating the role of news by testing whether news features alone contain meaningful predictive signal. The results show that news-only features perform close to random, which suggests that simple news metrics are not strong enough to explain market movement by themselves.

Finally, the project explicitly treats the news data as an imperfect public signal rather than a complete record of all information available to betting markets. The findings are interpreted cautiously: the model tests association, not guaranteed causation.
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

