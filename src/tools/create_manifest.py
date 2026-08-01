import os
import pandas as pd

def create_manifest_from_found_pdfs(start_dir, output_filename, limit=5):
    """
    Walks through a directory to find PDF files and creates an Excel manifest.

    Args:
        start_dir (str): The root directory to start searching from.
        output_filename (str): The name of the Excel file to create.
        limit (int): The number of PDF files to find before stopping.
    """
    pdf_files = []
    print(f"Starting search for {limit} PDF files in '{start_dir}'...")
    excluded_dir = os.path.join(os.path.expanduser("~"), "CrossDevice")

    for root, dirs, files in os.walk(start_dir):
        # Skip directories that are excluded or the user may not have permission to read
        if root.startswith(excluded_dir) or "AppData" in root or "Windows" in root:
            continue

        for file in files:
            if file.lower().endswith('.pdf'):
                full_path = os.path.join(root, file)
                # Check if the file size is greater than 50KB
                if os.path.getsize(full_path) > 50 * 1024:
                    pdf_files.append(full_path)
                    print(f"Found: {full_path}")
                    if len(pdf_files) >= limit:
                        break
        if len(pdf_files) >= limit:
            break
    
    if not pdf_files:
        print("No PDF files were found.")
        return

    # Create a DataFrame that matches the expected manifest format
    manifest_data = {
        'File Path': pdf_files,
        'Bates Prefix': ['DOC'] * len(pdf_files)  # Default prefix
    }
    df = pd.DataFrame(manifest_data)

    # Save the DataFrame to an Excel file
    df.to_excel(output_filename, index=False)
    print(f"\nSuccessfully created manifest: '{output_filename}' with {len(pdf_files)} entries.")

if __name__ == '__main__':
    # Start search from the user's home directory for better performance and permissions
    search_directory = os.path.expanduser("~") 
    create_manifest_from_found_pdfs(search_directory, 'new_bates_manifest.xlsx')