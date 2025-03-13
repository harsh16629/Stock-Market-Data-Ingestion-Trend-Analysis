#for local execution
import yfinance as yf
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import plotly.express as px
import streamlit as st

# Database connection details
DB_PARAMS = {
    "dbname": "stock_db",
    "user": "postgres",
    "password": "yourpassword",
    "host": "localhost",
    "port": "5432"
}

def fetch_stock_data(ticker, period="1mo", interval="1d"):
    """Fetch stock data from Yahoo Finance."""
    stock = yf.Ticker(ticker)
    data = stock.history(period=period, interval=interval)
    data.reset_index(inplace=True)
    return data

def transform_data(data):
    """Clean and add moving averages."""
    data["Moving_Avg_50"] = data["Close"].rolling(window=50).mean()
    data["Moving_Avg_200"] = data["Close"].rolling(window=200).mean()
    data.dropna(inplace=True)
    
    # Determine trend
    data["Trend"] = "Bearish"
    data.loc[data["Moving_Avg_50"] > data["Moving_Avg_200"], "Trend"] = "Bullish"
    return data

def load_to_postgres(data, ticker):
    """Load data into PostgreSQL."""
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS stock_data (
            id SERIAL PRIMARY KEY,
            ticker VARCHAR(10),
            date TIMESTAMP,
            open_price FLOAT,
            high_price FLOAT,
            low_price FLOAT,
            close_price FLOAT,
            volume BIGINT,
            moving_avg_50 FLOAT,
            moving_avg_200 FLOAT,
            trend VARCHAR(10)
        );
        """
        cur.execute(create_table_query)
        
        insert_query = """
        INSERT INTO stock_data (ticker, date, open_price, high_price, low_price, close_price, volume, moving_avg_50, moving_avg_200, trend)
        VALUES %s;
        """
        values = [(ticker, row["Date"], row["Open"], row["High"], row["Low"], row["Close"], row["Volume"], row["Moving_Avg_50"], row["Moving_Avg_200"], row["Trend"]) for _, row in data.iterrows()]
        execute_values(cur, insert_query, values)
        
        conn.commit()
        cur.close()
        conn.close()
        print(f"Data for {ticker} loaded successfully.")
    except Exception as e:
        print(f"Error loading data: {e}")

def visualize_data(ticker):
    """Visualize stock trends using Streamlit and Plotly."""
    conn = psycopg2.connect(**DB_PARAMS)
    query = f"SELECT date, close_price, moving_avg_50, moving_avg_200, trend FROM stock_data WHERE ticker = '{ticker}' ORDER BY date;"
    df = pd.read_sql(query, conn)
    conn.close()
    
    st.title(f"Stock Trend Analysis for {ticker}")
    fig = px.line(df, x="date", y=["close_price", "moving_avg_50", "moving_avg_200"], labels={"value": "Price", "date": "Date"}, title="Stock Prices & Moving Averages")
    st.plotly_chart(fig)
    
    trend_counts = df["trend"].value_counts().reset_index()
    trend_counts.columns = ["Trend", "Count"]
    st.bar_chart(trend_counts.set_index("Trend"))

def main():
    ticker = "AAPL"
    data = fetch_stock_data(ticker)
    transformed_data = transform_data(data)
    load_to_postgres(transformed_data, ticker)
    visualize_data(ticker)
    
if __name__ == "__main__":
    main()
