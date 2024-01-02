# Importing common python packages
# from setup.common_imports import np, pd, pickle # look into the error
import pandas as pd 
import numpy as np
import pickle

# Importing the SP500 wide dataframe file from the pickle file
pickle_folder_path = '/Users/lilygoncharov/Documents/Z/code/AI-Trading/data_pull/'
pickle_name = 'monthly_sp500_full_data.pkl'
df = pd.read_pickle(pickle_folder_path+pickle_name)

# Split the column names and create a MultiIndex
df.columns = pd.MultiIndex.from_tuples([tuple(col.split('_')) for col in df.columns])

# Stack the inner level of the columns, bringing the stock names into a single column
df_long = df.stack(level=0).reset_index()

# Rename the columns for clarity
df_long.columns = ['Date', 'Stock', 'Close', 'High', 'Low', 'Open', 'Volume']

# Sort by Date and Stock for better organization
df_long.sort_values(by=['Date', 'Stock'], inplace=True)

# Pickle the DataFrame
df_long.to_pickle('/Users/lilygoncharov/Documents/Z/code/AI-Trading/data_processing/df_long.pkl')