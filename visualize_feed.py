import matplotlib.pyplot as plt

# Data from Feed.pdf analysis
categories = ['Promotional Content', 'Educational Content', 'Thought Leadership', 'Personal Updates', 'Uncategorized']
num_posts = [18, 9, 6, 1, 2]  # Number of posts in each category

# Bar Chart: Number of Posts by Category
plt.figure(figsize=(10, 6))
plt.bar(categories, num_posts, color=['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854'], alpha=0.8, edgecolor='black')
plt.title('Number of Posts by Category', fontsize=16)
plt.xlabel('Category', fontsize=12)
plt.ylabel('Number of Posts', fontsize=12)
plt.xticks(rotation=30, ha='right', fontsize=10)
plt.tight_layout()
plt.show()

# Pie Chart: Distribution of Posts by Category
plt.figure(figsize=(8, 8))
plt.pie(num_posts, labels=categories, autopct='%1.1f%%', startangle=140, colors=['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854'])
plt.title('Distribution of Posts by Category', fontsize=16)
plt.tight_layout()
plt.show()

# Display example posts per category
example_posts = {
    'Promotional Content': ['Example 1', 'Example 2', 'Example 3'],  # Replace with actual examples from your data
    'Educational Content': ['Example 1', 'Example 2'],
    'Thought Leadership': ['Example 1', 'Example 2'],
    'Personal Updates': ['Example 1'],
    'Uncategorized': ['Example 1', 'Example 2']
}

print("\n--- Example Posts by Category ---")
for category, posts in example_posts.items():
    print(f"\nCategory: {category}")
    print(f"Number of Posts: {len(posts)}")
    print(f"Example Posts: {posts}")