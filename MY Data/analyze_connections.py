import pandas as pd

# Correct file path
file_path = "/Users/pconnor/Desktop/Custom GPT Files/LinkedIn Data Analyzer/Connections.csv"

try:
    # Use skiprows to skip the metadata rows
    data = pd.read_csv(file_path, skiprows=3)
    print(data.head())  # Display the first few rows
except Exception as e:
    print(f"Error loading file: {e}")