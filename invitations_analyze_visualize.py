import pandas as pd
import matplotlib.pyplot as plt

# File path
file_path = "/Users/pconnor/Desktop/Custom GPT Files/LinkedIn Data Analyzer/Invitations.csv"

# Load the data
try:
    data = pd.read_csv(file_path)
    print(f"Dataset Columns: {data.columns}")

    # Convert 'Sent At' column to datetime format
    try:
        data['Sent At'] = pd.to_datetime(data['Sent At'], format='%m/%d/%y, %I:%M %p', errors='coerce')  # Corrected line
    except Exception as e:
        print(f"An error occurred while parsing datetime: {e}")
    
    # Filter out rows with invalid datetime
    data = data.dropna(subset=['Sent At'])

    # Sort data by 'Sent At'
    data = data.sort_values(by='Sent At')

    # Extract date from 'Sent At' for grouping
    data['Date'] = data['Sent At'].dt.date

    # Count invitations sent per day
    daily_invitations = data.groupby('Date').size().reset_index(name='Count')

    # Plot the data
    plt.figure(figsize=(12, 6))
    plt.plot(daily_invitations['Date'], daily_invitations['Count'], marker='o')
    plt.title('Daily Invitations Sent', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Number of Invitations', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Save the processed data to a CSV
    processed_file_path = "/Users/pconnor/Desktop/Custom GPT Files/LinkedIn Data Analyzer/Processed_Invitations.csv"
    daily_invitations.to_csv(processed_file_path, index=False)
    print(f"Processed data saved to {processed_file_path}")

except Exception as e:
    print(f"An error occurred: {e}")