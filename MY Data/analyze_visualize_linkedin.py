import pandas as pd
import matplotlib.pyplot as plt
import warnings

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# File path to the Excel data
file_path = "/Users/pconnor/Desktop/Custom GPT Files/LinkedIn Data Analyzer/Content_2024-08-25_2024-11-22_C. PeteConnor MS, CCCM (1).xlsx"

try:
    # Load DISCOVERY data and process it
    discovery_data = pd.read_excel(file_path, sheet_name="DISCOVERY")
    discovery_data.columns = ["Metric", "Value"]  # Rename columns
    print("--- DISCOVERY ---")
    print(discovery_data)

    # Visualize DISCOVERY
    discovery_data.plot(kind='bar', x='Metric', y='Value', legend=False)
    plt.title("Discovery Metrics")
    plt.ylabel("Value")
    plt.show()

except Exception as e:
    print(f"Error processing or visualizing DISCOVERY: {e}")

try:
    # Load ENGAGEMENT data and process it
    engagement_data = pd.read_excel(file_path, sheet_name="ENGAGEMENT")
    print("\n--- ENGAGEMENT ---")
    print(engagement_data)

    # Visualize ENGAGEMENT: Trends in Engagements and Impressions
    engagement_data['Date'] = pd.to_datetime(engagement_data['Date'])
    plt.figure(figsize=(10, 6))
    plt.plot(engagement_data['Date'], engagement_data['Impressions'], label='Impressions')
    plt.plot(engagement_data['Date'], engagement_data['Engagements'], label='Engagements', linestyle='--')
    plt.title("Engagement Over Time")
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.legend()
    plt.show()

except Exception as e:
    print(f"Error processing or visualizing ENGAGEMENT: {e}")

try:
    # Load TOP POSTS data and process it
    top_posts_data = pd.read_excel(file_path, sheet_name="TOP POSTS", skiprows=2)
    top_posts_data.columns = ["Post URL", "Date", "Engagements", "Additional Info", "Comparison URL", "Comparison Date", "Comparison Views"]
    print("\n--- TOP POSTS ---")
    print(top_posts_data.head())

    # Visualize TOP POSTS: Engagements of Top Posts
    plt.figure(figsize=(10, 6))
    top_posts_data['Engagements'].plot(kind='bar', color='skyblue', alpha=0.7)
    plt.title("Top Posts Engagement")
    plt.xlabel("Posts")
    plt.ylabel("Engagement Count")
    plt.show()

except Exception as e:
    print(f"Error processing or visualizing TOP POSTS: {e}")

try:
    # Load FOLLOWERS data and process it
    followers_data = pd.read_excel(file_path, sheet_name="FOLLOWERS", skiprows=2)
    followers_data.columns = ["Date", "New Followers"]
    print("\n--- FOLLOWERS ---")
    print(followers_data)

    # Visualize FOLLOWERS: Followers Over Time
    followers_data['Date'] = pd.to_datetime(followers_data['Date'])
    plt.figure(figsize=(10, 6))
    plt.plot(followers_data['Date'], followers_data['New Followers'], label='New Followers', color='green')
    plt.title("New Followers Over Time")
    plt.xlabel("Date")
    plt.ylabel("New Followers")
    plt.legend()
    plt.show()

except Exception as e:
    print(f"Error processing or visualizing FOLLOWERS: {e}")

try:
    # Load DEMOGRAPHICS data and process it
    demographics_data = pd.read_excel(file_path, sheet_name="DEMOGRAPHICS")
    demographics_data["Percentage"] = demographics_data["Percentage"].str.replace('< 1', '0.5')  # Replace '< 1%' with '0.5'
    demographics_data["Percentage"] = demographics_data["Percentage"].str.rstrip('%').astype(float) / 100  # Convert to float
    print("\n--- DEMOGRAPHICS ---")
    print(demographics_data)

    # Visualize DEMOGRAPHICS: Top Job Titles
    job_titles = demographics_data[demographics_data["Top Demographics"] == "Job titles"]
    plt.figure(figsize=(10, 6))
    plt.bar(job_titles["Value"], job_titles["Percentage"], color='purple', alpha=0.6)
    plt.title("Top Job Titles by Percentage")
    plt.xlabel("Job Titles")
    plt.ylabel("Percentage")
    plt.xticks(rotation=45, ha='right')
    plt.show()

except Exception as e:
    print(f"Error processing or visualizing DEMOGRAPHICS: {e}")