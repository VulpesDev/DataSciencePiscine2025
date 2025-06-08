import psycopg2
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from dotenv import load_dotenv
from datetime import timedelta
import numpy as np
import math
from decimal import Decimal

start_date = '2022-10-01'
end_date = '2023-03-01'

load_dotenv(dotenv_path= '../.env')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

connection = psycopg2.connect(database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host="localhost", port=5432)

cursor = connection.cursor()

number_customers_month_query = """
    SELECT DATE_TRUNC('day', event_time) AS day,
           COUNT(DISTINCT user_id)
    FROM public.customers
    WHERE event_type = 'purchase'
      AND event_time >= %s
      AND event_time < %s
    GROUP BY day
    ORDER BY day;
"""

total_sales_month_query = """
SELECT DATE_TRUNC('month', event_time) AS month, SUM(price) FROM public.customers
WHERE event_type = 'purchase'
	AND event_time >= %s
	AND event_time < %s
GROUP BY month
ORDER BY month
"""

average_spendings_per_user_per_day = """
WITH user_daily_avg AS (
    SELECT 
        user_id, 
        DATE_TRUNC('day', event_time) AS day, 
        SUM(price) AS sum_spendings_per_user_per_day
    FROM public.customers
    WHERE event_type = 'purchase'
      AND event_time >= %s
      AND event_time < %s
    GROUP BY day, user_id
)

SELECT 
    day, 
    AVG(sum_spendings_per_user_per_day) AS avg_spending_per_user
FROM user_daily_avg
GROUP BY day
ORDER BY day;
"""

#Execute PSQL queries
cursor.execute(number_customers_month_query, (start_date, end_date))
record = cursor.fetchall()

day_timestamp = [row[0] for row in record]
count = [row[1] for row in record]

cursor.execute(total_sales_month_query, (start_date, end_date))
record = cursor.fetchall()

day_timestamp2 = [row[0] for row in record]
sales = [row[1] for row in record]

cursor.execute(average_spendings_per_user_per_day, (start_date, end_date))
record = cursor.fetchall()

day_timestamp3 = [row[0] for row in record]
spendings = [float(row[1]) for row in record]

#Plot data

plt.figure(figsize=(12, 100))
plt.subplots_adjust(hspace=0.4) 
plt.subplot(3, 1, 1)
plt.plot(day_timestamp, count)
plt.grid(True)
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%B'))
plt.xlim(min(day_timestamp), max(day_timestamp))
plt.ylabel("Number of customers ")
plt.title("Fluctuations in Monthly Customer Numbers")
#plt.show()

plt.subplot(3, 1, 2)
plt.bar(day_timestamp2, sales, width=timedelta(days=20), color = 'lightblue', zorder=3, edgecolor='lightgray')
plt.grid(axis='y', zorder=0, color='lightgray')
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%B'))
plt.ylabel("total sales in million (₳) ")
plt.title("Monthly Sales Volume (Millions ₳)")
#plt.show()

plt.subplot(3, 1, 3)
plt.ylim(0, max(spendings)+5)
plt.yticks(np.arange(0, max(spendings)+5, 5))
plt.plot(day_timestamp3, spendings, color = 'lightblue', zorder=3)
plt.fill_between(day_timestamp3, spendings, zorder=3, color='lightblue')
plt.grid(zorder=0, color='lightgray')
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%B'))
plt.xlim(min(day_timestamp3), max(day_timestamp3))
plt.ylabel("average spend/customer (₳)")
plt.title("Monthly Average Revenue per Customer")
plt.show()