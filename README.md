# API REST 

## Dataset

I'm using a ecommerce dataset from Kaggle. To download the dataset use ```download_data.sh```.

## FastAPI

To check the functions in terminal use the following commands:

- ```curl http://127.0.0.1:8000/health```

- ```curl http://127.0.0.1:8000/summary```

- ```curl http://127.0.0.1:8000/sales/daily```

## Project Structure

ecommerce_forecast_api/
├── app/
│   ├── main.py
│   ├── data_loader.py
│   ├── schemas.py
│   └── ml.py
├── data/
│   └── data.csv
├── requirements.txt