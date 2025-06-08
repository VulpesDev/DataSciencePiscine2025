import psycopg2
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path= '../.env')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

connection = psycopg2.connect(database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host="localhost", port=5432)

cursor = connection.cursor()

cursor.execute(""" SELECT event_type, COUNT(*) as count
        FROM customers
        GROUP BY event_type
        ORDER BY count DESC""")

# Fetch all rows from database
record = cursor.fetchall()

labels = [row[0] for row in record]
values = [row[1] for row in record]

plt.figure(figsize=(10, 6))
plt.pie(values, 
            labels=labels,
            autopct='%1.1f%%',
            startangle=35)
    
plt.axis('equal')

plt.title('Event Types Pie Chart')
    
plt.show()

print("Data from Database:- ", record)