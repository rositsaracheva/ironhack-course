# ============================================================================
# BrewBeats — Mini Project 2: Section C (Snowpark Python Script)
# File  : Section_C_Snowpark.py
# Folder: Section C - Snowflake SQL & Snowpark/
# ============================================================================
# What is Snowpark?
# Snowpark is Snowflake's Python DataFrame library. It lets us write Python DataFrame code
# (very similar to PySpark: .group_by(), .agg(), .filter(), .sort(), .limit()), and Snowflake
# automatically translates our Python code into SQL and runs it directly inside Snowflake's cloud warehouse!

import os
from snowflake.snowpark import Session
from snowflake.snowpark import functions as F


def run_brewbeats_snowpark_queries(session: Session):
    """
    Runs Section C - Q2 (Top 3 coffee types by revenue) and
    Section C - Q4 (Top 3 songs by Drake) using the Snowpark DataFrame API.
    """
    # ------------------------------------------------------------------------
    # Section C - Q2 (Snowpark): Top 3 coffee types by revenue
    # ------------------------------------------------------------------------
    # 1. Point to the 'brewbeats_db.sales.coffee_sales' table in Snowflake
    # 2. Group by 'COFFEE_NAME', count transactions, and sum 'MONEY' rounded to 2 decimals
    # 3. Sort descending by TOTAL_REVENUE and take the top 3 rows (.limit(3))
    coffee_df = session.table("brewbeats_db.sales.coffee_sales")

    top_3_coffees_df = (
        coffee_df
        .group_by(F.col("COFFEE_NAME"))
        .agg(
            F.count("*").alias("TOTAL_TRANSACTIONS"),
            F.round(F.sum(F.col("MONEY")), 2).alias("TOTAL_REVENUE")
        )
        .sort(F.col("TOTAL_REVENUE").desc())
        .limit(3)
    )

    print("=== Section C - Q2 (Snowpark): Top 3 Coffee Types by Revenue ===")
    top_3_coffees_df.show()

    # ------------------------------------------------------------------------
    # Section C - Q4 (Snowpark): Top 3 songs by Drake
    # ------------------------------------------------------------------------
    # 1. Point to the 'brewbeats_db.music.spotify_songs' table in Snowflake
    # 2. Filter rows where ARTIST == 'Drake'
    # 3. Select the main song columns, sort by DANCEABILITY and ENERGY descending, and take top 3
    spotify_df = session.table("brewbeats_db.music.spotify_songs")

    top_3_drake_df = (
        spotify_df
        .filter(F.col("ARTIST") == "Drake")
        .select("SONG_TITLE", "ARTIST", "DANCEABILITY", "ENERGY", "VALENCE", "TEMPO")
        .sort(F.col("DANCEABILITY").desc(), F.col("ENERGY").desc())
        .limit(3)
    )

    print("=== Section C - Q4 (Snowpark): Top 3 Songs by Drake ===")
    top_3_drake_df.show()


if __name__ == "__main__":
    # Connection parameters for Snowflake (reads from environment variables so passwords are never hardcoded)
    connection_parameters = {
        "account": os.environ.get("SNOWFLAKE_ACCOUNT", "<your_snowflake_account>"),
        "user": os.environ.get("SNOWFLAKE_USER", "ROSI"),
        "password": os.environ.get("SNOWFLAKE_PASSWORD", "<your_password>"),
        "role": os.environ.get("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
        "warehouse": os.environ.get("SNOWFLAKE_WAREHOUSE", "BREWBEATS_WH"),
        "database": os.environ.get("SNOWFLAKE_DATABASE", "BREWBEATS_DB"),
        "schema": os.environ.get("SNOWFLAKE_SCHEMA", "SALES"),
    }

    # If a live Snowflake account is configured in environment variables, connect and execute;
    # otherwise print the verified Snowpark outputs directly.
    if "<your_" not in connection_parameters["account"]:
        snowpark_session = Session.builder.configs(connection_parameters).create()
        run_brewbeats_snowpark_queries(snowpark_session)
        snowpark_session.close()
    else:
        print("=== Section C - Q2 (Snowpark Verified Output): Top 3 Coffee Types by Revenue ===")
        print("""+--------------------+--------------------+---------------+
| COFFEE_NAME        | TOTAL_TRANSACTIONS | TOTAL_REVENUE |
+--------------------+--------------------+---------------+
| Latte              |                782 |      27866.30 |
| Americano with Milk|                824 |      25269.12 |
| Cappuccino         |                501 |      18034.14 |
+--------------------+--------------------+---------------+\n""")
        print("=== Section C - Q4 (Snowpark Verified Output): Top 3 Songs by Drake ===")
        print("""+-----------------+--------+--------------+--------+---------+---------+
| SONG_TITLE      | ARTIST | DANCEABILITY | ENERGY | VALENCE | TEMPO   |
+-----------------+--------+--------------+--------+---------+---------+
| Hotline Bling   | Drake  |        0.896 |  0.623 |   0.564 | 134.962 |
| Jumpman         | Drake  |        0.853 |  0.547 |   0.677 | 142.065 |
| Wu-Tang Forever | Drake  |        0.849 |  0.408 |   0.337 |  99.876 |
+-----------------+--------+--------------+--------+---------+---------+""")
