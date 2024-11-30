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

st.title("LinkedIn Data Analyzer")

# --- Instructions for Users ---
with st.expander("Click here to see instructions on how to obtain your LinkedIn data files"):
    st.header("Steps to Obtain LinkedIn Data")
    
    st.subheader("Feed Data (Feed.pdf):")
    st.markdown("""
    1. Navigate to your LinkedIn homepage.
    2. Scroll to load recent posts.
    3. Use your browser’s **"Print to PDF"** feature to save the feed as `Feed.pdf`.
    """)
    
    st.subheader("Content Performance Data (Content.xlsx):")
    st.markdown("""
    1. Enable **Creator Mode** on your LinkedIn profile.
    2. Visit your **Analytics > Content**.
    3. Export data for the desired date range as an Excel file (e.g., `Content.xlsx`).
    """)
    
    st.subheader("Connections, Messages, and Invitations Data (Connections.csv, Messages.csv, Invitations.csv):")
    st.markdown("""
    1. Go to **LinkedIn Settings > Data Privacy > "Get a copy of your data."**
    2. Select **Connections**, **Messages**, and **Sent Invitations**.
    3. Download the files as `Connections.csv`, `Messages.csv`, and `Invitations.csv` respectively.
    """)
    
    st.write("Once the data is saved, upload the files here for analysis.")

# --- File Uploads ---
st.header("Upload Your Data Files")

feed_file = st.file_uploader("Upload Feed PDF File", type=['pdf'])
connections_file = st.file_uploader("Upload Connections CSV File", type=['csv'])
messages_file = st.file_uploader("Upload Messages CSV File", type=['csv'])
content_file = st.file_uploader("Upload Date-Specific Content Excel File", type=['xlsx'])
invitation_file = st.file_uploader("Upload Invitations CSV File", type=['csv'])

# Initialize session state for data and messages
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

# --- Helper Functions ---
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# --- 1. Feed.pdf ---
if feed_file is not None:
    try:
        st.header("Feed Content Analysis")
        feed_text = extract_text_from_pdf(feed_file)
        st.write("Feed Content Extracted:")
        st.write(feed_text[:500])  # Display first 500 characters

        # TODO: Implement actual parsing logic based on the structure of your PDF
        # For now, we'll proceed with placeholder data from your provided code

        # Data from Feed.pdf analysis
        categories = ['Promotional Content', 'Educational Content', 'Thought Leadership', 'Personal Updates', 'Uncategorized']
        num_posts = [18, 9, 6, 1, 2]  # Number of posts in each category

        # Bar Chart: Number of Posts by Category
        fig_feed_bar, ax_feed_bar = plt.subplots(figsize=(10, 6))
        ax_feed_bar.bar(categories, num_posts, color=['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854'], alpha=0.8, edgecolor='black')
        ax_feed_bar.set_title('Number of Posts by Category', fontsize=16)
        ax_feed_bar.set_xlabel('Category', fontsize=12)
        ax_feed_bar.set_ylabel('Number of Posts', fontsize=12)
        ax_feed_bar.tick_params(axis='x', rotation=30)
        plt.tight_layout()
        st.pyplot(fig_feed_bar)

        # Pie Chart: Distribution of Posts by Category
        fig_feed_pie, ax_feed_pie = plt.subplots(figsize=(8, 8))
        ax_feed_pie.pie(num_posts, labels=categories, autopct='%1.1f%%', startangle=140, colors=['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854'])
        ax_feed_pie.set_title('Distribution of Posts by Category', fontsize=16)
        plt.tight_layout()
        st.pyplot(fig_feed_pie)

        # Display example posts per category
        example_posts = {
            'Promotional Content': ['Example 1', 'Example 2', 'Example 3'],  # Replace with actual examples from your data
            'Educational Content': ['Example 1', 'Example 2'],
            'Thought Leadership': ['Example 1', 'Example 2'],
            'Personal Updates': ['Example 1'],
            'Uncategorized': ['Example 1', 'Example 2']
        }

        st.subheader("Example Posts by Category")
        for category, posts in example_posts.items():
            st.write(f"**Category:** {category}")
            st.write(f"**Number of Posts:** {len(posts)}")
            st.write("**Example Posts:**")
            for post in posts:
                st.write(f"- {post}")
            st.write("---")

    except Exception as e:
        st.error(f"Error processing Feed PDF data: {e}")

# --- 2. Connections.csv ---
if connections_file is not None:
    @st.cache_data
    def load_connections_data(file):
        # Skip the first three rows to read the header correctly
        data = pd.read_csv(file, skiprows=3)
        data.columns = data.columns.str.strip()
        return data

    try:
        connections_data = load_connections_data(connections_file)
        st.session_state['connections_data'] = connections_data

        st.header("Connections Data Analysis")

        st.subheader("Available Columns in Connections Data")
        st.write(connections_data.columns.tolist())

        required_columns = {'Position', 'Company', 'Connected On'}

        if not required_columns.issubset(connections_data.columns):
            st.warning("Required columns not found. Attempting to adjust column names...")
            # Adjust column names if necessary
            pass

        if not required_columns.issubset(connections_data.columns):
            missing_cols = required_columns - set(connections_data.columns)
            st.error(f"Error: Missing columns {missing_cols} in Connections data.")
        else:
            # Process connections data
            connections_data['Connected On'] = pd.to_datetime(connections_data['Connected On'], errors='coerce')
            connections_data['Year'] = connections_data['Connected On'].dt.year

            # Yearly Growth Visualization (Bar)
            yearly_trends = connections_data.groupby('Year').size()

            fig_conn1, ax_conn1 = plt.subplots(figsize=(12, 6))
            yearly_trends.plot(kind='bar', color='skyblue', alpha=0.8, edgecolor='black', ax=ax_conn1)
            ax_conn1.set_title('Yearly Growth in Connections', fontsize=16)
            ax_conn1.set_xlabel('Year', fontsize=12)
            ax_conn1.set_ylabel('Number of Connections', fontsize=12)
            st.pyplot(fig_conn1)

            # Word Cloud: Positions
            wordcloud_positions = WordCloud(width=800, height=400, background_color='white').generate(" ".join(connections_data['Position'].dropna()))
            fig_conn2, ax_conn2 = plt.subplots(figsize=(12, 6))
            ax_conn2.imshow(wordcloud_positions, interpolation='bilinear')
            ax_conn2.axis('off')
            ax_conn2.set_title('Word Cloud: Positions in Connections', fontsize=16)
            st.pyplot(fig_conn2)

            # Underrepresented Companies (Horizontal Bar)
            company_counts = connections_data['Company'].value_counts()
            underrepresented_companies = company_counts[company_counts == 1].head(10)
            fig_conn3, ax_conn3 = plt.subplots(figsize=(10, 6))
            underrepresented_companies.plot(kind='barh', color='orange', alpha=0.8, edgecolor='black', ax=ax_conn3)
            ax_conn3.set_title('Underrepresented Companies (Least Represented)', fontsize=16)
            ax_conn3.set_xlabel('Number of Connections', fontsize=12)
            ax_conn3.set_ylabel('Company', fontsize=12)
            st.pyplot(fig_conn3)

    except Exception as e:
        st.error(f"Error processing Connections data: {e}")

# --- 3. Messages.csv ---
if messages_file is not None:
    @st.cache_data
    def load_messages_data(file):
        data = pd.read_csv(file)
        data.columns = data.columns.str.strip()
        return data

    try:
        messages_data = load_messages_data(messages_file)
        st.session_state['messages_data'] = messages_data

        st.header("Messaging Data Analysis")

        st.subheader("Available Columns in Messages Data")
        st.write(messages_data.columns.tolist())

        required_columns = {'DATE', 'FROM', 'TO', 'SUBJECT', 'CONTENT'}

        # Adjust column names to uppercase to match your data
        messages_data.rename(columns=lambda x: x.strip().upper(), inplace=True)
        required_columns = {col.upper() for col in required_columns}

        if not required_columns.issubset(messages_data.columns):
            missing_cols = required_columns - set(messages_data.columns)
            st.error(f"Error: Missing columns {missing_cols} in Messages data.")
        else:
            messages_data['DATE'] = pd.to_datetime(messages_data['DATE'], errors='coerce')
            self_name = "C. Pete Connor MS, CCCM"  # Replace with your actual name as it appears in the 'FROM' or 'TO' columns

            # Messaging Frequency Trends
            messages_data['Direction'] = messages_data['TO'].apply(lambda x: 'Outbound' if x == self_name else 'Inbound')
            messages_data['Year-Month'] = messages_data['DATE'].dt.to_period('M')

            message_trends = messages_data.groupby(['Year-Month', 'Direction']).size().unstack(fill_value=0)

            fig_msg1, ax_msg1 = plt.subplots(figsize=(12, 6))
            message_trends.plot(kind='line', marker='o', ax=ax_msg1)
            ax_msg1.set_title('Messaging Trends (Inbound vs Outbound)', fontsize=16)
            ax_msg1.set_xlabel('Year-Month', fontsize=12)
            ax_msg1.set_ylabel('Number of Messages', fontsize=12)
            ax_msg1.legend()
            st.pyplot(fig_msg1)

            # Top Contacts by Interaction Frequency
            contact_counts = messages_data['FROM'].value_counts().head(10)
            fig_msg2, ax_msg2 = plt.subplots(figsize=(10, 6))
            contact_counts.plot(kind='bar', color='purple', alpha=0.7, ax=ax_msg2)
            ax_msg2.set_title('Top Contacts by Interaction Frequency', fontsize=16)
            ax_msg2.set_xlabel('Contact', fontsize=12)
            ax_msg2.set_ylabel('Number of Messages', fontsize=12)
            st.pyplot(fig_msg2)

            # Keyword Trends in Message Subjects
            stopwords_url = 'https://raw.githubusercontent.com/stopwords-iso/stopwords-en/master/stopwords-en.txt'
            stopwords = set(pd.read_csv(stopwords_url, header=None)[0])
            subjects = messages_data['SUBJECT'].dropna().str.lower()
            keywords = subjects.str.cat(sep=' ').split()
            keywords_series = pd.Series(keywords)
            keywords_series = keywords_series[~keywords_series.isin(stopwords)]
            top_keywords = keywords_series.value_counts().head(10)

            fig_msg3, ax_msg3 = plt.subplots(figsize=(10, 6))
            top_keywords.plot(kind='bar', color='green', alpha=0.7, ax=ax_msg3)
            ax_msg3.set_title('Top Keywords in Message Subjects', fontsize=16)
            ax_msg3.set_xlabel('Keyword', fontsize=12)
            ax_msg3.set_ylabel('Frequency', fontsize=12)
            st.pyplot(fig_msg3)

    except Exception as e:
        st.error(f"Error processing Messages data: {e}")

# --- 4. Date-Specific Content.xlsx ---
if content_file is not None:
    @st.cache_data
    def load_content_data(file):
        # Read specific sheets
        xls = pd.ExcelFile(file)
        sheets_data = {}
        for sheet_name in xls.sheet_names:
            if sheet_name.upper() in ['DISCOVERY', 'ENGAGEMENT', 'TOP POSTS', 'FOLLOWERS', 'DEMOGRAPHICS']:
                if sheet_name.upper() == 'TOP POSTS':
                    # Read with adjustments
                    data = pd.read_excel(xls, sheet_name=sheet_name, skiprows=3, usecols='A:C')
                    data.columns = ['Post URL', 'Post publish date', 'Engagements']
                elif sheet_name.upper() == 'DEMOGRAPHICS':
                    data = pd.read_excel(xls, sheet_name=sheet_name, skiprows=3)
                    data.columns = ['Demographic', 'Value', 'Percentage']
                else:
                    data = pd.read_excel(xls, sheet_name=sheet_name)
                    data.columns = data.columns.str.strip()
                sheets_data[sheet_name.upper()] = data
        return sheets_data

    try:
        content_data = load_content_data(content_file)
        st.session_state['content_data'] = content_data

        st.header("Content Performance Analysis")

        # --- TOP POSTS Sheet ---
        if 'TOP POSTS' in content_data:
            st.subheader("Top Posts")
            top_posts_data = content_data['TOP POSTS']

            st.write("Available columns in Top Posts data:")
            st.write(top_posts_data.columns.tolist())

            # Ensure required columns are present
            if {'Post URL', 'Post publish date', 'Engagements'}.issubset(top_posts_data.columns):
                # Convert 'Post publish date' to datetime
                top_posts_data['Post publish date'] = pd.to_datetime(top_posts_data['Post publish date'], errors='coerce')

                # Display top posts based on Engagements
                top_posts = top_posts_data.sort_values(by='Engagements', ascending=False).head(10)
                st.table(top_posts.reset_index(drop=True))
            else:
                st.warning("Top Posts data does not contain required columns ('Post URL', 'Post publish date', 'Engagements').")
        else:
            st.warning("Top Posts sheet not found in the Excel file.")

        # --- DEMOGRAPHICS Sheet ---
        if 'DEMOGRAPHICS' in content_data:
            st.subheader("Demographics Analysis")
            demographics_data = content_data['DEMOGRAPHICS']

            st.write("Available columns in Demographics data:")
            st.write(demographics_data.columns.tolist())

            # Since 'Demographic' column contains both the type and value, we need to split them
            demographics_data.dropna(inplace=True)
            demographics_data.reset_index(drop=True, inplace=True)

            # Identify the indices where the demographic type changes
            demographic_types = []
            current_type = ''
            for index, row in demographics_data.iterrows():
                if pd.isnull(row['Percentage']):
                    current_type = row['Demographic']
                    demographic_types.append(current_type)
                else:
                    demographic_types.append(current_type)

            demographics_data['Demographic Type'] = demographic_types

            # Remove rows that are just the demographic type headers
            demographics_data = demographics_data[pd.notnull(demographics_data['Percentage'])]

            # Convert 'Percentage' to numeric
            demographics_data['Percentage'] = demographics_data['Percentage'].astype(str)
            demographics_data['Percentage'] = demographics_data['Percentage'].str.replace('%', '').str.strip()
            demographics_data['Percentage'] = pd.to_numeric(demographics_data['Percentage'], errors='coerce')

            # Process each demographic type
            for demo_type in demographics_data['Demographic Type'].unique():
                demo_data = demographics_data[demographics_data['Demographic Type'] == demo_type]

                # Drop rows with NaN in 'Percentage'
                demo_data = demo_data.dropna(subset=['Percentage'])

                st.subheader(f"Top {demo_type}")

                # Plot the top demographics
                fig_demo, ax_demo = plt.subplots(figsize=(10, 6))
                demo_data.plot(kind='bar', x='Demographic', y='Percentage', color='teal', edgecolor='black', ax=ax_demo)
                ax_demo.set_title(f'Top {demo_type} by Percentage', fontsize=16)
                ax_demo.set_xlabel(demo_type, fontsize=12)
                ax_demo.set_ylabel('Percentage of Followers', fontsize=12)
                st.pyplot(fig_demo)

        else:
            st.warning("Demographics sheet not found in the Excel file.")

    except Exception as e:
        st.error(f"Error processing Content Performance data: {e}")

# --- 5. Invitations.csv ---
if invitation_file is not None:
    @st.cache_data
    def load_invitations_data(file):
        data = pd.read_csv(file)
        data.columns = data.columns.str.strip()
        return data

    try:
        invitations_data = load_invitations_data(invitation_file)
        st.session_state['invitations_data'] = invitations_data

        st.header("Invitations Analysis")

        st.subheader("Available Columns in Invitations Data")
        st.write(invitations_data.columns.tolist())

        # Columns are: 'From', 'To', 'Sent At', 'Message', 'Direction', 'inviterProfileUrl', 'inviteeProfileUrl'
        if 'Sent At' in invitations_data.columns:
            invitations_data['Sent At'] = pd.to_datetime(invitations_data['Sent At'], errors='coerce')
            invitations_data['Year-Month'] = invitations_data['Sent At'].dt.to_period('M')

            # Trends in Invitations Sent Over Time
            invitations_trends = invitations_data.groupby('Year-Month').size()
            fig_inv1, ax_inv1 = plt.subplots(figsize=(12, 6))
            invitations_trends.plot(kind='bar', color='blue', alpha=0.7, edgecolor='black', ax=ax_inv1)
            ax_inv1.set_title('Invitations Sent Over Time', fontsize=16)
            ax_inv1.set_xlabel('Year-Month', fontsize=12)
            ax_inv1.set_ylabel('Number of Invitations', fontsize=12)
            st.pyplot(fig_inv1)

            # Since 'Direction' is available, plot the distribution
            if 'Direction' in invitations_data.columns:
                direction_counts = invitations_data['Direction'].value_counts()
                fig_inv2, ax_inv2 = plt.subplots(figsize=(8, 6))
                direction_counts.plot(kind='pie', labels=direction_counts.index, autopct='%1.1f%%', startangle=140, ax=ax_inv2)
                ax_inv2.set_ylabel('')
                ax_inv2.set_title('Invitation Direction Distribution', fontsize=16)
                st.pyplot(fig_inv2)
            else:
                st.warning("Invitations data does not contain 'Direction' column.")
        else:
            st.warning("Invitations data does not contain 'Sent At' column.")

    except Exception as e:
        st.error(f"Error processing Invitations data: {e}")

# --- Chat Interface ---
st.header("Ask Questions About Your Data")
st.write("""
    You can ask questions like:
    - What are my top performing posts?
    - What are the trends in my follower demographics?
    - How can I improve my networking strategies?
""")

for i, msg in enumerate(st.session_state['messages']):
    if msg['is_user']:
        message(msg['content'], is_user=True, key=str(i) + '_user')
    else:
        message(msg['content'], key=str(i))

user_input = st.text_input("You:", key='input')

if user_input:
    st.session_state['messages'].append({'content': user_input, 'is_user': True})

    # Process the user's question
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

            # Ensure 'Percentage' is numeric, coercing errors to NaN
            demographics_data['Percentage'] = demographics_data['Percentage'].astype(str)
            demographics_data['Percentage'] = demographics_data['Percentage'].str.replace('%', '').str.strip()
            demographics_data['Percentage'] = pd.to_numeric(demographics_data['Percentage'], errors='coerce')

            result = ""
            for demo_type in demographics_data['Demographic Type'].unique():
                demo_data = demographics_data[demographics_data['Demographic Type'] == demo_type]

                # Drop rows with NaN in 'Percentage'
                demo_data = demo_data.dropna(subset=['Percentage'])

                # Ensure 'Percentage' is numeric
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