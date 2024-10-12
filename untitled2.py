# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1eNia5Fsa5NfrQpd4Jk7Pg2aQxrGaqLyo
"""

pip install pyspark

from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, DoubleType, StringType, StructType, StructField
from datetime import datetime, timedelta
import random

spark = SparkSession.builder.appName("data generation").getOrCreate()

num = 1000
product = ["computer", "monitor", "laptop", "mouse", "keyboard"]
start_date = datetime(2024, 1, 1).date()
end_date = datetime(2024, 9, 30).date()

def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

schema = StructType([
    StructField("Дата", StringType(), True),
    StructField("UserID", IntegerType(), True),
    StructField("Продукт", StringType(), True),
    StructField("Количество", IntegerType(), True),
    StructField("Цена", DoubleType(), True),
])

def generate_row():
    date = random_date(start_date, end_date).strftime("%Y-%m-%d")
    user_id = random.randint(1, 1000)
    random_product = random.choice(product)
    quantity = random.randint(1, 1000)
    price = round(random.uniform(1.0, 100000.0), 1)
    return (date, user_id, random_product, quantity, price)

data = [generate_row() for _ in range(num)]

df = spark.createDataFrame(data, schema)

df.coalesce(1).write.csv("data generation.csv", header=True, mode='overwrite')

spark.stop()