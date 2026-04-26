from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str

class SummaryResponse(BaseModel):
    transactions: int
    start_date: str
    end_date: str
    countries: int
    total_revenue: float

class DailySalesItem(BaseModel):
    date: str
    revenue: float

class TrainResponse(BaseModel):
    model_name: str
    mae: float
    rmse: float
    n_lags: int

class ForecastItem(BaseModel):
    date: str
    predicted_revenue: float