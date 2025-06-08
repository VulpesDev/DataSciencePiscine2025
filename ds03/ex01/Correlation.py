import pandas as pd

df = pd.read_csv('../Train_knight.csv')

df['knight_numeric'] = df['knight'].map({'Jedi': 1, 'Sith': 0})  # adjust if values differ

numeric_cols = df.select_dtypes(include='number').columns
correlations = df[numeric_cols].corrwith(df['knight_numeric'])
correlations_sorted = correlations.abs().sort_values(ascending=False)

corr_df = correlations_sorted.to_frame(name='correlation')
corr_df = corr_df.reset_index().rename(columns={'index': 'column'})
corr_df['correlation'] = corr_df['correlation'].round(6)
print(corr_df.to_string(index=False))