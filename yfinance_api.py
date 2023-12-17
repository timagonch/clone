import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Define the URL for the S&P 500 companies Wikipedia page
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

# Make the HTTP GET request and bypass SSL certificate verification
response = requests.get(url, verify=False)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing the S&P 500 symbols
table = soup.find('table', {'class': 'wikitable sortable'})

# Extract the symbols from the table
sp500_symbols = []
for row in table.find_all('tr')[1:]:
    symbol = row.find_all('td')[0].text.strip()
    sp500_symbols.append(symbol)

# Define the date range (last 5 years)
start_date = '2023-12-10'  # Change this according to your requirements
end_date = '2023-12-17'    # Change this according to your requirements

# Create an empty DataFrame to store the historical data
sp500_data = pd.DataFrame()

# Loop through each symbol in the S&P 500 list and fetch historical data
for symbol in sp500_symbols:
    try:
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        if not stock_data.empty:
            stock_data = stock_data[['Adj Close']].rename(columns={'Adj Close': symbol})
            sp500_data = pd.concat([sp500_data, stock_data], axis=1)
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")

# Display the first few rows of the combined DataFrame
print(sp500_data.head())

sp500_data.to_pickle('sp500_data.pkl')