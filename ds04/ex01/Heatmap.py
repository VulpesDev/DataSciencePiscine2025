import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# Load and prepare data
pd.set_option('display.max_columns', None)
df = pd.read_csv('./Train_knight.csv')

# Encode target variable
df['knight'] = df['knight'].map({'Jedi': 0, 'Sith': 1})

# Select numeric columns
numeric_cols = df.select_dtypes(include='number').columns

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[numeric_cols])
X_scaled_df = pd.DataFrame(X_scaled, columns=numeric_cols)

# Compute and visualize correlation matrix
correlations = X_scaled_df.corr()

print(correlations)

plt.figure(figsize=(10, 8))
sns.heatmap(correlations, cmap='rocket', annot=False, xticklabels=numeric_cols, yticklabels=numeric_cols)
plt.title("Feature Correlation Matrix")
plt.show()
