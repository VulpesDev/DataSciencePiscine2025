import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

df_train = pd.read_csv('../Train_knight.csv')
df_test = pd.read_csv('../Test_knight.csv')


numeric_cols_train = df_train.select_dtypes(include='number').columns
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(df_train[numeric_cols_train])
X_scaled_df = pd.DataFrame(X_scaled, columns=numeric_cols_train)
print(X_scaled_df.sort_values(by='Sensitivity', ascending=False))

X_scaled_df['knight'] = df_train['knight']

plt.figure(figsize=(6, 10))
plt.subplots_adjust(hspace=0.5)

plt.subplot(2, 1, 1)
sns.scatterplot(data=X_scaled_df, x='Push', y='Deflection', hue='knight', alpha=0.6, palette=['blue', 'red'])
plt.legend()
plt.title("Push vs Deflection by Knight Status")


numeric_cols_train = df_test.select_dtypes(include='number').columns
plt.subplot(2, 1, 2)
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(df_test[numeric_cols_train])
X_scaled_df = pd.DataFrame(X_scaled, columns=numeric_cols_train)

print(X_scaled_df.sort_values(by='Sensitivity', ascending=False))

sns.scatterplot(data=X_scaled_df, x='Push', y='Deflection', alpha=0.6, color='green')
plt.legend(['Knight'], loc='upper left', fontsize=12)
plt.title("Push vs Deflection for Knights")
plt.show()