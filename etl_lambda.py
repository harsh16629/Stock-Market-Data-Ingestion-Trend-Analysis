import json
from etl_local import fetch_stock_data, transform_data, load_to_postgres

def lambda_handler(event, context):
    ticker = event.get("ticker", "AAPL")
    data = fetch_stock_data(ticker)
    transformed_data = transform_data(data)
    load_to_postgres(transformed_data, ticker)
    return {"status": "Success", "message": f"Data for {ticker} loaded successfully."}