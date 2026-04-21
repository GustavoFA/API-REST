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