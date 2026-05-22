import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)


# Load environment variables
load_dotenv()


def load_data_to_postgres(df, table_name):

    """
    Load transformed data into PostgreSQL
    """
    logging.info("Starting data load to PostgreSQL...")

    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    # PostgreSQL connection string
    engine = create_engine(
        f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

    # Load dataframe into PostgreSQL
    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        # if_exists="append",
        index=False
    )

    # print(f"Data loaded successfully into table: {table_name}")
    logging.info(f"Data loaded successfully into table: {table_name}")


if __name__ == "__main__":

    processed_file_path = "data/processed/cleaned_transactions.csv"

    df = pd.read_csv(processed_file_path)

    load_data_to_postgres(df, "bank_transactions")