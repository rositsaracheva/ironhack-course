"""
QuickCart Data Engineering Pipeline
Section C: Python + Pandas Engineering
- Q1: Data Ingestion & Schema Validation
- Q2: Data Cleaning & Transformation
- Q3: Clickstream Analytics
"""

import os
import pandas as pd
import numpy as np

# Define Base Data Directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw") if os.path.exists(os.path.join(DATA_DIR, "raw")) else DATA_DIR
CLEANED_DIR = os.path.join(DATA_DIR, "cleaned")
os.makedirs(CLEANED_DIR, exist_ok=True)


# =====================================================================
# Q1. DATA INGESTION & VALIDATION PIPELINE
# =====================================================================

def load_datasets():
    """Reads all 4 datasets from the raw data folder."""
    print("=" * 60)
    print("STEP 1: INGESTING DATASETS FROM RAW FOLDER")
    print("=" * 60)
    
    customers = pd.read_csv(os.path.join(RAW_DIR, "customers.csv"))
    orders = pd.read_csv(os.path.join(RAW_DIR, "orders.csv"))
    products = pd.read_csv(os.path.join(RAW_DIR, "products.csv"))
    clickstream = pd.read_csv(os.path.join(RAW_DIR, "clickstream.csv"))
    
    print(f" Loaded Customers  : {len(customers):,} rows")
    print(f" Loaded Orders     : {len(orders):,} rows")
    print(f" Loaded Products   : {len(products):,} rows")
    print(f" Loaded Clickstream: {len(clickstream):,} rows")
    
    return customers, orders, products, clickstream


def validate_schemas(customers, orders, products, clickstream):
    """Validates presence of required columns and schema consistency."""
    print("\n" + "=" * 60)
    print("STEP 2: VALIDATING SCHEMAS")
    print("=" * 60)
    
    expected_schemas = {
        "customers": ["customer_id", "customer_name", "email", "city", "signup_date"],
        "orders": ["order_id", "customer_id", "product_id", "order_date", "quantity", "unit_price", "payment_status"],
        "products": ["product_id", "product_name", "category", "supplier_id", "cost_price", "selling_price"],
        "clickstream": ["event_id", "customer_id", "event_type", "page_url", "event_timestamp", "device_type"]
    }
    
    dfs = {
        "customers": customers,
        "orders": orders,
        "products": products,
        "clickstream": clickstream
    }
    
    all_valid = True
    for name, df in dfs.items():
        missing_cols = set(expected_schemas[name]) - set(df.columns)
        if missing_cols:
            print(f"❌ {name.upper()}: Missing columns {missing_cols}")
            all_valid = False
        else:
            print(f"✅ {name.upper()}: Schema consistent ({len(df.columns)} columns present)")
            
    return all_valid


def detect_duplicates_and_invalid(customers, orders, products, clickstream):
    """Detects duplicate customers and invalid records across datasets."""
    print("\n" + "=" * 60)
    print("STEP 3: DETECTING DUPLICATES & INVALID RECORDS")
    print("=" * 60)
    
    # 1. Duplicate Customers
    dup_id = customers.duplicated(subset=['customer_id']).sum()
    dup_email = customers.duplicated(subset=['email']).sum()
    print(f"• Customers duplicate IDs   : {dup_id}")
    print(f"• Customers duplicate Emails : {dup_email}")
    
    # 2. Invalid Orders
    inv_qty = (orders['quantity'] <= 0).sum()
    inv_price = (orders['unit_price'] <= 0).sum()
    orphan_cust_orders = (~orders['customer_id'].isin(customers['customer_id'])).sum()
    orphan_prod_orders = (~orders['product_id'].isin(products['product_id'])).sum()
    
    print(f"• Orders with quantity <= 0 : {inv_qty}")
    print(f"• Orders with price <= 0    : {inv_price}")
    print(f"• Orders with invalid customer_id: {orphan_cust_orders}")
    print(f"• Orders with invalid product_id : {orphan_prod_orders}")
    
    # 3. Clickstream Missing / Corrupted Values
    null_cust_clicks = clickstream['customer_id'].isnull().sum()
    null_page_clicks = clickstream['page_url'].isnull().sum()
    null_device_clicks = clickstream['device_type'].isnull().sum()
    
    print(f"• Clickstream missing customer_id: {null_cust_clicks} (anonymous visitors)")
    print(f"• Clickstream missing page_url   : {null_page_clicks}")
    print(f"• Clickstream missing device_type: {null_device_clicks}")


# =====================================================================
# Q2. DATA CLEANING & TRANSFORMATION
# =====================================================================

def clean_customers(customers):
    """Standardizes customer names, emails, and city names."""
    df = customers.copy()
    df['customer_name'] = df['customer_name'].astype(str).str.strip().str.title()
    df['email'] = df['email'].astype(str).str.strip().str.lower()
    df['city'] = df['city'].astype(str).str.strip().str.title()
    df['signup_date'] = pd.to_datetime(df['signup_date'], errors='coerce')
    return df


def clean_orders(orders):
    """Cleans and standardizes orders."""
    df = orders.copy()
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df['payment_status'] = df['payment_status'].astype(str).str.strip().str.title()
    return df


def clean_clickstream(clickstream):
    """
    Cleans clickstream events:
    - Standardizes timestamps with mixed formats and timezones (UTC).
    - Cleans and standardizes misspelled event types ('clik' -> 'click', 'serach' -> 'search').
    - Standardizes device types (Title Case: Mobile, Desktop, Tablet).
    - Handles missing values.
    """
    df = clickstream.copy()
    
    # 1. Parse mixed timestamps (ISO with Z, DD/MM/YYYY, etc.) to UTC
    df['event_timestamp'] = pd.to_datetime(df['event_timestamp'], format='mixed', utc=True)
    
    # 2. Standardize event types
    df['event_type'] = (
        df['event_type']
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(' ', '_')
        .str.replace('-', '_')
    )
    # Fix common misspellings found in logs
    event_replacements = {
        'clik': 'click',
        'serach': 'search',
        'pageview': 'page_view'
    }
    df['event_type'] = df['event_type'].replace(event_replacements)
    
    # 3. Standardize device types
    df['device_type'] = df['device_type'].astype(str).str.strip().str.title()
    df['device_type'] = df['device_type'].replace({'Nan': np.nan, 'None': np.nan})
    
    # Fill missing device type with 'Unknown' for analytics
    df['device_type_imputed'] = df['device_type'].fillna('Unknown')
    
    # 4. Standardize page_url
    df['page_url'] = df['page_url'].astype(str).str.strip()
    df['page_url'] = df['page_url'].replace({'nan': np.nan, '': np.nan})
    
    # 5. Customer ID (keep integer for known users, -1 for anonymous)
    df['customer_id_clean'] = df['customer_id'].fillna(-1).astype(int)
    
    return df


# =====================================================================
# Q3. CLICKSTREAM ANALYTICS
# =====================================================================

def analyze_clickstream(clean_clicks):
    """Computes required clickstream metrics."""
    print("\n" + "=" * 60)
    print("STEP 4: CLICKSTREAM ANALYTICS")
    print("=" * 60)
    
    # 1. Most Visited Pages
    print("\n📌 1. TOP 5 MOST VISITED PAGES:")
    page_visits = clean_clicks['page_url'].dropna().value_counts().head(5)
    for rank, (url, count) in enumerate(page_visits.items(), 1):
        print(f"   {rank}. {url:<16} : {count:,} visits")
        
    # 2. Calculate Session Counts (30-minute inactivity threshold per customer)
    print("\n📌 2. SESSION COUNTS CALCULATION:")
    known_users = clean_clicks[clean_clicks['customer_id_clean'] != -1].copy()
    known_users = known_users.sort_values(by=['customer_id_clean', 'event_timestamp'])
    
    # If gap between events is > 30 minutes, it's a new session
    time_diff = known_users.groupby('customer_id_clean')['event_timestamp'].diff()
    is_new_session = (time_diff > pd.Timedelta(minutes=30)) | (time_diff.isnull())
    known_users['session_id'] = is_new_session.cumsum()
    
    total_sessions = known_users['session_id'].nunique()
    print(f"   • Total distinct user sessions (30-min window): {total_sessions:,}")
    print(f"   • Total registered users with activity        : {known_users['customer_id_clean'].nunique():,}")
    print(f"   • Average events per session                 : {len(known_users) / total_sessions:.2f}")

    # 3. Mobile vs Desktop Traffic Percentage
    print("\n📌 3. DEVICE TRAFFIC DISTRIBUTION:")
    device_counts = clean_clicks['device_type'].dropna().value_counts()
    device_pct = (clean_clicks['device_type'].dropna().value_counts(normalize=True) * 100).round(2)
    
    for device, pct in device_pct.items():
        print(f"   • {device:<10} : {pct:>5.2f}% ({device_counts[device]:,} events)")
        
    # Direct comparison: Mobile vs Desktop only (excluding Tablets)
    mob_desk = clean_clicks[clean_clicks['device_type'].isin(['Mobile', 'Desktop'])]
    mob_desk_pct = (mob_desk['device_type'].value_counts(normalize=True) * 100).round(2)
    print("\n   🎯 Mobile vs. Desktop Direct Comparison (Excluding Tablets):")
    print(f"   • Mobile  : {mob_desk_pct.get('Mobile', 0):.2f}%")
    print(f"   • Desktop : {mob_desk_pct.get('Desktop', 0):.2f}%")


# =====================================================================
# MAIN PIPELINE EXECUTION
# =====================================================================

def main():
    # 1. Ingestion & Validation
    customers, orders, products, clickstream = load_datasets()
    validate_schemas(customers, orders, products, clickstream)
    detect_duplicates_and_invalid(customers, orders, products, clickstream)
    
    # 2. Cleaning & Transformation
    print("\n" + "=" * 60)
    print("STEP 5: CLEANING & TRANSFORMING DATASETS")
    print("=" * 60)
    clean_cust = clean_customers(customers)
    clean_ord = clean_orders(orders)
    clean_clk = clean_clickstream(clickstream)
    
    # Save cleaned files for downstream SQL & Airflow
    clean_cust.to_csv(os.path.join(CLEANED_DIR, "clean_customers.csv"), index=False)
    clean_ord.to_csv(os.path.join(CLEANED_DIR, "clean_orders.csv"), index=False)
    products.to_csv(os.path.join(CLEANED_DIR, "clean_products.csv"), index=False)
    clean_clk.to_csv(os.path.join(CLEANED_DIR, "clean_clickstream.csv"), index=False)
    print(" Cleaned files saved to data/cleaned/ folder!")
    
    # 3. Clickstream Analytics
    analyze_clickstream(clean_clk)
    print("\n" + "=" * 60)
    print("🎉 SECTION C PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    main()
