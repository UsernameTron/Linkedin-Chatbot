import os
import subprocess
import PyPDF2  # For PDF handling

# Configure the path to the MY DATA folder
BASE_PATH = "/Users/pconnor/Desktop/Custom GPT Files/LinkedIn Data Analyzer"
DATA_PATH = os.path.join(BASE_PATH, "MY Data")  # Correctly locate MY DATA folder

# Define available scripts and their purposes
SCRIPTS = {
    "analyze_connections": os.path.join(BASE_PATH, "analyze_connections.py"),
    "analyze_content": os.path.join(BASE_PATH, "analyze_content.py"),
    "generate_visualizations": os.path.join(BASE_PATH, "generate_visualizations.py"),
    "process_messages": os.path.join(BASE_PATH, "process_messages.py"),
    "demographics_analysis": os.path.join(BASE_PATH, "demographics_analysis.py"),
    "process_feed_pdf": os.path.join(BASE_PATH, "process_feed_pdf.py"),
}

# Supported file types
SUPPORTED_FILE_TYPES = {
    "csv": ["Connections.csv", "messages.csv"],
    "excel": ["Content.xlsx", "Engagement.xlsx", "Discovery.xlsx"],
    "pdf": ["feed.pdf"],
}

# Function to install dependencies
def install_dependencies():
    """Installs dependencies listed in requirements.txt."""
    requirements_file = os.path.join(BASE_PATH, "requirements.txt")
    if os.path.exists(requirements_file):
        try:
            subprocess.run(["pip", "install", "-r", requirements_file], check=True)
            print("Dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing dependencies: {e}")
    else:
        print("requirements.txt not found. Skipping dependency installation.")

# Function to execute a specific script
def run_script(script_name, *args):
    """
    Executes a script from the repository with optional arguments.

    Parameters:
    - script_name (str): Name of the script to run (must match a key in SCRIPTS).
    - *args: Arguments to pass to the script.

    Returns:
    - str: Output from the script or error message.
    """
    script_path = SCRIPTS.get(script_name)
    if not script_path or not os.path.exists(script_path):
        return f"Error: Script '{script_name}' not found."
    
    try:
        result = subprocess.run(
            ["python", script_path] + list(args),
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Script execution failed: {result.stderr}"
    except Exception as e:
        return f"Error running the script: {e}"

# Function to process PDF files
def process_pdf(file_path):
    """
    Extracts text from a PDF file for further processing.

    Parameters:
    - file_path (str): The path to the PDF file.

    Returns:
    - str: Extracted text or an error message.
    """
    try:
        with open(file_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = "".join(page.extract_text() for page in reader.pages)
            return text
    except Exception as e:
        return f"Error reading PDF file: {e}"

# Function to determine the appropriate script based on file type and name
def determine_script(file_name):
    """
    Determines which script to use based on the file name.

    Parameters:
    - file_name (str): The name of the file provided.

    Returns:
    - str: The name of the script to execute or None if unsupported.
    """
    ext = file_name.split('.')[-1].lower()
    if ext == "csv" and "Connections" in file_name:
        return "analyze_connections"
    elif ext == "csv" and "messages" in file_name:
        return "process_messages"
    elif ext in ["xlsx", "xlsm", "xls"]:
        return "analyze_content"
    elif ext == "pdf" and "feed" in file_name.lower():
        return "process_feed_pdf"
    return None

# Main function to handle file input and execute the correct script
def handle_file(file_path):
    """
    Handles processing of a given file by determining the appropriate script.

    Parameters:
    - file_path (str): The full path to the file.

    Returns:
    - str: The output from the executed script or an error message.
    """
    file_name = os.path.basename(file_path)
    script_name = determine_script(file_name)

    if not script_name:
        return f"Unsupported file type or name: {file_name}"

    if script_name == "process_feed_pdf":
        # Special handling for PDFs
        extracted_text = process_pdf(file_path)
        if "Error" in extracted_text:
            return extracted_text
        # Pass extracted text to the relevant script
        return run_script(script_name, extracted_text)
    else:
        # For other file types, pass the file path to the script
        return run_script(script_name, file_path)

# Updated prompt for file path input
if __name__ == "__main__":
    install_dependencies()
    print(f"Place all your files in the 'MY DATA' folder at: {DATA_PATH}")
    # Prompt for file path
    file_path = input("Enter the name of the file you want to analyze (e.g., Connections.csv): ").strip()
    
    # Resolve file path within MY DATA folder
    resolved_path = os.path.join(DATA_PATH, file_path)

    # Check if file exists
    if os.path.exists(resolved_path):
        print(f"Processing file: {resolved_path}")
        print(handle_file(resolved_path))  # Run the appropriate analysis
    else:
        print(f"Error: File '{resolved_path}' does not exist.")