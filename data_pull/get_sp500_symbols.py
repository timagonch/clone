# Import Packages
import requests
from bs4 import BeautifulSoup
import pickle

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

# Pickle the list of S&P 500 symbols
with open('sp500_symbols.pkl', 'wb') as file:
    pickle.dump(sp500_symbols, file)