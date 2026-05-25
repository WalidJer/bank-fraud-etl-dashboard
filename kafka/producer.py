import pandas as pd
import json
import time
from kafka import KafkaProducer


TOPIC_NAME = "bank_transactions_stream"
KAFKA_SERVER = "localhost:9092"
CSV_FILE_PATH = "data/processed/cleaned_transactions.csv"


producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda value: json.dumps(value, default=str).encode("utf-8")
)


def send_transactions_to_kafka():
    df = pd.read_csv(CSV_FILE_PATH)

    print(f"Sending {len(df)} transactions to Kafka topic: {TOPIC_NAME}")

    for index, row in df.iterrows():
        transaction = row.to_dict()

        producer.send(TOPIC_NAME, value=transaction)

        print(f"Sent transaction: {transaction['transactionid']}")

        time.sleep(0.1)

    producer.flush()
    producer.close()

    print("All transactions sent successfully.")


if __name__ == "__main__":
    send_transactions_to_kafka()
