import pdfplumber
from collections import defaultdict

# Load Feed.pdf
feed_pdf_path = "/Users/pconnor/Desktop/Custom GPT Files/LinkedIn Data Analyzer/Feed.pdf"

# Define categories and their keywords
categories = {
    "Promotional Content": ["buy", "offer", "ad", "sale", "discount"],
    "Educational Content": ["guide", "learn", "how-to", "tips", "steps"],
    "Thought Leadership": ["insight", "opinion", "perspective", "leadership"],
    "Personal Updates": ["achievement", "milestone", "journey", "promotion"],
    "Engagement-Oriented Posts": ["question", "poll", "discussion", "engage"]
}

# Function to categorize a post
def categorize_post(post_text):
    post_categories = []
    for category, keywords in categories.items():
        if any(keyword.lower() in post_text.lower() for keyword in keywords):
            post_categories.append(category)
    return post_categories if post_categories else ["Uncategorized"]

# Analyze Feed.pdf
feed_data = defaultdict(list)

try:
    with pdfplumber.open(feed_pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                posts = text.split("\n\n")  # Assume posts are separated by double newlines
                for post in posts:
                    post_categories = categorize_post(post)
                    for cat in post_categories:
                        feed_data[cat].append(post.strip())
except Exception as e:
    print(f"Error processing Feed.pdf: {e}")

# Summary of categories
for category, posts in feed_data.items():
    print(f"Category: {category}")
    print(f"Number of Posts: {len(posts)}")
    print(f"Example Posts: {posts[:3]}")
    print()