import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)



def transform_data(df):
    """
    Clean and transform bank transaction data
    """

    # print("Starting data transformation...")
    logging.info("Starting data transformation...")


    # 1. Clean column names
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(" ", "_")
    )

    # 2. Remove duplicate rows
    df = df.drop_duplicates()

    # 3. Convert date columns
    df["transactiondate"] = pd.to_datetime(df["transactiondate"])
    df["previoustransactiondate"] = pd.to_datetime(df["previoustransactiondate"])

    # 4. Create new useful columns
    df["transaction_hour"] = df["transactiondate"].dt.hour
    df["transaction_day"] = df["transactiondate"].dt.day_name()

    df["time_since_previous_transaction_hours"] = (
        df["transactiondate"] - df["previoustransactiondate"]
    ).dt.total_seconds() / 3600

    # 5. Mark large transactions
    large_transaction_threshold = df["transactionamount"].quantile(0.90)

    df["is_large_transaction"] = (
        df["transactionamount"] > large_transaction_threshold
    )

    # print("Data transformation completed.")
    # print(f"Rows after transformation: {df.shape[0]}")
    # print(f"Columns after transformation: {df.shape[1]}")

    logging.info("Data transformation completed.")
    logging.info(f"Rows after transformation: {df.shape[0]}")
    logging.info(f"Columns after transformation: {df.shape[1]}")


    return df


if __name__ == "__main__":

    raw_file_path = "data/raw/bank_transactions.csv"
    processed_file_path = "data/processed/cleaned_transactions.csv"

    df = pd.read_csv(raw_file_path)

    transformed_df = transform_data(df)

    transformed_df.to_csv(processed_file_path, index=False)

    print(f"Cleaned data saved to {processed_file_path}")