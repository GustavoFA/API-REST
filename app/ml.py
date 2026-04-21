import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

from app.data_loader import load_data, clean_data, get_daily_sales

def create_lag_features(daily_df: pd.DataFrame, n_lags: int = 3) -> pd.DataFrame:
    """
    Create lag features from the daily revenue series.

    Input columns expected:
    - Date
    - Revenue
    """
    df = daily_df.copy()

    for lag in range(1, n_lags + 1):
        df[f"lag_{lag}"] = df["revenue"].shift(lag)

    df = df.dropna().reset_index(drop=True)
    
    return df

def train_forecast_model(feature_df: pd.DataFrame) -> dict:
    """
    Train a Linear Regression model using lag features.

    Returns:
    - trained model
    - evaluation metrics
    - number of lags used
    """
    features_column = [col for col in feature_df.columns if col.startswith("lag_")]

    X = feature_df[features_column]
    y = feature_df["revenue"]

    model = LinearRegression()
    model.fit(X, y)

    predictions = model.predict(X)

    mae = mean_absolute_error(y, predictions)
    rmse = root_mean_squared_error(y, predictions)

    return {
        'model': model,
        'mae': float(mae),
        'rmse': float(rmse),
        'n_lags': len(features_column),
        'features_columns': features_column
    }

def forecast_next_days(
    model,
    revenue_series: pd.Series,
    days: int = 7,
    n_lags: int = 3
) -> list[float]:
    """
    Forecast the next `days` values recursively.

    Parameters:
    - model: trained scikit-learn model
    - revenue_series: historical daily revenue series
    - days: number of future days to forecast
    - n_lags: number of lag features used

    Returns:
    - list of predicted revenues
    """
    history = list(revenue_series.astype(float).values)
    forecasts = []

    for _ in range(days):
        last_values = history[-n_lags:]
        input_data = pd.DataFrame(
            [[last_values[-1], last_values[-2], last_values[-3]]],
            columns=[f"lag_{i}" for i in range(1, n_lags + 1)]
        )

        prediction = float(model.predict(input_data)[0])
        forecasts.append(prediction)
        history.append(prediction)

    return forecasts

if __name__ == "__main__":

    df = clean_data(load_data())
    daily = get_daily_sales(df)

    feature_df = create_lag_features(daily, n_lags=3)
    print("FEATURE DATA:")
    print(feature_df.head())

    results = train_forecast_model(feature_df)
    print("\nTRAIN RESULTS:")
    print({
        "mae": results["mae"],
        "rmse": results["rmse"],
        "n_lags": results["n_lags"],
    })

    forecasts = forecast_next_days(
        model=results["model"],
        revenue_series=daily["revenue"],
        days=7,
        n_lags=3
    )
    print("\nNEXT 7 DAYS FORECAST:")
    print(forecasts)