-- ============================================================================
-- BrewBeats — Mini Project 2: Section C (Snowflake SQL & Snowpark)
-- File  : Section_C_Q4.sql
-- Folder: Section C - Snowflake SQL & Snowpark/
-- Table : brewbeats_db.music.spotify_songs
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Section C - Q4: Write a query to find the top 3 songs by Drake.
-- ----------------------------------------------------------------------------
-- How I calculate this in Snowflake SQL:
-- 1. USE WAREHOUSE / DATABASE / SCHEMA: sets our active Snowflake context to brewbeats_db.music.
-- 2. SELECT song_title, artist, danceability, energy, valence, tempo: picks the song details
--    and main audio features from our spotify_songs table.
-- 3. WHERE artist = 'Drake': filters the 2,017 songs to keep only tracks performed by Drake (16 songs).
-- 4. ORDER BY danceability DESC, energy DESC: ranks Drake's songs from highest danceability and energy
--    to lowest (ideal for BrewBeats' in-store coffee kiosk playlists).
-- 5. LIMIT 3: keeps only the top 3 songs by Drake.

USE WAREHOUSE brewbeats_wh;
USE DATABASE brewbeats_db;
USE SCHEMA brewbeats_db.music;

SELECT
    song_title,
    artist,
    danceability,
    energy,
    valence,
    tempo
FROM spotify_songs
WHERE artist = 'Drake'
ORDER BY danceability DESC, energy DESC
LIMIT 3;

/*
Verified Output (Section C - Q4):
+-----------------+--------+--------------+--------+---------+---------+
| SONG_TITLE      | ARTIST | DANCEABILITY | ENERGY | VALENCE | TEMPO   |
+-----------------+--------+--------------+--------+---------+---------+
| Hotline Bling   | Drake  |        0.896 |  0.623 |   0.564 | 134.962 |
| Jumpman         | Drake  |        0.853 |  0.547 |   0.677 | 142.065 |
| Wu-Tang Forever | Drake  |        0.849 |  0.408 |   0.337 |  99.876 |
+-----------------+--------+--------------+--------+---------+---------+
*/
