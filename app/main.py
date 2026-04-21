from fastapi import FastAPI
from app.data_loader import *

app = FastAPI(title="E-commerce Revenue Forecast API")

df = clean_data(load_data())

@app.get("/health")
def health():
    """Checking if API is running."""
    return {"status": "ok"}

@app.get("/summary")
def summary():
    """Return the dataset summary."""
    return get_summary(df)

@app.get("/sales/daily")
def sales_daily():
    """Get the aggregaded daily revenue and convert each row into dictionaries."""
    daily = get_daily_sales(df)
    return [
        {'date': str(row['Date']), 'revenue': float(row['revenue'])}
        for _, row in daily.iterrows()
    ]