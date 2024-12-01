import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import warnings

# Suppress warnings from openpyxl
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# --- File Paths ---
connections_file = "/Users/pconnor/Desktop/Custom GPT Files/LinkedIn Data Analyzer/Connections.csv"
content_file = "/Users/pconnor/Desktop/Custom GPT Files/LinkedIn Data Analyzer/Content_2024-08-25_2024-11-22_C. PeteConnor MS, CCCM (1).xlsx"
messages_file = "/Users/pconnor/Desktop/Custom GPT Files/LinkedIn Data Analyzer/messages.csv"

# --- CONNECTIONS DATA ANALYSIS ---
try:
    connections_data = pd.read_csv(connections_file, skiprows=2)
    connections_data.columns = connections_data.columns.str.strip()

    # Verify required columns
    required_columns = {'Position', 'Company', 'Connected On'}
    if not required_columns.issubset(connections_data.columns):
        print(f"Error: Missing columns {required_columns - set(connections_data.columns)}")
    else:
        # Process connections data
        connections_data['Connected On'] = pd.to_datetime(connections_data['Connected On'], errors='coerce')
        connections_data['Year'] = connections_data['Connected On'].dt.year

        # Yearly Growth Visualization (Bar)
        yearly_trends = connections_data.groupby('Year').size()
        plt.figure(figsize=(12, 6))
        yearly_trends.plot(kind='bar', color='skyblue', alpha=0.8, edgecolor='black')
        plt.title('Yearly Growth in Connections', fontsize=16)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Number of Connections', fontsize=12)
        plt.tight_layout()
        plt.show()

        # Word Cloud: Positions
        wordcloud_positions = WordCloud(width=800, height=400, background_color='white').generate(" ".join(connections_data['Position'].dropna()))
        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud_positions, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud: Positions in Connections', fontsize=16)
        plt.tight_layout()
        plt.show()

        # Underrepresented Companies (Horizontal Bar)
        underrepresented_companies = connections_data['Company'].value_counts()
        underrepresented_companies = underrepresented_companies[underrepresented_companies == 1].head(10)
        plt.figure(figsize=(10, 6))
        underrepresented_companies.plot(kind='barh', color='orange', alpha=0.8, edgecolor='black')
        plt.title('Underrepresented Companies (Least Represented)', fontsize=16)
        plt.xlabel('Number of Connections', fontsize=12)
        plt.ylabel('Company', fontsize=12)
        plt.tight_layout()
        plt.show()

except Exception as e:
    print(f"Error processing Connections data: {e}")

# --- CONTENT PERFORMANCE ANALYSIS ---
try:
    content_data = pd.read_excel(content_file)

    # Verify required columns
    required_columns = {'Impressions', 'Engagement', 'Content Type'}
    if not required_columns.issubset(content_data.columns):
        print(f"Error: Missing columns {required_columns - set(content_data.columns)}")
    else:
        # Calculate engagement rates
        content_data['Engagement Rate'] = content_data['Engagement'] / content_data['Impressions'] * 100
        avg_engagement_rate = content_data.groupby('Content Type')['Engagement Rate'].mean().sort_values(ascending=False)

        # Bar Chart: Engagement Rate by Content Type
        plt.figure(figsize=(12, 6))
        avg_engagement_rate.plot(kind='bar', color='green', alpha=0.8, edgecolor='black')
        plt.title('Average Engagement Rate by Content Type', fontsize=16)
        plt.xlabel('Content Type', fontsize=12)
        plt.ylabel('Engagement Rate (%)', fontsize=12)
        plt.tight_layout()
        plt.show()

        # Pie Chart: Content Distribution
        content_distribution = content_data['Content Type'].value_counts()
        plt.figure(figsize=(10, 6))
        plt.pie(content_distribution, labels=content_distribution.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.tab10.colors)
        plt.title('Content Distribution by Type', fontsize=16)
        plt.tight_layout()
        plt.show()

except Exception as e:
    print(f"Error processing Content Performance data: {e}")

# --- MESSAGING DATA ANALYSIS ---
try:
    messages_data = pd.read_csv(messages_file)
    messages_data['DATE'] = pd.to_datetime(messages_data['DATE'], errors='coerce')

    # Messaging Trends
    self_name = "C. Pete Connor MS, CCCM"
    messages_data['Direction'] = messages_data['TO'].apply(lambda x: 'Outbound' if x == self_name else 'Inbound')
    messages_data['Year-Month'] = messages_data['DATE'].dt.to_period('M')

    message_trends = messages_data.groupby(['Year-Month', 'Direction']).size().unstack(fill_value=0)
    message_trends.plot(kind='line', figsize=(12, 6), marker='o')
    plt.title('Messaging Trends (Inbound vs Outbound)', fontsize=16)
    plt.xlabel('Year-Month', fontsize=12)
    plt.ylabel('Number of Messages', fontsize=12)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Top Keywords from Subjects
    stopwords = {"the", "to", "and", "a", "of", "is", "in", "for", "on", "with", "your", "you", "it", "at", "this", "an", "be"}
    keywords_subjects = pd.Series(" ".join(messages_data['SUBJECT'].fillna("")).lower().split()).value_counts().head(10)
    keywords_subjects = keywords_subjects[~keywords_subjects.index.isin(stopwords)]

    plt.figure(figsize=(10, 6))
    keywords_subjects.plot(kind='bar', color='purple', alpha=0.7)
    plt.title('Top Keywords in Message Subjects', fontsize=16)
    plt.xlabel('Keywords', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Error processing Messaging data: {e}")