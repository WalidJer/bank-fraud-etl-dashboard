import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def extract_data(file_path):
    """
    Extract data from CSV file
    """

    logging.info("Starting data extraction...")


    df = pd.read_csv(file_path)

    # print("Data extracted successfully.")
    # print(f"Number of rows: {df.shape[0]}")
    # print(f"Number of columns: {df.shape[1]}")

    logging.info("Data extracted successfully.")
    logging.info(f"Number of rows: {df.shape[0]}")
    logging.info(f"Number of columns: {df.shape[1]}")


    return df


if __name__ == "__main__":

    file_path = "data/raw/bank_transactions.csv"

    df = extract_data(file_path)

    print(df.head())