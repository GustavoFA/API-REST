from fastapi import FastAPI, HTTPException
from datetime import timedelta
from app.ml import create_lag_features, train_forecast_model, forecast_next_days
from app.data_loader import load_data, clean_data, get_daily_sales, get_summary
from app.schemas import HealthResponse, SummaryResponse, DailySalesItem, TrainResponse, ForecastItem
from typing import List

app = FastAPI(title="E-commerce Revenue Forecast API")

df = clean_data(load_data())
daily_df = get_daily_sales(df)

trained_model = None
trained_n_lags = 3

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

@app.post("/train", response_model=TrainResponse)
def train():
    global trained_model, trained_n_lags

    features_df = create_lag_features(daily_df, n_lags=trained_n_lags)
    results = train_forecast_model(features_df)

    trained_model = results['model']

    return {
        "model_name": "Linear Regression",
        "mae": results["mae"],
        "rmse": results["rmse"],
        "n_lags": results["n_lags"],
    }

@app.get("/forecast", response_model=list[ForecastItem])
def forecast(days: int = 7):
    if trained_model is None:
        raise HTTPException(
            status_code=400,
            detail="Model not trained yet. Call POST /train first."
        )
    
    forecast_values = forecast_next_days(
        model=trained_model,
        revenue_series=daily_df["revenue"],
        days=days,
        n_lags=trained_n_lags,
    )

    last_date = daily_df["Date"].max()

    results = []
    for i, value in enumerate(forecast_values, start=1):
        future_date = last_date + timedelta(days=i)
        results.append({
            "date": str(future_date),
            "predicted_revenue": float(value)
        })
    
    return results