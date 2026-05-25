# Bank Fraud ETL & Risk Monitoring Dashboard

## Project Overview

This project is an end-to-end Data Engineering and Business Intelligence pipeline built using:

- Python
- Pandas
- PostgreSQL
- Apache Airflow
- Docker
- Astro CLI
- Power BI

The goal of this project is to simulate a real-world banking transaction ETL workflow and build interactive dashboards for fraud/risk monitoring and business analytics.

The pipeline performs:

1. Data Extraction
2. Data Transformation
3. Data Loading into PostgreSQL
4. Workflow Orchestration using Apache Airflow
5. Interactive Dashboarding using Power BI

---

# Project Architecture

```text
Kaggle Banking Dataset
        ↓
Python / Pandas ETL
        ↓
PostgreSQL Database
        ↓
Apache Airflow DAG
        ↓
Power BI Dashboard
```

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python | ETL scripting |
| Pandas | Data transformation |
| PostgreSQL | Data warehouse/database |
| SQLAlchemy | Database connection |
| Psycopg2 | PostgreSQL adapter |
| Apache Airflow | Workflow orchestration |
| Docker | Containerization |
| Astro CLI | Airflow local development |
| Power BI | Data visualization & dashboarding |

---

# Dataset

Dataset used from Kaggle:

Bank Transaction Dataset for Fraud Detection

Dataset includes:
- Transaction IDs
- Account IDs
- Transaction Amounts
- Transaction Dates
- Transaction Types
- Locations
- Channels (ATM / Branch / Online)
- Customer Information
- Account Balances
- Previous Transaction Dates

---

# Project Folder Structure

```text
bank_fraud_etl/
│
├── dags/
│   └── fraud_etl_dag.py
│
├── data/
│   ├── raw/
│   │   └── bank_transactions.csv
│   │
│   └── processed/
│       └── cleaned_transactions.csv
│
├── logs/
│
├── scripts/
│   ├── __init__.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── etl_pipeline.py
│   └── validate.py
│
├── sql/
│   └── create_tables.sql
│
├── .env
├── requirements.txt
├── README.md
│
├── Dockerfile
├── airflow_settings.yaml
└── packages.txt
```

---

# ETL Pipeline

## 1. Extract Stage

### File:
```text
scripts/extract.py
```

### Responsibilities:
- Read raw CSV file
- Load data into Pandas DataFrame
- Log extraction details

### Main Operations:
- `pd.read_csv()`
- Logging
- Row/column inspection

---

## 2. Transform Stage

### File:
```text
scripts/transform.py
```

### Responsibilities:
- Clean column names
- Remove duplicates
- Convert date columns
- Perform feature engineering

### Transformations Performed

### Clean column names

```python
df.columns = (
    df.columns
    .str.lower()
    .str.strip()
    .str.replace(" ", "_")
)
```

### Remove duplicates

```python
df.drop_duplicates()
```

### Convert datetime columns

```python
pd.to_datetime()
```

### Feature Engineering

Created:
- `transaction_hour`
- `transaction_day`
- `time_since_previous_transaction_hours`
- `is_large_transaction`

### Large transaction logic

```python
df["transactionamount"] > df["transactionamount"].quantile(0.90)
```

---

## 3. Load Stage

### File:
```text
scripts/load.py
```

### Responsibilities:
- Connect to PostgreSQL
- Load transformed data into database

### Technologies:
- SQLAlchemy
- Psycopg2
- PostgreSQL

### Database Loading

```python
df.to_sql(
    table_name,
    engine,
    if_exists="replace",
    index=False
)
```

---

# PostgreSQL Setup

## Create Database

```sql
CREATE DATABASE fraud_db;
```

---

# Environment Variables

## `.env`

```text
DB_USER=postgres
DB_PASSWORD=YOUR_PASSWORD
DB_HOST=host.docker.internal
DB_PORT=5432
DB_NAME=fraud_db
```

---

# Required Python Packages

## Install Dependencies

```powershell
py -m pip install pandas sqlalchemy psycopg2-binary python-dotenv
```

## Save Requirements

```powershell
py -m pip freeze > requirements.txt
```

---

# Airflow Setup

## Astro Initialization

### Initialize Astro Project

```powershell
astro dev init
```

### Start Airflow

```powershell
astro dev start
```

### Restart Airflow

```powershell
astro dev restart
```

### View Logs

```powershell
astro dev logs
```

---

# Airflow UI

Access:

```text
http://localhost:8080
```

Default Credentials:

```text
Username: admin
Password: admin
```

---

# Airflow DAG

## DAG File

```text
dags/fraud_etl_dag.py
```

---

# Airflow Tasks

The ETL workflow was split into separate tasks:

```text
extract_bank_transactions
        ↓
transform_bank_transactions
        ↓
load_bank_transactions_to_postgres
```

![Airflow DAG](screenshots/Airflow_DAG.png)

---

# Why Splitting Tasks Matters

Benefits:
- Better monitoring
- Easier debugging
- Independent retries
- Production-ready orchestration
- Cleaner pipeline management

---

# Docker Networking Issue Solved

Problem encountered:

```text
localhost inside Docker container is not the local machine
```

Fix:

```text
DB_HOST=host.docker.internal
```

This allowed Airflow containers to connect to local PostgreSQL.

---

# Logging

Logging was added using Python logging module.

Example:

```python
import logging

logging.basicConfig(level=logging.INFO)

logging.info("Starting data extraction...")
```

Benefits:
- Better monitoring
- Easier debugging
- Airflow log integration

---

# Power BI Dashboard

## Power BI Connected To

```text
PostgreSQL → fraud_db → bank_transactions
```

---

# Dashboard Pages

---

# Page 1 — Executive Overview

### KPIs
- Total Transaction Amount
- Total Transactions
- Average Transaction Amount

### Charts
- Transactions by Channel
- Transactions by Type
- Transactions by Hour

### Business Insights
- Channel usage distribution
- Debit vs Credit behavior
- Peak transaction activity hours

![Executive Overview](screenshots/powerBi1.png)

---

# Page 2 — Risk Monitoring

### KPI
- Large Transactions

### Visuals
- Suspicious Large Transactions Table
- Large Transactions by Channel

### Business Insights
- High-value transaction monitoring
- Risk distribution across transaction channels

![Risk Monitoring](screenshots/powerBi2.png)


---

# Page 3 — Location Risk Analysis

### KPI
- High Risk Locations

### Visuals
- High-Risk Transactions by Location
- Interactive Channel Slicer

### Business Insights
- Geographic risk concentration
- High-risk transaction locations
- Channel-based filtering

![Location Risk](screenshots/powerBi3.png)


---

# Power BI Measures Created

## Total Transactions

```DAX
Total Transactions = COUNT(bank_transactions[transactionid])
```

---

## Average Transaction Amount

```DAX
Average Transaction Amount = 
AVERAGE(bank_transactions[transactionamount])
```

---

## Large Transactions

```DAX
Large Transactions =
CALCULATE(
    COUNT(bank_transactions[transactionid]),
    bank_transactions[is_large_transaction] = TRUE()
)
```

---

## High Risk Locations

```DAX
High Risk Locations =
DISTINCTCOUNT(bank_transactions[location])
```

---

# Dashboard Design Concepts Applied

- Multi-page dashboard architecture
- KPI card design
- Interactive slicers
- Risk-focused analytics
- Executive overview layout
- Consistent visual formatting
- Business-oriented storytelling

---

# Key Data Engineering Concepts Demonstrated

## ETL Pipeline Development
- Extraction
- Transformation
- Loading

## Workflow Orchestration
- Apache Airflow DAGs
- Task dependencies
- Scheduling concepts

## Containerization
- Docker networking
- Astro CLI

## Data Warehousing
- PostgreSQL integration

## Business Intelligence
- Power BI dashboards
- KPI development
- Interactive filtering

---

# Example Business Insights

- Debit transactions dominate compared to credit transactions.
- Branch transactions are slightly higher than ATM and Online transactions.
- Certain locations exhibit higher concentrations of large transactions.
- Online channels show slightly elevated high-value transaction activity.
- Transaction activity peaks around hour 16.

---
# Kafka Streaming Pipeline

## Overview

Apache Kafka was added to extend the project from a traditional batch ETL workflow into a streaming data pipeline capable of simulating real-time banking transaction processing.

The streaming pipeline performs:

1. Read cleaned transaction records
2. Publish transaction events into Kafka topics
3. Consume streaming events
4. Load streamed transactions into PostgreSQL
5. Visualize streaming data in Power BI

## Updated Project Architecture Using Kafka

```text
                         ┌────────────────────┐
                         │ Kaggle CSV Dataset │
                         └─────────┬──────────┘
                                   │
                     ┌─────────────┴─────────────┐
                     │                           │
                     ▼                           ▼
          Batch ETL Pipeline           Streaming Pipeline
                     │                           │
                     ▼                           ▼
          Pandas Transformation        Kafka Producer
                     │                           │
                     ▼                           ▼
               Apache Airflow              Kafka Topic
                     │                           │
                     ▼                           ▼
                PostgreSQL               Kafka Consumer
                     │                           │
                     └───────────┬───────────────┘
                                 ▼
                           Power BI Dashboard
```

---

# Updated Technologies Used

| Technology | Purpose |
|---|---|
| Python | ETL scripting |
| Pandas | Data transformation |
| PostgreSQL | Data warehouse/database |
| SQLAlchemy | Database connection |
| Psycopg2 | PostgreSQL adapter |
| Apache Airflow | Workflow orchestration |
| Docker | Containerization |
| Astro CLI | Airflow local development |
| Apache Kafka | Real-time event streaming |
| Kafka Producer/Consumer | Streaming transaction processing |
| Kafka UI | Kafka topic and consumer monitoring |
| Power BI | Data visualization & dashboarding |

---

# Update Folder Structure to include:

```text
├── kafka/
│   ├── producer.py
│   ├── consumer.py
│   └── docker-compose.kafka.yml

---

# Kafka Streaming Architecture

```text
Cleaned CSV File
      ↓
Kafka Producer
      ↓
Kafka Topic
bank_transactions_stream
      ↓
Kafka Consumer
      ↓
PostgreSQL Table
bank_transactions_stream
      ↓
Power BI
```

---

# Kafka Docker Setup

## Docker Compose File

### File

```text
docker-compose.kafka.yml
```

### Start Kafka

```powershell
docker compose -f docker-compose.kafka.yml up -d
```

### Stop Kafka

```powershell
docker compose -f docker-compose.kafka.yml down
```

### Check Running Containers

```powershell
docker ps
```

Expected containers:

```text
bank_fraud_kafka
kafka_ui
```

---

# Kafka Topic Management

## Create Kafka Topic

```powershell
docker exec -it bank_fraud_kafka kafka-topics --bootstrap-server localhost:9092 --create --topic bank_transactions_stream --partitions 1 --replication-factor 1
```

## List Kafka Topics

```powershell
docker exec -it bank_fraud_kafka kafka-topics --bootstrap-server localhost:9092 --list
```

Expected output:

```text
bank_transactions_stream
```

---

# Kafka Producer

## File

```text
kafka/producer.py
```

## Responsibilities

- Read cleaned transaction CSV
- Convert transaction rows into JSON messages
- Publish transaction events into Kafka topic
- Simulate real-time streaming using delays

## Run Kafka Producer

```powershell
py kafka/producer.py
```

Expected output:

```text
Sent transaction: TX000001
Sent transaction: TX000002
...
All transactions sent successfully.
```

---

# Kafka Consumer

## File

```text
kafka/consumer.py
```

## Responsibilities

- Consume Kafka transaction events
- Deserialize JSON messages
- Convert events into DataFrames
- Insert streamed records into PostgreSQL
- Continuously listen for new events

## Run Kafka Consumer

```powershell
py kafka/consumer.py
```

Expected output:

```text
Inserted transaction: TX000001
Inserted transaction: TX000002
...
```

---

# PostgreSQL Stream Verification

## Verify Streamed Records

```sql
SELECT COUNT(*) FROM bank_transactions_stream;
```

Purpose:
- Confirm Kafka consumer successfully inserted streaming records into PostgreSQL.

---

# Kafka UI

Kafka UI was added for visual monitoring and inspection of:

- Topics
- Messages
- Consumer Groups
- Brokers
- Partitions

## Access Kafka UI

```text
http://localhost:8085
```

---

# Kafka Concepts Demonstrated

This project demonstrates:

- Kafka Producers
- Kafka Consumers
- Kafka Topics
- Event Streaming
- Real-Time Data Pipelines
- Consumer Groups
- Streaming PostgreSQL Ingestion
- Docker-based Kafka Deployment
- Kafka UI Monitoring

---

# Streaming Pipeline Benefits

The Kafka streaming architecture enables:

- Real-time transaction ingestion
- Event-driven architecture
- Decoupled producer/consumer systems
- Scalable streaming pipelines
- Real-time fraud monitoring simulation
- Streaming analytics workflows

---

# Kafka Screenshots

## Kafka Streaming Architecture

![Kafka Architecture](screenshots/Kafka_Architecture.png)

---

## Kafka UI Dashboard

![Kafka UI](screenshots/Kafka_Topic.png)

---

## Kafka Producer Output

![Kafka Producer](screenshots/Producer.png)

---

## Kafka Consumer Output

![Kafka Consumer](screenshots/Consumer.png)

---

## PostgreSQL Stream Verification

![PostgreSQL Verification](screenshots/kafka_postgres.png)

---

# Updated Key Data Engineering Concepts Demonstrated

## ETL Pipeline Development
- Extraction
- Transformation
- Loading

## Workflow Orchestration
- Apache Airflow DAGs
- Task dependencies
- Scheduling concepts

## Streaming Data Engineering
- Apache Kafka producers and consumers
- Real-time event streaming
- Kafka topic management
- Streaming PostgreSQL ingestion

## Containerization
- Docker networking
- Astro CLI
- Kafka container deployment

## Data Warehousing
- PostgreSQL integration

## Business Intelligence
- Power BI dashboards
- KPI development
- Interactive filtering
