import pandas as pd

# Load object from pickle file
loaded_object = pd.read_pickle('sp500_symbols.pkl')

# Convert loaded object to a DataFrame
if not isinstance(loaded_object, pd.DataFrame):
    loaded_object = pd.DataFrame(loaded_object)

# Now, 'loaded_object' will be a DataFrame
print(loaded_object.head())  # Assuming you want to print the DataFrame content
