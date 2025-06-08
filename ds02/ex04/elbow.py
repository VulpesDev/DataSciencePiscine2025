import os
import psycopg2
from dotenv import load_dotenv
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


load_dotenv(dotenv_path= '../.env')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

connection = psycopg2.connect(database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host="localhost", port=5432)

cursor = connection.cursor()

user_analysis_query = """
    SELECT
        user_id,
        SUM(price) AS total_spent,
        AVG(price) AS avg_price,
        COUNT(product_id) AS total_items,
        COUNT(DISTINCT user_session) AS unique_sessions,
        COUNT(DISTINCT category_code) AS unique_categories,
        COUNT(DISTINCT brand) AS unique_brands
    FROM customers
    WHERE event_type = 'purchase'
    GROUP BY user_id
    ORDER BY user_id
""" 

cursor.execute(user_analysis_query)
record = cursor.fetchall()

user_id = [float(row[0]) for row in record]
total_spent = [float(row[1]) for row in record]
avg_price = [float(row[2]) for row in record]
total_items = [float(row[3]) for row in record]
unique_sessions = [float(row[4]) for row in record]
unique_categories = [float(row[5]) for row in record]
unique_brands = [float(row[6]) for row in record]

user_df = pd.DataFrame({
    'user_id': user_id,
    'total_spent': total_spent,
    'avg_price': avg_price,
    'total_items': total_items,
    'unique_sessions': unique_sessions,
    'unique_categories': unique_categories,
    'unique_brands': unique_brands
})

# Drop user_id before clustering
X = user_df.drop(columns=['user_id'])

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Elbow method
wcss = [] # Within-cluster sum of squares
for k in range(1, 31):
    kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

# Plot
plt.figure(figsize=(16, 6))
plt.subplot(1, 2, 1)
plt.plot(range(1, 31), wcss, 'bo-')
plt.axvline(x=9, linestyle='--', color='red', label='Optimal k')
plt.title('Elbow Method (1-30 clusters)')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('WCSS')
plt.grid(True)

# Elbow method
wcss = []
for k in range(1, 16):
    kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

# Plot
plt.subplot(1, 2, 2)
plt.plot(range(1, 16), wcss, 'bo-')
plt.axvline(x=9, linestyle='--', color='red', label='Optimal k')
plt.title('Elbow Method (1-15 clusters)')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('WCSS')
plt.grid(True)
plt.show()