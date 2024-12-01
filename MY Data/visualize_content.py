import matplotlib.pyplot as plt

# Example visualization
try:
    content_data.columns = ["Metric", "Value"]  # Ensure column names are consistent
    content_data.plot(kind='bar', x='Metric', y='Value', legend=False)
    plt.title("Content Performance")
    plt.ylabel("Value")
    plt.show()
except Exception as e:
    print(f"Error during visualization: {e}")