-- 1. Create Database, Schema, and Warehouse
CREATE DATABASE IF NOT EXISTS spotify_db;
CREATE SCHEMA IF NOT EXISTS spotify_db.music;
CREATE WAREHOUSE IF NOT EXISTS spotify_wh WAREHOUSE_SIZE = 'XSMALL' AUTO_SUSPEND = 60 AUTO_RESUME = TRUE;
USE WAREHOUSE spotify_wh;
USE SCHEMA spotify_db.music;
-- 2. Create the CSV File Format
CREATE
OR REPLACE FILE FORMAT spotify_csv_ff TYPE = CSV SKIP_HEADER = 1 FIELD_OPTIONALLY_ENCLOSED_BY = '"' ESCAPE_UNENCLOSED_FIELD = NONE NULL_IF = ('');
-- 3. Create the spotify_songs Table (17 columns matching the CSV)
CREATE
OR REPLACE TABLE spotify_songs (
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
-- 4. Create the Stage to upload the CSV file
-- CREATE OR REPLACE STAGE spotify_stage FILE_FORMAT = spotify_csv_ff;
-- 5. Copy the uploaded CSV into the spotify_songs table
COPY INTO spotify_songs
FROM
    @spotify_stage ON_ERROR = 'CONTINUE';
    -- Q1. Which is the longest song released yet?
SELECT
    song_title,
    artist,
    duration_ms,
    ROUND(duration_ms / 60000, 2) AS duration_minutes
FROM
    spotify_songs
ORDER BY
    duration_ms DESC
LIMIT
    1;
    -- Q2. How many songs has Drake sung?
SELECT
    COUNT(*) AS drake_songs
FROM
    spotify_songs
WHERE
    artist = 'Drake';
    -- Q3. List those songs with 'Love' in them.
SELECT
    song_title,
    artist
FROM
    spotify_songs
WHERE
    song_title ILIKE '%Love%';
    -- Q4. Select songs which have a number in them.
SELECT
    song_title,
    artist
FROM
    spotify_songs
WHERE
    REGEXP_LIKE(song_title, '.*[0-9].*');
    -- Q5. You have a bachelorette weekend, which songs would you play the most?
SELECT
    song_title,
    artist,
    danceability,
    energy,
    valence
FROM
    spotify_songs
WHERE
    danceability > 0.8
    AND energy > 0.8
    AND valence > 0.75
ORDER BY
    danceability DESC,
    energy DESC
LIMIT
    10;
    -- Q6. In a dance battle, which 3 songs would you choose for a dance off?
SELECT
    song_title,
    artist,
    danceability,
    energy,
    tempo
FROM
    spotify_songs
ORDER BY
    danceability DESC,
    energy DESC,
    tempo DESC
LIMIT
    3;
    -- Q7. Which artist has the max songs released?
SELECT
    artist,
    COUNT(*) AS total_songs
FROM
    spotify_songs
GROUP BY
    artist
ORDER BY
    total_songs DESC
LIMIT
    1;
    -- Q8. Make a 'break-up' song list >..<
SELECT
    song_title,
    artist,
    valence,
    energy,
    acousticness
FROM
    spotify_songs
WHERE
    valence < 0.25
    AND energy < 0.4
    AND acousticness > 0.7
    AND instrumentalness < 0.5
ORDER BY
    valence ASC
LIMIT
    10;