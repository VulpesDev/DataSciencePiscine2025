import os
import psycopg2
import numpy as np
import seaborn as sns
from dotenv import load_dotenv
import matplotlib.pyplot as plt

load_dotenv(dotenv_path= '../.env')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

connection = psycopg2.connect(database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host="localhost", port=5432)

cursor = connection.cursor()

select_prices_query = """
    SELECT price FROM public.customers
        WHERE event_type = 'purchase'
"""
average_basket_per_user_query = """
    SELECT 
      user_id,
      AVG(basket_total) AS avg_basket_price_per_user
    FROM (
      SELECT 
        user_id,
        user_session,
        SUM(price) AS basket_total
      FROM public.customers
      WHERE event_type = 'purchase'
      GROUP BY user_id, user_session
    ) AS session_totals
    GROUP BY user_id
    ORDER BY user_id;
"""

cursor.execute(select_prices_query)
record = cursor.fetchall()

prices = [float(row[0]) for row in record]

perc_q1 = np.percentile(prices, 25)
perc_q2 = np.percentile(prices, 50)
perc_q3 = np.percentile(prices, 75)

IQR = perc_q3 - perc_q1
lower_whisker = min([p for p in prices if p >= (perc_q1 - 1.5 * IQR)])
upper_whisker = max([p for p in prices if p <= (perc_q3 + 1.5 * IQR)])

cursor.execute(average_basket_per_user_query)
record = cursor.fetchall()

avrg_bask_prices_per_user = [float(row[1]) for row in record]

grid_background_color = "#f8f1e5"
grid_line_color = '#e6dbc2'
outliers_color = '#c8a6a6'
box_color = '#c8a6a6'
whiskers_caps_median_color = '#7e685a'


flierprops = dict(marker='o', markerfacecolor=outliers_color, markersize=6, linestyle='none', markeredgecolor=outliers_color)
boxprops = dict(facecolor=box_color, color=box_color, edgecolor=box_color, linewidth=2)
capprops = dict(color=whiskers_caps_median_color, linewidth=1.5)
whiskerprops = dict(color=whiskers_caps_median_color, linewidth=1.5)
medianprops=dict(color=whiskers_caps_median_color, linewidth=2)
print("count".ljust(10), len(prices))
print("mean".ljust(10), round(np.mean(prices), 2))
print("std".ljust(10), np.median(prices))
print("min".ljust(10), np.min(prices))
print("25%".ljust(10), perc_q1)
print("50%".ljust(10), perc_q2)
print("75%".ljust(10), perc_q3)
print("max".ljust(10), np.max(prices))

plt.figure(figsize=(24, 6))
plt.subplot(1,3,1)
plt.title("Box plot of prices")        
plt.gca().set_facecolor(grid_background_color)
plt.grid(True, axis='x', color=grid_line_color, linewidth=1.0)
plt.boxplot(
    prices, 
    orientation="horizontal", 
    widths=0.6,
    patch_artist=True,
    boxprops=boxprops,
    flierprops=flierprops,
    capprops=capprops,
    medianprops=medianprops,
    whiskerprops=whiskerprops)
plt.xlabel("price")
#plt.show()



plt.subplot(1,3,2)
plt.title("Interquartile range of prices")
plt.grid(True, axis='x')
plt.xlim(lower_whisker - 1, upper_whisker + 1)

plt.gca().set_facecolor(grid_background_color)
plt.grid(True, axis='x', color=grid_line_color, linewidth=1.0)
plt.boxplot(prices,
            orientation='horizontal', 
            widths=0.6,
            showfliers=False,
            patch_artist=True,
            boxprops=boxprops,
            flierprops=flierprops,
            capprops=capprops,
            medianprops=medianprops,
            whiskerprops=whiskerprops)
plt.xlabel("price")
#plt.show()


plt.subplot(1,3,3)
plt.title("Average basket price per user")
plt.gca().set_facecolor(grid_background_color)
plt.grid(True, axis='x', color=grid_line_color, linewidth=1.0)
plt.boxplot(avrg_bask_prices_per_user,
            orientation='horizontal', 
            widths=0.6,
            showfliers=False,
            patch_artist=True,
            boxprops=boxprops,
            flierprops=flierprops,
            capprops=capprops,
            medianprops=medianprops,
            whiskerprops=whiskerprops)
plt.grid(True, axis='x')
plt.xlabel("average basket price")
                    
plt.show()
