import pandas as pd

# Load CSV file
csv_file_path = '/Users/tjgon/Desktop/test.csv'  # Replace 'your_file.csv' with the actual path to your CSV file
df = pd.read_csv(csv_file_path)

# Do some operations on the DataFrame if needed
# For example, you can add a new column or filter rows

# Save DataFrame to a new CSV file
output_csv_path = './timon/output_file.csv'  # Replace 'output_file.csv' with the desired output file path
df.to_csv(output_csv_path, index=False)

print(f"CSV file saved to: {output_csv_path}")