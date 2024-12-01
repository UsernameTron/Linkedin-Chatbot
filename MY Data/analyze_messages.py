import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load messages data
file_path = "messages.csv"

try:
    # Read the CSV file
    messages_data = pd.read_csv(file_path)
    
    # Convert 'DATE' to datetime
    messages_data['DATE'] = pd.to_datetime(messages_data['DATE'], errors='coerce')
    
    # Define your name to identify outbound messages
    self_name = "C. Pete Connor MS, CCCM"  # Replace with your name as it appears in the dataset
    
    # Categorize messages as Inbound or Outbound
    messages_data['Direction'] = messages_data['TO'].apply(lambda x: 'Outbound' if x == self_name else 'Inbound')
    
    # Analyze trends by month
    messages_data['Year-Month'] = messages_data['DATE'].dt.to_period('M')
    message_trends = messages_data.groupby(['Year-Month', 'Direction']).size().unstack(fill_value=0)
    
    # Identify top contacts by frequency
    user_interactions = pd.concat([messages_data['FROM'], messages_data['TO']])
    user_interactions = user_interactions[~user_interactions.str.contains("LinkedIn Member", na=False)]
    top_contacts = user_interactions.value_counts().head(10)
    
    print("\nTop 10 Contacts by Message Frequency:")
    print(top_contacts)
    
    # Extract keywords from content
    if 'CONTENT' in messages_data.columns and not messages_data['CONTENT'].isna().all():
        content_keywords = (
            messages_data['CONTENT']
            .dropna()
            .str.lower()
            .str.split(expand=True)
            .stack()
            .value_counts()
            .head(10)
        )
        print("\nTop Keywords in Message Content:")
        print(content_keywords)
    else:
        print("\nNo valid content found for keyword analysis.")
    
except Exception as e:
    print(f"An error occurred: {e}")