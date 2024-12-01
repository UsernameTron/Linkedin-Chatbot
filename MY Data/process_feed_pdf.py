import PyPDF2
import re
import pandas as pd
import matplotlib.pyplot as plt

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    try:
        with open(pdf_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return ""

def categorize_posts(text):
    """Categorizes posts based on keywords in the text."""
    categories = {"Educational": 0, "Promotional": 0, "Engagement": 0}
    for line in text.splitlines():
        if "educational" in line.lower():
            categories["Educational"] += 1
        elif "promo" in line.lower() or "sale" in line.lower():
            categories["Promotional"] += 1
        elif "engage" in line.lower() or "like" in line.lower():
            categories["Engagement"] += 1
    return categories

def create_visualizations(categories):
    """Creates visualizations for categorized posts."""
    try:
        # Bar Chart for Category Distribution
        plt.bar(categories.keys(), categories.values())
        plt.title("Post Categories Distribution")
        plt.xlabel("Category")
        plt.ylabel("Count")
        plt.show()
    except Exception as e:
        print(f"Error generating visualization: {e}")

def main():
    pdf_path = "feed.pdf"  # Update with the actual file path
    text = extract_text_from_pdf(pdf_path)
    if not text:
        print("No text extracted from the PDF. Exiting.")
        return

    categories = categorize_posts(text)
    print("Post Categories:")
    for category, count in categories.items():
        print(f"{category}: {count}")

    create_visualizations(categories)

if __name__ == "__main__":
    main()