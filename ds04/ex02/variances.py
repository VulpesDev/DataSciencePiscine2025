import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv('./Train_knight.csv')

# Encode target if needed
df['knight'] = df['knight'].map({'Jedi': 1, 'Sith': 0})

# Select only numeric features
numeric_df = df.select_dtypes(include='number')

# Scale features to 0–1 range
scaler = StandardScaler()
X_scaled = scaler.fit_transform(numeric_df)

# Apply PCA
pca = PCA()
pca.fit(X_scaled)

# Get explained variance
explained_var = pca.explained_variance_
explained_ratio = pca.explained_variance_ratio_
cumulative_variance = explained_ratio.cumsum()

# Convert to DataFrame
pca_df = pd.DataFrame({
    'Component': range(1, len(explained_var)+1),
    'Explained Variance': explained_var,
    'Explained Variance Ratio (%)': explained_ratio * 100,
    'Cumulative Variance (%)': cumulative_variance * 100
})

# Print example values
print('Variances (Percentage):\r\n', pca_df['Explained Variance Ratio (%)'].to_numpy())
print('Cumulative Variances (Percentage):\r\n', pca_df['Cumulative Variance (%)'].to_numpy())

# Plot cumulative explained variance
plt.figure(figsize=(8, 8))
plt.plot(pca_df['Component'], pca_df['Cumulative Variance (%)'], marker='')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Variance (%)')
plt.title('PCA - Cumulative Explained Variance')
plt.ylim(min(pca_df['Cumulative Variance (%)']) - 5, 100 + 5)
plt.show()
