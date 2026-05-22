from extract import extract_data
from transform import transform_data
from load import load_data_to_postgres


def run_etl_pipeline():
    raw_file_path = "data/raw/bank_transactions.csv"
    table_name = "bank_transactions"

    print("Starting ETL pipeline...")

    # Extract
    df = extract_data(raw_file_path)

    # Transform
    transformed_df = transform_data(df)

    # Load
    load_data_to_postgres(transformed_df, table_name)

    print("ETL pipeline completed successfully.")


if __name__ == "__main__":
    run_etl_pipeline()