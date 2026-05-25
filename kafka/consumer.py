import json
import pandas as pd
from kafka import KafkaConsumer
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


TOPIC_NAME = "bank_transactions_stream"
KAFKA_SERVER = "localhost:9092"


load_dotenv()


db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")


engine = create_engine(
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)


consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=KAFKA_SERVER,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="bank_fraud_consumer_group",
    value_deserializer=lambda value: json.loads(value.decode("utf-8"))
)


def consume_transactions():
    print(f"Listening for messages on topic: {TOPIC_NAME}")

    for message in consumer:
        transaction = message.value

        df = pd.DataFrame([transaction])

        df.to_sql(
            "bank_transactions_stream",
            engine,
            if_exists="append",
            index=False
        )

        print(f"Inserted transaction: {transaction['transactionid']}")


if __name__ == "__main__":
    consume_transactions()