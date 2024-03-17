import pandas as pd
df = pd.read_pickle('./data/crypto_coins_list_data.pkl')
print(df.head())
# show all columns names
print(df.columns) 
