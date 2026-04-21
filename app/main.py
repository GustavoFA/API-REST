from fastapi import FastAPI
from app.data_loader import load_data, clean_data, get_daily_sales, get_summary
from app.schemas import HealthResponse, SummaryResponse, DailySalesItem
from typing import List

app = FastAPI(title="E-commerce Revenue Forecast API")

df = clean_data(load_data())

@app.get("/health", response_model=HealthResponse)
def health():
    """Checking if API is running."""
    return {"status": "ok"}

@app.get("/summary", response_model=SummaryResponse)
def summary():
    """Return the dataset summary."""
    return get_summary(df)

@app.get("/sales/daily", response_model=List[DailySalesItem])
def sales_daily():
    """Get the aggregaded daily revenue and convert each row into dictionaries."""
    daily = get_daily_sales(df)
    return [
        {'date': str(row['Date']), 'revenue': float(row['revenue'])}
        for _, row in daily.iterrows()
    ]