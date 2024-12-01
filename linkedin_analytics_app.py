import os
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for non-interactive plotting
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import warnings
from streamlit_chat import message
import re
import io
import pdfplumber

warnings.filterwarnings("ignore")

# Initialize session state variables
if 'feed_data' not in st.session_state:
    st.session_state['feed_data'] = None
if 'connections_data' not in st.session_state:
    st.session_state['connections_data'] = None
if 'messages_data' not in st.session_state:
    st.session_state['messages_data'] = None
if 'content_data' not in st.session_state:
    st.session_state['content_data'] = {}
if 'invitations_data' not in st.session_state:
    st.session_state['invitations_data'] = None
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

st.title("LinkedIn Data Analyzer")

# --- File Uploads ---
st.header("Upload Your Data Files")

feed_file = st.file_uploader("Upload Feed PDF File", type=['pdf'])
connections_file = st.file_uploader("Upload Connections CSV File", type=['csv'])
messages_file = st.file_uploader("Upload Messages CSV File", type=['csv'])
content_file = st.file_uploader("Upload Date-Specific Content Excel File", type=['xlsx'])
invitations_file = st.file_uploader("Upload Invitations CSV File", type=['csv'])

# --- Helper Functions ---
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# (All other code remains unchanged and follows here.)

# --- Chat Interface ---
st.header("Ask Questions About Your Data")
st.write("""
    You can ask questions like:
    - What are my top performing posts?
    - What are the trends in my follower demographics?
    - How can I improve my networking strategies?
""")

# Iterate through and display messages
for i, msg in enumerate(st.session_state['messages']):
    if msg['is_user']:
        message(msg['content'], is_user=True, key=str(i) + '_user')
    else:
        message(msg['content'], key=str(i))

# Accept user input
user_input = st.text_input("You:", key='input')

if user_input:
    st.session_state['messages'].append({'content': user_input, 'is_user': True})

    # Process the user's query
    def process_user_query(query):
        query_lower = query.lower()

        if 'top performing posts' in query_lower:
            return get_top_performing_posts()
        elif 'follower demographics' in query_lower:
            return get_follower_demographics()
        elif 'improve my networking' in query_lower:
            return provide_networking_recommendations()
        else:
            return "I'm sorry, I didn't understand your question. Please try asking in a different way."

    def get_top_performing_posts():
        if 'TOP POSTS' in st.session_state['content_data']:
            top_posts_data = st.session_state['content_data']['TOP POSTS']
            if {'Post URL', 'Engagements'}.issubset(top_posts_data.columns):
                top_posts = top_posts_data[['Post URL', 'Engagements']].sort_values(by='Engagements', ascending=False).head(5)
                return top_posts.reset_index(drop=True).to_string(index=False)
            else:
                return "Required columns not found in Top Posts data."
        else:
            return "Top Posts data not available. Please upload your content performance data."

    def get_follower_demographics():
        if 'DEMOGRAPHICS' in st.session_state['content_data']:
            demographics_data = st.session_state['content_data']['DEMOGRAPHICS']
            demographics_data['Percentage'] = demographics_data['Percentage'].astype(str)
            demographics_data['Percentage'] = demographics_data['Percentage'].str.replace('%', '').str.strip()
            demographics_data['Percentage'] = pd.to_numeric(demographics_data['Percentage'], errors='coerce')

            result = ""
            for demo_type in demographics_data['Demographic Type'].unique():
                demo_data = demographics_data[demographics_data['Demographic Type'] == demo_type]
                demo_data = demo_data.dropna(subset=['Percentage'])
                demo_data['Percentage'] = demo_data['Percentage'].astype(float)
                top_demo = demo_data.sort_values(by='Percentage', ascending=False).head(5)
                result += f"Top {demo_type}:\n"
                for idx, row in top_demo.iterrows():
                    result += f"- {row['Demographic']}: {row['Percentage']}%\n"
                result += "\n"
            return result
        else:
            return "Demographics data not available. Please upload your content performance data."

    def provide_networking_recommendations():
        if st.session_state['connections_data'] is not None:
            connections_data = st.session_state['connections_data']
            recommendations = ("Based on your connections data:\n"
                                "- Engage with underrepresented industries or companies to diversify your network.\n"
                                "- Consider reaching out to connections in growing industries.\n"
                                "- Attend networking events to increase connections.")
            return recommendations
        else:
            return "Connections data not available. Please upload your connections data."

    response = process_user_query(user_input)
    st.session_state['messages'].append({'content': response, 'is_user': False})