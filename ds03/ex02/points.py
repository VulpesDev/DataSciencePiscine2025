import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df_train = pd.read_csv('../Train_knight.csv')
df_test = pd.read_csv('../Test_knight.csv')

plt.figure(figsize=(12, 8))
plt.subplots_adjust(hspace=0.5)

plt.subplot(2,2,1)
sns.scatterplot(data=df_train, x='Empowered', y='Stims', hue='knight', alpha=0.6, palette={'blue', 'red'})
plt.legend()
plt.title("Empowered vs Stims by Knight Status")

plt.subplot(2,2,2)
sns.scatterplot(data=df_train, x='Push', y='Deflection', hue='knight', alpha=0.6, palette=['blue', 'red'])
plt.legend()
plt.title("Push vs Deflection by Knight Status")


plt.subplot(2,2,3)
sns.scatterplot(data=df_test, x='Empowered', y='Stims', alpha=0.6, color='green')
plt.legend(['Knight'], loc='upper left', fontsize=12)
plt.title("Empowered vs Stims for Knights")

plt.subplot(2,2,4)
sns.scatterplot(data=df_test, x='Push', y='Deflection', alpha=0.6, color='green')
plt.legend(['Knight'], loc='upper left', fontsize=12)
plt.title("Push vs Deflection for Knights")
plt.show()

