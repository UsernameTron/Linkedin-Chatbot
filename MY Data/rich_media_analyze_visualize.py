import pandas as pd
import matplotlib.pyplot as plt

# File path for the dataset
file_path = "/Users/pconnor/Desktop/Custom GPT Files/LinkedIn Data Analyzer/Rich_Media.csv"

try:
    # Load the dataset with the correct delimiter
    rich_media_data = pd.read_csv(file_path)

    # Inspect column names
    print(f"Dataset Columns: {rich_media_data.columns}")

    # Ensure column names are standardized
    if 'Media Link' in rich_media_data.columns:
        # Categorize media based on URL patterns
        def categorize_media(link):
            if isinstance(link, str):
                if 'playlist/vid' in link or 'dms.video' in link:
                    return 'Video'
                elif 'feedshare-document-url-metadata-scrapper-pdf' in link:
                    return 'Feed Document'
                elif 'profile-treasury-document' in link:
                    return 'Uploaded Document'
                elif 'image' in link or 'photo' in link:
                    return 'Image'
                else:
                    return 'Other'
            return 'Unknown'

        # Apply the categorization logic
        rich_media_data['Media Type'] = rich_media_data['Media Link'].apply(categorize_media)

        # Group data by media type
        media_counts = rich_media_data['Media Type'].value_counts()

        # Visualization: Media Type Distribution
        plt.figure(figsize=(10, 6))
        media_counts.plot(kind='bar', color='skyblue', edgecolor='black', alpha=0.8)
        plt.title('Media Type Distribution', fontsize=16)
        plt.xlabel('Media Type', fontsize=12)
        plt.ylabel('Count', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

        # Save the processed data for further analysis
        processed_file_path = "/Users/pconnor/Desktop/Custom GPT Files/LinkedIn Data Analyzer/Processed_Rich_Media.csv"
        rich_media_data.to_csv(processed_file_path, index=False)
        print(f"Processed data saved to {processed_file_path}")
    else:
        print("Error: 'Media Link' column not found in the dataset.")

except Exception as e:
    print(f"An error occurred: {e}")