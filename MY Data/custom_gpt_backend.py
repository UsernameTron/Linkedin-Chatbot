import os
import matplotlib.pyplot as plt
import pandas as pd
import PyPDF2

# Define the analysis workflow
ANALYSIS_WORKFLOW = [
    {"file_name": "Feed.pdf", "script": "process_feed_pdf", "description": "Analyze your LinkedIn feed content for post categories and trends."},
    {"file_name": "Connections.csv", "script": "analyze_connections", "description": "Analyze your LinkedIn connections to identify trends and underrepresented industries."},
    {"file_name": "messages.csv", "script": "process_messages", "description": "Analyze your LinkedIn messages for trends and key communication patterns."},
    {"file_name": "Content.xlsx", "script": "analyze_content", "description": "Analyze your LinkedIn content performance, including impressions and engagements."},
    {"file_name": "Rich_Media.csv", "script": "rich_media_analyze", "description": "Analyze the performance of your videos, images, and documents on LinkedIn."},
]

# Function to process PDF files
def process_pdf(file_path):
    try:
        with open(file_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = "".join(page.extract_text() for page in reader.pages)
            return text
    except Exception as e:
        return f"Error reading PDF file: {e}"

# Function to handle Feed.pdf
def process_feed_pdf(file_path):
    # Example: Simulating feed analysis logic
    feed_data = process_pdf(file_path)
    if "Error" in feed_data:
        return feed_data
    categories = ["Promotional Content", "Educational Content", "Thought Leadership", "Personal Updates", "Uncategorized"]
    num_posts = [18, 9, 6, 1, 2]  # Simulated data
    plt.bar(categories, num_posts)
    plt.title("Feed Analysis: Number of Posts by Category")
    plt.show()
    return "Feed analysis completed with simulated data."

# Function to analyze connections
def analyze_connections(file_path):
    try:
        data = pd.read_csv(file_path, skiprows=3)
        data['Connected On'] = pd.to_datetime(data['Connected On'], errors='coerce')
        yearly_trends = data['Connected On'].dt.year.value_counts().sort_index()
        yearly_trends.plot(kind="bar", title="Connections Growth by Year")
        plt.show()
        return "Connections analysis completed."
    except Exception as e:
        return f"Error processing Connections.csv: {e}"

# Function to handle messages.csv
def process_messages(file_path):
    try:
        data = pd.read_csv(file_path)
        data['DATE'] = pd.to_datetime(data['DATE'], errors='coerce')
        data['Year-Month'] = data['DATE'].dt.to_period('M')
        trends = data.groupby(['Year-Month']).size()
        trends.plot(title="Message Trends Over Time")
        plt.show()
        return "Message analysis completed."
    except Exception as e:
        return f"Error processing messages.csv: {e}"

# Function to analyze content.xlsx
def analyze_content(file_path):
    try:
        data = pd.read_excel(file_path)
        data['Engagement Rate'] = data['Engagement'] / data['Impressions'] * 100
        avg_engagement = data.groupby('Content Type')['Engagement Rate'].mean()
        avg_engagement.plot(kind="bar", title="Average Engagement Rate by Content Type")
        plt.show()
        return "Content analysis completed."
    except Exception as e:
        return f"Error processing Content.xlsx: {e}"

# Function to analyze rich media
def rich_media_analyze(file_path):
    try:
        data = pd.read_csv(file_path)
        media_types = data['Media Type'].value_counts()
        media_types.plot(kind="bar", title="Media Type Distribution")
        plt.show()
        return "Rich media analysis completed."
    except Exception as e:
        return f"Error processing Rich_Media.csv: {e}"

# Main function to guide users
def main():
    print("Welcome! I will guide you through a step-by-step LinkedIn data analysis process.")
    for step in ANALYSIS_WORKFLOW:
        print(f"\nStep: {step['description']}")
        file_path = input(f"Please upload your {step['file_name']} file (enter the full path): ").strip()
        
        if not os.path.exists(file_path):
            choice = input(f"File {step['file_name']} not found. Would you like to skip this step? (yes/no): ").strip().lower()
            if choice == "yes":
                print(f"Skipping {step['file_name']} analysis.")
                continue
            else:
                print("Please ensure the file exists and try again.")
                break
        
        print(f"Processing {step['file_name']}...")
        script_name = step['script']
        if script_name == "process_feed_pdf":
            print(process_feed_pdf(file_path))
        elif script_name == "analyze_connections":
            print(analyze_connections(file_path))
        elif script_name == "process_messages":
            print(process_messages(file_path))
        elif script_name == "analyze_content":
            print(analyze_content(file_path))
        elif script_name == "rich_media_analyze":
            print(rich_media_analyze(file_path))
        else:
            print(f"Script for {step['file_name']} not found.")

    print("\nAnalysis complete! Thank you for providing your data.")

if __name__ == "__main__":
    main()
