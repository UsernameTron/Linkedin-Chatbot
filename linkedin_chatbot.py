import pdfplumber
import streamlit as st
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Streamlit app title
st.title("LinkedIn Chatbot")

# --- Section: File Uploads ---
st.header("Upload Your Data Files")

feed_file = st.file_uploader("Upload Feed File (PDF)", type=['pdf'])
connections_file = st.file_uploader("Upload Connections File (CSV)", type=['csv'])
messages_file = st.file_uploader("Upload Messages File (CSV)", type=['csv'])
content_file = st.file_uploader("Upload Date-Specific Content File (Excel)", type=['xlsx'])
invitations_file = st.file_uploader("Upload Invitations File (CSV)", type=['csv'])

# Initialize session state for data and messages
st.session_state['feed_data'] = st.session_state.get('feed_data')
st.session_state['connections_data'] = st.session_state.get('connections_data')
st.session_state['messages_data'] = st.session_state.get('messages_data')
st.session_state['content_data'] = st.session_state.get('content_data', {})
st.session_state['invitations_data'] = st.session_state.get('invitations_data')
st.session_state['messages'] = st.session_state.get('messages', [])

# --- Helper Functions ---

def categorize_posts(feed_text):
    """
    Categorizes posts from the feed text into predefined categories.

    Parameters:
    feed_text (str): The text extracted from the feed PDF.

    Returns:
    dict: A dictionary with categories as keys and lists of posts as values.
    """
    categories = ['Promotional Content', 'Educational Content', 'Thought Leadership', 'Personal Updates', 'Uncategorized']
    posts = feed_text.split("\n")
    categorized_posts = {category: [] for category in categories}
    
    for post in posts:
        # Extract engagements and usernames from the post text
        # Example extraction logic (replace with actual logic based on your data format)
        engagements = {
            "likes": int(post.split("Likes:")[1].split()[0]) if "Likes:" in post else 0,
            "comments": int(post.split("Comments:")[1].split()[0]) if "Comments:" in post else 0
        }
        username = post.split("Posted by:")[1].split()[0] if "Posted by:" in post else "Unknown"
        
        post_detail = {
            "text": post,
            "engagements": engagements,
            "username": username
        }
        
        # Categorize the post (this is a placeholder logic)
        if "promo" in post.lower():
            categorized_posts['Promotional Content'].append(post_detail)
        elif "learn" in post.lower():
            categorized_posts['Educational Content'].append(post_detail)
        elif "thought" in post.lower():
            categorized_posts['Thought Leadership'].append(post_detail)
        elif "update" in post.lower():
            categorized_posts['Personal Updates'].append(post_detail)
        else:
            categorized_posts['Uncategorized'].append(post_detail)
    
    return categorized_posts

# Example usage of categorize_posts function
if feed_file is not None:
    with pdfplumber.open(feed_file) as pdf:
        first_page = pdf.pages[0]
        feed_text = first_page.extract_text()
        categorized_posts = categorize_posts(feed_text)
        st.write(categorized_posts)