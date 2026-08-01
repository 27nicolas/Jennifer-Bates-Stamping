# Jennifer-Bates-Stamping

## Overview

A simple desktop application to apply Bates stamping to PDF documents. Bates stamping is the process of assigning unique, sequential identifiers to each page of a document to ensure accurate organization and tracking.

This application provides a graphical user interface (GUI) to:
1.  Automatically scan your computer for PDF files to generate an Excel manifest.
2.  Upload an Excel manifest file that lists the documents to be stamped.

The application then processes each document, adding a unique Bates number to the bottom-right corner of every page.

## Features
- Simple graphical user interface for ease of use.
- Utility to automatically create a manifest file by scanning for PDFs.
- Processes documents based on an Excel manifest.
- Applies sequential Bates numbers across all pages of all documents.
- Saves stamped documents to a separate output directory (`stamped_documents`).

## Installation

1.  **Prerequisites:**
    - Python 3.6+

2.  **Clone the repository (if applicable) or ensure all project files are in the same directory.**

3.  **Install required Python libraries:**
    Open your terminal or command prompt and run the following command to install the necessary dependencies:
    ```bash
    pip install pandas pypdf reportlab
    ```

## How to Use

### Step 1: Prepare the Manifest File

You can create the manifest file in two ways: automatically using the application, or manually.

**Option A: Automatically Generate a Manifest (Recommended)**

1.  Run the application (see Step 2).
2.  Click the "Find PDFs and Create Manifest" button.
3.  A dialog will appear asking you to select a folder. The application will then scan the selected folder and its subfolders for PDF files to create `new_bates_manifest.xlsx` in the project directory. The file will be automatically selected for processing.

**Option B: Manually Create a Manifest**

1.  Create an Excel file (e.g., `manifest.xlsx`).
2.  The file must contain two columns:
    - `File Path`: The full, absolute path to the PDF document you want to stamp.
    - `Bates Prefix`: The text prefix for the Bates number (e.g., "DOC", "CASE001").

### Step 2: Run the Application

**On Windows:**
Simply double-click the `start.bat` file located in the project directory. This will launch the application window.

**On macOS / Linux (or as an alternative):**
1.  Open your terminal or command prompt and navigate to the project directory.
2.  Run the following command:
    ```bash
    python gui_app.py
    ```

### Step 3: Process Your Documents

1.  If you didn't use the automatic creation tool, click "Select Manifest File (.xlsx)" and choose your manifest.
2.  Click "Upload and Process".
3.  The application will begin stamping the documents. You can monitor the progress in the "Processing Log" window. You will see a final status message upon completion.

### Step 4: Find Your Stamped Files

Once the process is complete, the newly stamped PDF files will be available in the `stamped_documents` folder within your project directory.
