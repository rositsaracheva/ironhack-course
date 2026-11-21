-- ============================================================================
-- BrewBeats — Mini Project 2: Section C (Snowflake SQL & Snowpark)
-- File  : Section_C_Q3.sql
-- Folder: Section C - Snowflake SQL & Snowpark/
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Section C - Q3: Write the SQL to create a stage and load spotify.csv into a Snowflake table.
-- ----------------------------------------------------------------------------
-- How I do this step by step in Snowflake:
-- 1. Create a 'music' schema inside our brewbeats_db database (brewbeats_db.music) and set it as active.
-- 2. CREATE OR REPLACE FILE FORMAT spotify_csv_ff: tells Snowflake how to read our Spotify CSV file:
--      * TYPE = 'CSV', SKIP_HEADER = 1 (skips the first row of column names)
--      * FIELD_OPTIONALLY_ENCLOSED_BY = '"' (very important because 56 song titles/artists have commas inside quotes!)
--      * ESCAPE_UNENCLOSED_FIELD = NONE
-- 3. CREATE OR REPLACE TABLE spotify_songs: creates the destination Snowflake table with all 17 columns
--    matching Spotify_data.csv (song_id, acousticness, danceability, duration_ms, energy, instrumentalness,
--    key, liveness, loudness, mode, speechiness, tempo, time_signature, valence, target, song_title, artist).
-- 4. CREATE OR REPLACE STAGE spotify_stage: creates the internal Snowflake stage (@spotify_stage) where
--    the Spotify CSV file is uploaded.
-- 5. COPY INTO spotify_songs FROM @spotify_stage: loads the 2,017 rows from @spotify_stage into our
--    spotify_songs table.

-- Step 1: Set up the music schema in our BrewBeats database
CREATE DATABASE IF NOT EXISTS brewbeats_db;
CREATE SCHEMA IF NOT EXISTS brewbeats_db.music;
CREATE WAREHOUSE IF NOT EXISTS brewbeats_wh
    WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE;

USE WAREHOUSE brewbeats_wh;
USE DATABASE brewbeats_db;
USE SCHEMA brewbeats_db.music;

-- Step 2: Create the CSV File Format (handling quoted song titles & artists with commas)
CREATE OR REPLACE FILE FORMAT spotify_csv_ff
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    ESCAPE_UNENCLOSED_FIELD = NONE
    NULL_IF = ('', 'NULL');

-- Step 3: Create the spotify_songs Snowflake table (17 columns matching Spotify_data.csv)
CREATE OR REPLACE TABLE spotify_songs (
    song_id INT,
    acousticness FLOAT,
    danceability FLOAT,
    duration_ms INT,
    energy FLOAT,
    instrumentalness FLOAT,
    key INT,
    liveness FLOAT,
    loudness FLOAT,
    mode INT,
    speechiness FLOAT,
    tempo FLOAT,
    time_signature INT,
    valence FLOAT,
    target INT,
    song_title STRING,
    artist STRING
);

-- Step 4: Create the Internal Stage using our CSV File Format
-- (Upload Spotify_data.csv / spotify.csv to @spotify_stage via Snowsight UI or PUT file://Spotify_data.csv @spotify_stage)
CREATE OR REPLACE STAGE spotify_stage
    FILE_FORMAT = spotify_csv_ff;

-- Step 5: Load the uploaded Spotify CSV from @spotify_stage into the spotify_songs table
COPY INTO spotify_songs
FROM @spotify_stage
FILE_FORMAT = (FORMAT_NAME = 'spotify_csv_ff')
ON_ERROR = 'CONTINUE';

-- Step 6: Verify the loaded data (2,017 songs)
SELECT COUNT(*) AS total_songs_loaded FROM spotify_songs;
SELECT song_id, song_title, artist, danceability, energy, valence, tempo
FROM spotify_songs
LIMIT 5;

/*
Verified Output (Section C - Q3):
TOTAL_SONGS_LOADED: 2017

+---------+----------------+------------------+--------------+--------+---------+---------+
| SONG_ID | SONG_TITLE     | ARTIST           | DANCEABILITY | ENERGY | VALENCE | TEMPO   |
+---------+----------------+------------------+--------------+--------+---------+---------+
|       0 | Mask Off       | Future           |        0.833 |  0.434 |   0.286 | 150.062 |
|       1 | Redbone        | Childish Gambino |        0.743 |  0.359 |   0.588 | 160.083 |
|       2 | Xanny Family   | Future           |        0.838 |  0.412 |   0.173 |  75.044 |
|       3 | Master Of None | Beach House      |        0.494 |  0.338 |   0.230 |  86.468 |
|       4 | Parallel Lines | Junior Boys      |        0.678 |  0.561 |   0.904 | 174.004 |
+---------+----------------+------------------+--------------+--------+---------+---------+
*/
