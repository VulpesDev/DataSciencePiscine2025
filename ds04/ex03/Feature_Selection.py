import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant

# Example dataframe
df = pd.read_csv('./Train_knight.csv')

# Encode target if needed
df['knight'] = df['knight'].map({'Jedi': 1, 'Sith': 0})

# Select only numeric features
numeric_df = df.select_dtypes(include='number')

# Add constant (intercept) term
X = add_constant(numeric_df)

# Calculate VIF for each variable
vif_data = pd.DataFrame()
vif_data[""] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
vif_data["Tolerance"] = 1 / vif_data["VIF"]

print(vif_data.to_string(index=False))

#Check for practical values
filtered_values = vif_data[vif_data['VIF'] < 5]
print(filtered_values.to_string(index=False))



