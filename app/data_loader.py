import pandas as pd
from pathlib import Path
# from typing import Dict

DATA_PATH = Path('./data/data.csv')

def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH, encoding='ISO-8859-1')


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the E-commerce dataset."""
    df = df.dropna(subset=['InvoiceDate'])
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
    df = df.dropna(subset=['InvoiceDate'])

    df = df.dropna(subset=['Quantity', 'UnitPrice'])
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)].copy()

    df = create_revenue(df)
    df['Date'] = df['InvoiceDate'].dt.date

    return df

def create_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Create the column revenue."""
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    return df

def get_daily_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate total revenue by day."""
    daily = (
        df.groupby('Date', as_index=False)['Revenue']
        .sum()
        .sort_values('Date')
        .rename(columns={'Revenue': 'revenue'})
    )
    return daily

def get_summary(df: pd.DataFrame) -> dict:
    """Return a simple dataset summary."""
    return {
        'transactions': int(len(df)),
        'start_date': str(df['Date'].min()),
        'end_date': str(df['Date'].max()),
        'countries': int(df['Country'].nunique()) if 'Country' in df.columns else 0,
        'total_revenue': float(df['Revenue'].sum())
    }

if __name__ == "__main__":
    df = load_data()
    df = clean_data(df)

    print("COLUMNS:")
    print(df.columns)

    print("\nFIRST 5 ROWS:")
    print(df.head())

    print("\nSUMMARY:")
    print(get_summary(df))

    print("\nDAILY SALES:")
    print(get_daily_sales(df).head())