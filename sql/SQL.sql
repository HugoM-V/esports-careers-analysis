CREATE TABLE players_profiles_with_id (
    PlayerId INTEGER PRIMARY KEY,
    NameFirst TEXT,
    NameLast TEXT,
    CurrentHandle TEXT,
    CountryCode TEXT,
    WorldRanking INTEGER,
    CountryRanking INTEGER,
    TotalUSDPrize FLOAT,
    TotalTournaments INTEGER
);

SELECT * FROM players_profiles_with_id
LIMIT 10;

SELECT COUNT(*) FROM players_profiles_with_id;

CREATE TABLE games_metadata_enriched (
    GameId INTEGER PRIMARY KEY,
    GameName TEXT,
    TotalUSDPrize FLOAT,
    TotalTournaments INTEGER,
    TotalPlayers INTEGER,
    GameType TEXT
);

CREATE TABLE top_1000_players (
    PlayerId INTEGER PRIMARY KEY,
    NameFirst TEXT,
    NameLast TEXT,
    CurrentHandle TEXT,
    CountryCode TEXT,
    TotalUSDPrize FLOAT
);
DROP TABLE IF EXISTS players_tournaments;

CREATE TABLE players_tournaments (
    RankText TEXT,
    Prize FLOAT,
    ExchangeRate FLOAT,
    CurrencyCode TEXT,
    TournamentName TEXT,
    EndDate DATE,
    GameId INTEGER,
    Note TEXT,
    TeamPlayers INTEGER,
    PlayerId INTEGER,
    FOREIGN KEY (PlayerId) REFERENCES top_1000_players(PlayerId),
    FOREIGN KEY (GameId) REFERENCES games_metadata_enriched(GameId)
);


SELECT EndDate, DATE(EndDate) AS ParsedDate
FROM players_tournaments
LIMIT 5;

SELECT *
FROM players_tournaments
WHERE EndDate >= '2022-01-01'
LIMIT 5;

SELECT CurrentHandle, CountryCode, TotalUSDPrize
FROM top_1000_players
ORDER BY TotalUSDPrize DESC;

SELECT TournamentName, EndDate, Prize
FROM players_tournaments
WHERE PlayerId = 3304
ORDER BY EndDate DESC;

SELECT PlayerId
FROM players_tournaments
GROUP BY PlayerId
HAVING COUNT(*) = 100;

SELECT * FROM TOP_1000_PLAYERS TP
WHERE PLAYERID = 14175


DROP TABLE IF EXISTS players_tournaments;
DROP TABLE IF EXISTS GAMES_METaDATA_ENRICHED;

CREATE TABLE games (
    GameId INTEGER PRIMARY KEY,
    GameName TEXT,
    TotalUSDPrize FLOAT,
    TotalTournaments INTEGER,
    TotalPlayers INTEGER,
    GameType TEXT
);


CREATE TABLE players_tournaments (
    RankText TEXT,
    Prize FLOAT,
    ExchangeRate FLOAT,
    CurrencyCode TEXT,
    TournamentName TEXT,
    EndDate DATE,
    GameId INTEGER,
    Note TEXT,
    TeamPlayers INTEGER,
    PlayerId INTEGER,
    FOREIGN KEY (GameId) REFERENCES games(GameId),
    FOREIGN KEY (PlayerId) REFERENCES players_profiles_with_id(PlayerId)
);

SELECT * FROM GAMES G;
SELECT * FROM PLAYERS_PROFILES; 
SELECT * FROM PLAYERS_TOURNAMENTS PT;
SELECT * FROM TOP_1000_PLAYERS TP;


SELECT
  MIN(EndDate) AS first_tournament,
  MAX(EndDate) AS last_tournament
FROM players_tournaments;

SELECT
  strftime('%Y', EndDate) AS year,
  COUNT(*) AS tournament_count
FROM players_tournaments
GROUP BY year
ORDER BY year;

SELECT
  strftime('%Y', EndDate) AS year,
  ROUND(SUM(Prize * ExchangeRate), 0) AS total_usd_prize
FROM players_tournaments
GROUP BY year
ORDER BY year;

SELECT COUNT(*) FROM players_tournaments WHERE TEAMPLAYERS   IS NULL OR Prize < 0;

SELECT DISTINCT GameId
FROM players_tournaments
WHERE GameId NOT IN (SELECT GameId FROM games);

SELECT GameType, COUNT(*) AS nb_tournois
FROM players_tournaments pt
JOIN games g ON pt.GameId = g.GameId
GROUP BY GameType
ORDER BY nb_tournois DESC;

SELECT p.PlayerName, SUM(pt.Prize * pt.ExchangeRate) AS total_usd
FROM players_tournaments pt
JOIN players_profiles ON pt.PlayerId = p.PlayerId
GROUP BY p.PlayerName
ORDER BY total_usd DESC
LIMIT 10;

SELECT 
    pt.TournamentName, 
    g.GameName,
    (pt.Prize * pt.ExchangeRate) AS total_usd
FROM players_tournaments pt
JOIN games g ON pt.GameId = g.GameId
WHERE (pt.Prize * pt.ExchangeRate) > 500000
ORDER BY total_usd DESC;

SELECT 
    p.CURRENTHANDLE ,
    pt.TournamentName, 
    g.GameName, 
    pt.Prize, 
    pt.ExchangeRate, 
    (pt.Prize * pt.ExchangeRate) AS total_usd
FROM players_tournaments pt
JOIN games g ON pt.GameId = g.GameId
JOIN players_profiles p ON pt.PlayerId = p.PlayerId
WHERE (pt.Prize * pt.ExchangeRate) > 500000
ORDER BY total_usd DESC;

SELECT 
    CASE 
        WHEN pt.TeamPlayers = 1 THEN 'Solo'
        ELSE 'Team'
    END AS format,
    COUNT(*) AS num_tournaments,
    SUM(pt.Prize * pt.ExchangeRate) AS total_prize_usd,
    AVG(pt.Prize * pt.ExchangeRate) AS avg_prize_usd
FROM players_tournaments pt
GROUP BY format
ORDER BY total_prize_usd DESC;

CREATE VIEW player_career_summary AS
SELECT 
    p.PlayerId,
    p.CurrentHandle,
    COUNT(DISTINCT pt.TournamentName) AS num_tournaments,
    COUNT(DISTINCT pt.GameId) AS num_games,
    ROUND(SUM(pt.Prize * pt.ExchangeRate), 2) AS total_prize_usd,
    MIN(pt.EndDate) AS first_tournament,
    MAX(pt.EndDate) AS last_tournament
FROM players_profiles p
JOIN players_tournaments pt ON p.PlayerId = pt.PlayerId
GROUP BY p.PlayerId;

SELECT * FROM player_career_summary;

CREATE VIEW game_format_summary AS
SELECT 
    g.GameName,
    g.GameType,
    CASE WHEN pt.TeamPlayers = 1 THEN 'Solo' ELSE 'Team' END AS format,
    COUNT(*) AS num_tournaments,
    ROUND(SUM(pt.Prize * pt.ExchangeRate), 2) AS total_prize_usd
FROM players_tournaments pt
JOIN games g ON pt.GameId = g.GameId
GROUP BY g.GameName, format;

DROP VIEW IF EXISTS PLAYER_CAREER_SUMMARY;

CREATE VIEW player_career_summary AS
SELECT 
    p.PlayerId,
    p.CurrentHandle AS pseudo,
    TRIM(p.NameFirst || ' ' || p.NameLast) AS real_name,
    COUNT(DISTINCT pt.TournamentName) AS num_tournaments,
    COUNT(DISTINCT pt.GameId) AS num_games,
    ROUND(SUM(pt.Prize * pt.ExchangeRate), 2) AS total_prize_usd,
    MIN(pt.EndDate) AS first_tournament,
    MAX(pt.EndDate) AS last_tournament
FROM players_profiles p
JOIN players_tournaments pt ON p.PlayerId = pt.PlayerId
GROUP BY p.PlayerId;

SELECT * FROM PLAYER_CAREER_SUMMARY PCS
ORDER BY PCS.TOTAL_PRIZE_USD DESC;

CREATE VIEW earnings_by_country as
SELECT 
    p.COUNTRYCODE ,
    COUNT(DISTINCT p.PlayerId) AS num_players,
    COUNT(DISTINCT pt.TournamentName) AS num_tournaments,
    ROUND(SUM(pt.Prize * pt.ExchangeRate), 2) AS total_prize_usd,
    ROUND(SUM(pt.Prize * pt.ExchangeRate) / COUNT(DISTINCT p.PlayerId), 2) AS avg_prize_per_player
FROM players_profiles p
JOIN players_tournaments pt ON p.PlayerId = pt.PlayerId
GROUP BY p.COUNTRYCODE 
ORDER BY total_prize_usd DESC;


SELECT 
    ROUND(SUM(Prize * ExchangeRate), 2) AS global_prizepool
FROM players_tournaments;

SELECT GameId, GameName 
FROM games 
WHERE GameName LIKE '%Dota 2%';

SELECT 
    ROUND(
        100.0 * SUM(CASE WHEN GameId = 231 THEN Prize * ExchangeRate ELSE 0 END) 
        / SUM(Prize * ExchangeRate), 2
    ) AS dota2_percentage_of_total
FROM players_tournaments;

-- Nombre de joueurs uniques ayant joué à Dota 2
SELECT 
    COUNT(DISTINCT PlayerId) * 1.0 / 1000 AS pct_dota2_players,
    COUNT(DISTINCT PlayerId) AS num_dota2_players
FROM players_tournaments
WHERE GameId = 231;

SELECT * FROM PLAYER_CAREER_SUMMARY PCS 
ORDER BY TOTAL_PRIZE_USD DESC

SELECT * FROM GAMES G 
WHERE G.TOTALTOURNAMENTS > 100;

SELECT * FROM GAMES G 
WHERE G.TOTALTOURNAMENTS > 100;

