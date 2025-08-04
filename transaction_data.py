import pandas as pd
import random
from faker import Faker
from datetime import datetime
import os

# Parameters
fake = Faker()
RECORD_COUNT = 1_000_000
TODAY = datetime.today().strftime("%Y-%m-%d")

# Products catalog
PRODUCTS = [
    {"product_id": "01", "name": "Facewash", "category": "skincare", "price": 25.99},
    {"product_id": "02", "name": "lipliner", "category": "makeup", "price": 49.99},
    {"product_id": "03", "name": "Lipgloss", "category": "makeup", "price": 4.99},
    {"product_id": "04", "name": "moisturizer", "category": "skincare", "price": 12.50},
    {"product_id": "05", "name": "face cream", "category": "skincare", "price": 34.95},
    {"product_id": "06", "name": "Toner", "category": "skincare", "price": 19.99},
    {"product_id": "07", "name": "Sunscreen", "category": "skincare", "price": 29.50},
    {"product_id": "08", "name": "Eye Cream", "category": "skincare", "price": 22.75},
    {"product_id": "09", "name": "Cleansing Oil", "category": "skincare", "price": 18.00},
    {"product_id": "10", "name": "Night Serum", "category": "skincare", "price": 39.99},
    {"product_id": "11", "name": "Exfoliating Scrub", "category": "skincare", "price": 15.99},
    {"product_id": "12", "name": "Hydrating Mask", "category": "skincare", "price": 24.50},
    {"product_id": "13", "name": "Clay Mask", "category": "skincare", "price": 20.00},
    {"product_id": "14", "name": "Eye Serum", "category": "skincare", "price": 26.25},
    {"product_id": "15", "name": "Anti-aging Cream", "category": "skincare", "price": 42.00},
    {"product_id": "16", "name": "Foundation", "category": "makeup", "price": 35.00},
    {"product_id": "17", "name": "Concealer", "category": "makeup", "price": 21.50},
    {"product_id": "18", "name": "Blush", "category": "makeup", "price": 18.75},
    {"product_id": "19", "name": "Highlighter", "category": "makeup", "price": 24.99},
    {"product_id": "20", "name": "Bronzer", "category": "makeup", "price": 23.00},
    {"product_id": "21", "name": "Mascara", "category": "makeup", "price": 19.99},
    {"product_id": "22", "name": "Eyeliner", "category": "makeup", "price": 14.25},
    {"product_id": "23", "name": "Eyeshadow Palette", "category": "makeup", "price": 45.00},
    {"product_id": "24", "name": "Primer", "category": "makeup", "price": 13.50},
    {"product_id": "25", "name": "Setting Spray", "category": "makeup", "price": 20.00}
]

CITY = ["London", "Manchester", "Hatfield", "Luton", "Sheffield", "Oxford", "Conventry", "Milton Keynes", "Wolverhampton", "Liverpool"]

PAYMENT_METHODS = ["Credit Card", "PayPal", "Cash", "Debit Card"]

def generate_transaction_data(n=RECORD_COUNT):
    transactions = []
    for _ in range(n):
        customer_id = f"{fake.random_int(1000, 9999)}"
        product = random.choice(PRODUCTS)
        store_location = random.choice(CITY)
        quantity = random.randint(1, 5)
        unit_price = product["price"]
        total = round(quantity * unit_price, 2)

        transaction_data = {
            "transaction_id": fake.uuid4(),
            "customer_id": customer_id,
            "product_id": product["product_id"],
            "product_name": product["name"],
            "category": product["category"],
            "quantity": quantity,
            "unit_price": unit_price,
            "total_amount": total,
            "payment_method": random.choice(PAYMENT_METHODS),
            "transaction_date": fake.date_time_this_year().isoformat(),
            "store_location": random.choice(CITY)
        }
        transactions.append(transaction_data)
    return pd.DataFrame(transactions)

print(generate_transaction_data(10))



