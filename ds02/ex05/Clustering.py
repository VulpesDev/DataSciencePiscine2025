import os
import psycopg2
from dotenv import load_dotenv
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA


load_dotenv(dotenv_path= '../.env')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

connection = psycopg2.connect(database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host="localhost", port=5432)

cursor = connection.cursor()

cluster_labels = {
    0: "Low Spenders (Minimal Variety)",
    1: "Loyal Regular Buyers",
    2: "Mid-Spend, Brand Explorers",
    3: "Occasional Small Buyers",
    4: "Single Category Shoppers",
    5: "Quiet Newcomers",
    6: "Unengaged Users",
    7: "Budget Variety Shoppers",
    8: "VIP Power Buyers"
}

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
kmeans = KMeans(n_clusters=9, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

user_df['cluster'] = clusters
user_df['cluster_label'] = user_df['cluster'].map(cluster_labels)

summary_with_labels = user_df.groupby(['cluster', 'cluster_label']).mean(numeric_only=True)
pd.set_option('display.max_columns', None)
print(summary_with_labels)

summary_with_labels = summary_with_labels.reset_index()
cluster_counts = user_df['cluster_label'].value_counts().sort_values(ascending=False)

plt.figure(figsize=(14, 6))
sns.barplot(x=cluster_counts.values, y=cluster_counts.index, palette='tab10')
for i, (value, label) in enumerate(zip(cluster_counts.values, cluster_counts.index)):
    plt.text(value + 5, i, str(value), va='center', fontsize=10)
plt.title("Number of Customers per Cluster")
plt.xlabel("Number of Customers")
plt.ylabel("")
plt.tight_layout()
plt.show()


# Reduce your scaled data to 2D for visualization
pca = PCA(n_components=2) #Practical Component Analysis
X_pca = pca.fit_transform(X_scaled)

# Add PCA results to the DataFrame
user_df['pca1'] = X_pca[:, 0]
user_df['pca2'] = X_pca[:, 1]

# Plot using cluster_label
plt.figure(figsize=(10, 7))
sns.scatterplot(data=user_df,
                x='pca1', y='pca2',
                hue='cluster_label',
                palette='tab10', s=50, alpha=0.8)

plt.title("Customer Segments Visualized by Cluster Label")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.legend(title='Cluster Label', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()