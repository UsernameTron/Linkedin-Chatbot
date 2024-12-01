import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import warnings
from streamlit_chat import message
import re
import io
import pdfplumber

# Ensure compatibility with Streamlit deployment
plt.switch_backend('Agg')  # Use non-interactive backend for matplotlib

warnings.filterwarnings("ignore")

st.title("LinkedIn Data Analyzer")

# --- File Uploads ---
st.header("Upload Your Data Files")

feed_file = st.file_uploader("Upload Feed PDF File", type=['pdf'])
connections_file = st.file_uploader("Upload Connections CSV File", type=['csv'])
messages_file = st.file_uploader("Upload Messages CSV File", type=['csv'])
content_file = st.file_uploader("Upload Date-Specific Content Excel File", type=['xlsx'])
invitations_file = st.file_uploader("Upload Invitations CSV File", type=['csv'])

# Initialize session state for data and messages
session_keys = {
    'feed_data': None,
    'connections_data': None,
    'messages_data': None,
    'content_data': {},
    'invitations_data': None,
    'messages': [],
}

for key, default_value in session_keys.items():
    if key not in st.session_state:
        st.session_state[key] = default_value

# --- Helper Functions ---
def extract_text_from_pdf(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
    return text

# --- File Processing ---
# Place all feed, connections, messages, content, and invitation processing here.
# ...

# Example: Feed PDF Analysis
if feed_file is not None:
    try:
        st.header("Feed Content Analysis")
        feed_text = extract_text_from_pdf(feed_file)
        st.write("Feed Content Extracted:")
        st.write(feed_text[:500])  # Display first 500 characters for preview

        # Example Placeholder Data
        categories = ['Promotional Content', 'Educational Content', 'Thought Leadership', 'Personal Updates', 'Uncategorized']
        num_posts = [18, 9, 6, 1, 2]

        # Bar Chart
        fig_feed_bar, ax_feed_bar = plt.subplots()
        ax_feed_bar.bar(categories, num_posts, color=['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854'], edgecolor='black')
        ax_feed_bar.set_title('Number of Posts by Category')
        ax_feed_bar.set_xlabel('Category')
        ax_feed_bar.set_ylabel('Number of Posts')
        st.pyplot(fig_feed_bar)

        # Pie Chart
        fig_feed_pie, ax_feed_pie = plt.subplots()
        ax_feed_pie.pie(num_posts, labels=categories, autopct='%1.1f%%', startangle=140)
        ax_feed_pie.set_title('Distribution of Posts by Category')
        st.pyplot(fig_feed_pie)

    except Exception as e:
        st.error(f"Error processing Feed PDF data: {e}")

# --- Connections Data ---
if connections_file is not None:
    @st.cache_data
    def load_connections(file):
        try:
            data = pd.read_csv(file, skiprows=3)
            data.columns = data.columns.str.strip()
            return data
        except Exception as e:
            st.error(f"Error loading connections CSV: {e}")
            return pd.DataFrame()

    connections_data = load_connections(connections_file)
    st.header("Connections Data Analysis")
    if not connections_data.empty:
        st.write(connections_data.head())

# Additional processing for messages, content, invitations...

# --- Chat Interface ---
st.header("Ask Questions About Your Data")
st.write("""
    Example questions:
    - What are my top performing posts?
    - What are the trends in my follower demographics?
""")

for i, msg in enumerate(st.session_state['messages']):
    if msg['is_user']:
        message(msg['content'], is_user=True, key=f"user_{i}")
    else:
        message(msg['content'], key=f"bot_{i}")

user_input = st.text_input("Ask a question:", key="input")

if user_input:
    st.session_state['messages'].append({'content': user_input, 'is_user': True})
    # Placeholder for response logic
    st.session_state['messages'].append({'content': "Response placeholder", 'is_user': False})