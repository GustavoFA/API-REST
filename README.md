# API REST 

## Dataset

I'm using a ecommerce dataset from Kaggle. To download the dataset use ```download_data.sh```.

## FastAPI

```curl -X POST -H "Content-Type: application/json" 'http://127.0.0.1:8000/items?item=ok'``` 

```curl -X GET http://127.0.0.1:8000/items/1```

ecommerce_forecast_api/
├── app/
│   ├── main.py
│   ├── data_loader.py
│   ├── schemas.py
│   └── ml.py
├── data/
│   └── data.csv
├── requirements.txt