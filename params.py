import pandas as pd

# Choose your start and end dates
start_date = '2023-12-10'
end_date = '2023-12-17'

# Data
weekly_sp500 = pd.read_pickle('weekly_sp500_data.pkl')
monthly_sp500 = pd.read_pickle('monthly_sp500_data.pkl')
monthly_sp500_full = pd.read_pickle('monthly_sp500_full_data.pkl')

# Choose your data from the list above
sp500_data = monthly_sp500