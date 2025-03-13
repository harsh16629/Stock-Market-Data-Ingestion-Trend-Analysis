# Stock Market Data Ingestion & Trend Analysis

##  Overview
This project automates the process of **extracting, transforming, and storing** stock market data while providing **visual insights** using **Streamlit and Plotly**. It integrates **Yahoo Finance API** for data retrieval, **PostgreSQL** for storage, and **AWS Lambda** for automation.

---

##  Features
- **Extract**: Fetch stock data (Open, Close, High, Low, Volume) from **Yahoo Finance API**.
- **Transform**: Clean data, compute **50-day & 200-day moving averages**, and **identify trends** (bullish/bearish).
- **Load**: Store processed data in a **PostgreSQL** database.
- **Automate**: Run periodically via **AWS Lambda**.
- **Visualize**: Interactive **dashboard** with **Plotly & Streamlit**.

---

## Tech Stack
- **Python** (Data Processing)
- **Pandas** (Data Transformation)
- **PostgreSQL** (Database)
- **Yahoo Finance API** (Stock Data)
- **Matplotlib & Plotly** (Visualization)
- **AWS Lambda** (Automation)
- **Streamlit** (Dashboard)

---


## Setup & Installation
1️. Clone the Repository
```sh
  git clone https://github.com/harsh16629/Stock-Market-Data-Ingestion-Trend-Analysis.git
  cd Stock Market Data Ingestion Trend Analysis
```
2️. Create & Activate a Virtual Environment
```sh
  python -m venv venv
  source venv/bin/activate  # On macOS/Linux
  venv\Scripts\activate     # On Windows
```
3️. Install Dependencies
```sh
  pip install -r requirements.txt
```
4️. Set Up PostgreSQL Database
Ensure PostgreSQL is installed and create a database:

```sql
CREATE DATABASE stock_db;
```
Update DB_PARAMS in etl_local.py with your PostgreSQL credentials.

## Running the Project
1. Local Execution
Run the ETL process and visualize stock trends:
```sh
  python etl_local.py
```
This fetches Apple Inc. (AAPL) stock data, transforms it, loads it into PostgreSQL, and displays it via Streamlit.

2. Running the Visualization Dashboard
If you only want to view the dashboard:
```sh
  streamlit run etl_local.py
```
3. Deploying to AWS Lambda
- Package the Dependencies:
```sh
  pip install -r requirements.txt -t package/
  cd package && zip -r ../etl_lambda.zip . && cd ..
  zip -g etl_lambda.zip etl_lambda.py
```  
- Upload to AWS Lambda:
Create an AWS Lambda function.
Upload etl_lambda.zip.
Set the handler as etl_lambda.lambda_handler.

- Schedule with AWS EventBridge:
Set a CloudWatch Rule to trigger the Lambda function daily.

## License
This project is licensed under the MIT [License](LICENSE).
