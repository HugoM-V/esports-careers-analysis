# 🎮 Career Dynamics in Pro Esports – Final Bootcamp Project

## 1. 🌟 Project Goals

- Analyze career dynamics of top 1000 esports players in term of tournament earnings
- Focus on **player-centric** patterns: longevity, volatility, regional factors, game-specific trends
- Go beyond surface-level dashboards — produce **insightful analysis with narrative impact**

## 2. 🔮 Philosophy & Intention

- Use esports as a passion-driven topic but apply rigorous data methods
- Showcase autonomy, structuring, and analysis depth
- Deliver results understandable to both data & non-data audiences, esports-savvy or not

## 3. 🪠 Data Strategy & Structure (Finalized)

**Data Source**: All data was retrieved from the [esportsearnings.com API](https://www.esportsearnings.com/), with some manual enrichment (notably on game types).

### 📦 Final Datasets

| File                          | Size         | Description |
|------------------------------|--------------|-------------|
| `players_profiles_with_id.csv`   | 1,000 rows   | Player handles, country, total earnings, + PlayerId for SQL joins |
| `players_tournaments_merged.csv` | 79,321 rows  | Complete tournament history (incl. extended results for high-volume players) |
| `games_metadata_enriched.csv`    | 202 rows     | Game-level metadata with manually assigned `GameType` |

### 🛠️ Initial & Intermediate Datasets

| File                     | Size        | Notes |
|--------------------------|-------------|-------|
| `top_1000_players.csv`   | 1,000 rows  | Initial player list from `LookupHighestEarningPlayers` |
| `players_profiles.csv`   | 1,000 rows  | Base for enriched player profiles from `LookupPlayerById` |
| `players_tournaments.csv`| 60,527 rows | Merged and expanded to build final tournament dataset from `LookupPlayerTournaments` |
| `games_metadata.csv`     | 182 rows    | Base for enriched game metadata from `LookupGameById` |



### 🔄 Key Relationships

- **PlayerId** as primary join key (across players & tournaments)
- **GameId** used to enrich tournament entries
- Tournaments are not directly collected — only present via player results

## 4. 🤖 Tools & Stack (temp.)

- Language: **Python**, **SQLite** 
- Libraries: `requests`, `pandas`, `json`, `time`, `dotenv`
- Secret handling: `.env` file with API key
- Storage: `.csv` (for now)
- Visualization: **Tableau**, possibly **Streamlit**

## 5. 🔎 Analytical Focus (Full Scope — Presentation Will Be Filtered)

This section outlines the full range of analytical dimensions explored throughout the project.  
The live presentation will focus on a curated subset of key insights.

### 1. Career Longevity

- Active years per player
- Career timeline of earnings
- Typologies: "one-hit wonder", "stable top", "short burst"
- 📊: Histograms, line curves, heatmaps

### 2. Income Volatility

- Share of income from biggest tournament
- Standard deviation of annual earnings
- One-peak vs. resilient careers
- 📊: Scatterplot, boxplot (by game type)

#### 2.1. Outlier Focus: Dota 2

- Yet Dota 2 alone accounts for 44% of all recorded prize money
- Only 20.7% of the top 1000 players participated in Dota 2
- Highlights the extreme prize pool concentration driven by The International, explain why
- Compared to other games across volatility, regional weight, and career structure
- 📊: Dedicated charts contrasting Dota 2 vs all other games (earnings, volatility, player share)

### 3. Regional Dynamics

- Top player distribution by country
- Earnings by region
- "3-year survival" proxy
- 📊: Choropleth map, bar/radar charts

### 4. Stability Drivers

- Game genre comparison: MOBA vs FPS vs RTS
- Avg career span by game
- Solo vs team-based games (from TeamPlayers field)
- 📊: Survival curves, bar charts by game


## 6. 📆 Timeline (approx.)

| Week | Objectives                                           |
| ---- | ---------------------------------------------------- |
| 1    | ✅ Collect, clean and structure all core datasets     |
| 2    | 🔍 Start exploratory analysis: longevity, volatility |
| 3    | 🌍 Deep-dive into regional & game-based patterns     |
| 4    | 🎨 Prepare presentation visuals & final insights     |

## 7. 📂 Folder Structure (for Github)

```
project_root/
  ├─ raw_data/                  # API-collected CSVs
  ├─ cleaned_data/              # Processed, merged files
  ├─ sql_exports/               # Optional SQL views or dumps
  ├─ notebooks/                 # Analysis in Jupyter / .ipynb
  ├─ visuals/                   # Tableau exports / screenshots
  └─ README_esports-project.md  # You are here :)
```

## 8. 🔖 Progress Log

- ✅ **30/05**: Collected top 1000 players + initial metadata (based on PlayerId)
- ✅ **01/06**: Fetched players' full tournament history (~60k rows total)
- ✅ **01/06**: Collected and matched game metadata via GameId
- ✅ **01/06**: Enriched `games_metadata.csv` with manually added GameType categories
- ✅ **01/06**: Added PlayerId to `players_profile.csv` to ensure clean PK/FK structure for joins
- ✅ **02/06**: Fetched remaining tournament pages for players with >100 results; merged all into `players_tournaments_merged.csv` (+19k rows)
- ✅ **02/06**: Retrieved missing games from new dataset (+20 entries)
- ✅ **02/06**: Imported final CSVs into SQLite via DBeaver → 4 clean tables with primary and foreign keys
- ✅ **02/06**: Created SQL views using joins: `player_career_summary`, `game_format_summary`, `earnings_by_country`
- ✅ **02/06**: Started first analyses, with a focus on Dota 2 as a structural outlier

---

- ✅ Dataset now fully covers all planned analytical axes (players & games only)
- ❌ Tournament-level analysis dropped due to too many missing TournamentIds



## 9. 🧠 Next Steps

🔜 Next: Exploratory analysis in pandas/Tableau (career length, volatility, regional distribution)


## 10. 💡 Important notes

💡 This analysis focuses exclusively on tournament earnings for the top 1000 players in term of earnings, as reported by esportsearnings.com. It does not include salaries, sponsorship deals, or streaming income — which often represent significant parts of a player's total income, but are not publicly accessible in a structured way.

-> While this limits the analysis to prize-based performance, it allows for a consistent and comparable dataset across games, regions, and time periods — offering insights into the competitive structure and financial rewards of tournament play.


💡 Although Dota 2 alone accounts for 44% of all tournament prize money, this project focuses on understanding broader career patterns across the top 1000 players. Treating Dota 2 as a statistical outlier allowed for a clearer analysis of the rest of the competitive ecosystem.

-> While most games show moderate prize growth, Dota 2 stands in a league of its own — a unique case driven by The International’s massive community-funded prize pools.


