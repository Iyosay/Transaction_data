import random
from datetime import datetime

import awswrangler as wr
import boto3
import pandas as pd
from airflow.models import Variable
from faker import Faker

fake = Faker()

"""
Synthetic Transaction Data Generator for Skincare Products Business.

This script generates fake skincare product transactions using the Faker library,
formats them into a DataFrame, and uploads the data as a Parquet file to an S3 bucket.
"""

# Constants
RECORD_COUNT = fake.random_int(500000, 1000000)
CITY = [
    "London",
    "Manchester",
    "Hatfield",
    "Luton",
    "Sheffield",
    "Oxford",
    "Coventry",
    "Milton Keynes",
    "Wolverhampton",
    "Liverpool",
]
PAYMENT_METHODS = ["Credit Card", "PayPal", "Cash", "Debit Card"]
PRODUCTS = [
    {"product_id": 1, "name": "Facewash", "category": "skincare", "price": 25.99},
    {"product_id": 2, "name": "Lipgloss", "category": "makeup", "price": 4.99},
    {"product_id": 3, "name": "Lipliner", "category": "makeup", "price": 12.50},
    {"product_id": 4, "name": "Cleanser", "category": "skincare", "price": 19.99},
    {"product_id": 5, "name": "Toner", "category": "skincare", "price": 20.50},
    {"product_id": 6, "name": "Moisturizer", "category": "skincare", "price": 22.00},
    {"product_id": 7, "name": "Cleansing Oil", "category": "skincare", "price": 28.00},
    {"product_id": 8, "name": "Face Serum", "category": "skincare", "price": 18.00},
    {"product_id": 9, "name": "Foundation", "category": "makeup", "price": 32.00},
    {"product_id": 10, "name": "Concealer", "category": "makeup", "price": 21.50},
    {"product_id": 11, "name": "Blush", "category": "makeup", "price": 18.75},
    {"product_id": 12, "name": "Highlighter", "category": "makeup", "price": 24.99},
    {"product_id": 13, "name": "Bronzer", "category": "makeup", "price": 23.99},
    {"product_id": 14, "name": "Eyeliner", "category": "makeup", "price": 14.25},
    {
        "product_id": 15,
        "name": "Eyeshadow Palette",
        "category": "makeup",
        "price": 45.00,
    },
    {"product_id": 16, "name": "Primer", "category": "makeup", "price": 15.50},
]


"""
    Generate fake skincare transactions and upload them to an S3 bucket as a Parquet file.

"""


def skincare_transaction_data():

    transactions = []

    for _ in range(RECORD_COUNT):
        product = random.choice(PRODUCTS)
        quantity = random.randint(1, 20)
        unit_price = product["price"]
        total = quantity * unit_price

        transaction = {
            "transaction_id": fake.uuid4(),
            # "product_id": product["product_id"],
            "product_name": product["name"],
            "category": product["category"],
            # "quantity": quantity,
            "unit_price": unit_price,
            "total_amount": total,
            "payment_method": random.choice(PAYMENT_METHODS),
            # "location": random.choice(CITY),
            # "timestamp": fake.date_time_this_year().isoformat()
        }

        transactions.append(transaction)

    df = pd.DataFrame(transactions)

    # AWS Setup
    session = boto3.session.Session(
        aws_access_key_id=Variable.get("JOY_KEY"),
        aws_secret_access_key=Variable.get("JOY_SECRET"),
        region_name="eu-west-2",
    )
    # Generate filename with today's date
    file_date = datetime.today().strftime("%Y-%m-%d")
    s3_path = f"s3://joy-skincare-daily-transaction-data/transactions/{file_date}_tranx.parquet"

    # Upload the DataFrame as a Parquet file to the specified S3 path
    wr.s3.to_parquet(df=df, path=s3_path, dataset=False, boto3_session=session)
    return df
