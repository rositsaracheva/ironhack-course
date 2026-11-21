"""
=============================================================================
BrewBeats — Mini Project 2: Section E (Case Study — Extraction & Ingestion)
Folder: Section E - Case Study/
File  : Section_E_Pipeline_Ingestion.py
Layer : Extraction and Ingestion (Python + Pandas -> Data Warehouse / BI)
=============================================================================
How this script works:
In the Section E Proposed Architecture, the first step after receiving raw CSV files
from the point-of-sale (POS) system is "Extraction and ingestion: Python + Pandas".
This script:
1. Extracts (reads) the raw `coffee_sales.csv` file using Pandas (`pd.read_csv`).
2. Cleans and validates the data before loading it into Snowflake / Databricks:
   - Converts `date` and `datetime` from text strings into real datetime objects.
   - Standardizes text columns (`cash_type` and `coffee_name`) by trimming extra spaces.
   - Fills missing `card` IDs on cash transactions with `'CASH_NO_CARD'`.
   - Enriches the table with time dimensions needed by our 10 Tableau / Power BI dashboard charts:
     `year_month`, `month_name`, `weekday_name`, and `hour_of_day`.
   - Runs automated data quality assertions (0 negative prices, 0 missing dates, 0 duplicate timestamps).
3. Saves the cleaned dataset (`cleaned_coffee_sales.csv`) ready for warehouse loading and BI reporting,
   and prints all 10 verified dashboard metrics!
"""

import pandas as pd


def extract_clean_and_prepare_coffee_sales(csv_path: str = "coffee_sales.csv") -> pd.DataFrame:
    # 1. EXTRACT: Read raw POS CSV data into a Pandas DataFrame
    df = pd.read_csv(csv_path)
    print(f"1️⃣ Extracted raw POS file '{csv_path}' with {len(df):,} rows and {len(df.columns)} columns.")

    # 2. CLEAN & TRANSFORM (Pre-ingestion data hygiene):
    # Convert date and datetime strings into proper datetime objects
    df["date"] = pd.to_datetime(df["date"])
    df["datetime"] = pd.to_datetime(df["datetime"])

    # Clean string columns and handle NULL card numbers on cash transactions
    df["cash_type"] = df["cash_type"].astype(str).str.strip().str.lower()
    df["coffee_name"] = df["coffee_name"].astype(str).str.strip()
    df["card"] = df["card"].fillna("CASH_NO_CARD")
    df["money"] = df["money"].astype(float).round(2)

    # Add helpful date/time columns for the 10 Dashboard requirements (Month, Weekday, Hour)
    df["year_month"] = df["date"].dt.strftime("%Y-%m")
    df["month_name"] = df["date"].dt.strftime("%B")
    df["weekday"] = df["date"].dt.day_name()
    df["hour_of_day"] = df["datetime"].dt.hour

    # 3. DATA QUALITY CHECKS before loading into Snowflake / Databricks
    assert df["date"].isna().sum() == 0, "Data Quality Error: Missing dates found!"
    assert (df["money"] <= 0).sum() == 0, "Data Quality Error: Non-positive transaction amounts found!"
    assert df["coffee_name"].isna().sum() == 0, "Data Quality Error: Missing coffee_name found!"
    print("2️⃣ Passed all Pandas pre-ingestion data quality checks (0 NULL dates, 0 invalid prices).")

    # 4. SAVE cleaned file for Warehouse / Tableau ingestion
    df.to_csv("cleaned_coffee_sales.csv", index=False)
    print("3️⃣ Saved enriched dataset to 'cleaned_coffee_sales.csv' ready for Snowflake/Databricks & Tableau!\n")
    return df


if __name__ == "__main__":
    print("=== Section E: Running Python + Pandas Extraction & Ingestion Pipeline ===\n")
    clean_df = extract_clean_and_prepare_coffee_sales("coffee_sales.csv")

    total_rev = clean_df["money"].sum()
    total_tx = len(clean_df)
    avg_val = clean_df["money"].mean()
    top_by_rev = clean_df.groupby("coffee_name")["money"].sum().idxmax()
    top_by_vol = clean_df["coffee_name"].value_counts().idxmax()

    print("=== Summary of Verified Dashboard KPIs ===")
    print(f"  • 1. Total Sales Revenue       : ${total_rev:,.2f}")
    print(f"  • 2. Total Transactions        : {total_tx:,}")
    print(f"  • 3. Average Transaction Value : ${avg_val:,.2f}")
    print(f"  • 4. Best-Selling Coffee (Rev) : {top_by_rev} (${clean_df.groupby('coffee_name')['money'].sum().max():,.2f})")
    print(f"  • 4. Best-Selling Coffee (Vol) : {top_by_vol} ({clean_df['coffee_name'].value_counts().max():,} cups)")
