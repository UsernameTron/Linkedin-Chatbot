import pandas as pd
import matplotlib.pyplot as plt

# File path
file_path = "/Users/pconnor/Desktop/Custom GPT Files/LinkedIn Data Analyzer/Connections.csv"

try:
    # Load data
    data = pd.read_csv(file_path, skiprows=3)
    
    # Ensure 'Connected On' column is in datetime format
    data['Connected On'] = pd.to_datetime(data['Connected On'], errors='coerce')
    data = data.dropna(subset=['Connected On'])  # Remove rows with invalid dates

    # Extract the year of connection
    data['Year'] = data['Connected On'].dt.year

    # --- Visualization 1: Connection Growth Over Time ---
    yearly_connections = data['Year'].value_counts().sort_index()
    plt.figure(figsize=(12, 6))
    plt.bar(yearly_connections.index, yearly_connections.values, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title('Connection Growth Over Time', fontsize=16)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Number of Connections', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    # --- Visualization 2: Top Companies ---
    top_companies = data['Company'].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    top_companies.plot(kind='barh', color='orange', edgecolor='black', alpha=0.7)
    plt.title('Top 10 Companies in Your Connections', fontsize=16)
    plt.xlabel('Number of Connections', fontsize=12)
    plt.ylabel('Company', fontsize=12)
    plt.tight_layout()
    plt.show()

    # --- Visualization 3: Top Job Titles ---
    top_titles = data['Position'].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    top_titles.plot(kind='barh', color='green', edgecolor='black', alpha=0.7)
    plt.title('Top 10 Job Titles in Your Connections', fontsize=16)
    plt.xlabel('Number of Connections', fontsize=12)
    plt.ylabel('Job Title', fontsize=12)
    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Error loading or processing file: {e}")