import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv('../Train_knight.csv')

train_df, val_df = train_test_split(df, test_size=0.2, random_state=42, shuffle=True)

train_df.to_csv('Training_knight.csv', index=False)
val_df.to_csv('Validation_knight.csv', index=False)

print(f"Training set: {len(train_df)} rows ({len(train_df)/len(df)*100:.2f}%)")
print(f"Validation set: {len(val_df)} rows ({len(val_df)/len(df)*100:.2f}%)")
