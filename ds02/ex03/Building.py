import os
import psycopg2
import numpy as np
from dotenv import load_dotenv  
import matplotlib.pyplot as plt


load_dotenv(dotenv_path= '../.env')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

connection = psycopg2.connect(database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host="localhost", port=5432)

cursor = connection.cursor()

numCustomers_per_numOrders = """
    SELECT purchase_count,
           COUNT(*) AS num_customers
    FROM (
        SELECT user_id, COUNT(*) AS purchase_count
        FROM customers
        WHERE event_type = 'purchase'
        GROUP BY user_id
    ) AS user_purchases
    GROUP BY purchase_count
    ORDER BY purchase_count;
""" 

numCUstomers_per_valPrice = """
    SELECT purchase_sum,
           COUNT(*) AS num_customers
    FROM (
        SELECT user_id, SUM(price) AS purchase_sum
        FROM customers
        WHERE event_type = 'purchase'
        GROUP BY user_id
    ) AS user_purchases
    GROUP BY purchase_sum
    ORDER BY num_customers DESC;
"""

def calculate_cutoff_x(x, y) :
    cumulative = np.cumsum(y)
    total = cumulative[-1]
    cutoff_idx = np.argmax(cumulative >= 0.95 * total)
    cutoff_x = x[cutoff_idx]
    return cutoff_x
def set_cutoff(x, y) :
    cutoff_x = calculate_cutoff_x( x, y)
    plt.xlim(x[0], cutoff_x)

cursor.execute(numCustomers_per_numOrders)
record = cursor.fetchall()

purchase_count = [float(row[0]) for row in record]
num_customers = [float(row[1]) for row in record]

plt.figure(figsize=(8, 18))
plt.subplot(2, 1, 1)
set_cutoff(purchase_count, num_customers)
plt.bar(purchase_count, num_customers, width=0.8, color = 'lightblue', zorder=3, edgecolor='lightgray')
plt.grid(zorder=0, color='lightgray')
plt.ylabel('number of customers')
plt.xlabel('number of orders', loc='left')
plt.title('Customer Purchases Frequency Distribution')



cursor.execute(numCUstomers_per_valPrice)
record = cursor.fetchall()

purchase_sum = [float(row[0]) for row in record]
num_customers = [float(row[1]) for row in record]

plt.subplot(2, 1, 2)
set_cutoff(purchase_sum, num_customers)
plt.bar(purchase_sum, num_customers, width=0.8, color = 'lightblue', zorder=3, edgecolor='lightgray')
plt.grid(zorder=0, color='lightgray')
plt.ylabel('number of customers')
plt.xlabel('monetary value in ₳')
plt.title('Customer Spendings Frequency Distribution')
plt.show()