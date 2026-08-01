import os
import pandas as pd

def create_manifest_from_found_pdfs(start_dir, output_filename, logger=print):
    """
    Walks through a directory to find PDF files and creates an Excel manifest.

    Args:
        start_dir (str): The root directory to start searching from.
        output_filename (str): The name of the Excel file to create.
        logger (function): A function to use for logging progress (e.g., print or a GUI logger).
    """
    pdf_files = []
    logger(f"Starting search for all PDF files in '{start_dir}'...")
    excluded_dir = os.path.join(os.path.expanduser("~"), "CrossDevice")

    for root, dirs, files in os.walk(start_dir):
        # Skip directories that are excluded or the user may not have permission to read
        if root.startswith(excluded_dir) or "AppData" in root or "Windows" in root:
            continue

        for file in files:
            if file.lower().endswith('.pdf'):
                try:
                    full_path = os.path.join(root, file)
                    # Check if the file size is greater than 50KB
                    if os.path.getsize(full_path) > 50 * 1024:
                        pdf_files.append(full_path)
                        logger(f"Found: {full_path}")
                except OSError:
                    # Ignore files we can't access
                    continue
    
    if not pdf_files:
        logger("No PDF files were found.")
        return False

    # Create a DataFrame that matches the expected manifest format
    manifest_data = {
        'File Path': pdf_files,
        'Bates Prefix': ['DOC'] * len(pdf_files)  # Default prefix
    }
    df = pd.DataFrame(manifest_data)

    # Save the DataFrame to an Excel file
    df.to_excel(output_filename, index=False)
    logger(f"\nSuccessfully created manifest: '{output_filename}' with {len(pdf_files)} entries.")
    return True

if __name__ == '__main__':
    # Start search from the user's home directory for better performance and permissions
    search_directory = os.path.expanduser("~") 
    create_manifest_from_found_pdfs(search_directory, 'new_bates_manifest.xlsx')