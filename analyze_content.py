import warnings
import pandas as pd

# Suppress specific warning
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# Define file path
file_path = "/Users/pconnor/Desktop/Custom GPT Files/LinkedIn Data Analyzer/Content_2024-08-25_2024-11-22_C. PeteConnor MS, CCCM (1).xlsx"

# Load each tab
try:
    discovery_data = pd.read_excel(file_path, sheet_name="DISCOVERY")
    engagement_data = pd.read_excel(file_path, sheet_name="ENGAGEMENT")
    top_posts_data = pd.read_excel(file_path, sheet_name="TOP POSTS")
    followers_data = pd.read_excel(file_path, sheet_name="FOLLOWERS")
    demographics_data = pd.read_excel(file_path, sheet_name="DEMOGRAPHICS")

    # Display the first few rows of each sheet
    print("--- DISCOVERY ---")
    print(discovery_data.head())

    print("\n--- ENGAGEMENT ---")
    print(engagement_data.head())

    print("\n--- TOP POSTS ---")
    print(top_posts_data.head())

    print("\n--- FOLLOWERS ---")
    print(followers_data.head())

    print("\n--- DEMOGRAPHICS ---")
    print(demographics_data.head())

except Exception as e:
    print(f"Error loading Excel file: {e}")