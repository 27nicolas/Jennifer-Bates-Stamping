# Jennifer-Bates-Stamping

## Overview

A simple web application to apply Bates stamping to PDF documents. Bates stamping is the process of assigning unique, sequential identifiers to each page of a document to ensure accurate organization and tracking.

This application provides a web interface to upload an Excel manifest file. The manifest lists the documents to be stamped. The application then processes each document, adding a unique Bates number to the bottom-right corner of every page.

It also includes a helper script to automatically scan your computer for PDF files and generate a manifest for you.

## Features
- Web-based interface for easy use.
- Processes documents based on an Excel manifest.
- Applies sequential Bates numbers across all pages of all documents.
- Saves stamped documents to a separate output directory (`stamped_documents`).
- Includes a utility to automatically create a manifest file.

## Installation

1.  **Prerequisites:**
    - Python 3.6+

2.  **Clone the repository (if applicable) or ensure all project files are in the same directory.**

3.  **Install required Python libraries:**
    Open your terminal or command prompt and run the following command to install the necessary dependencies:
    ```bash
    pip install Flask pandas pypdf reportlab
    ```

## How to Use

### Step 1: Prepare the Manifest File

You have two options for creating the manifest file:

**Option A: Automatically Generate a Manifest**

A helper script is included to find PDF files on your computer and create a manifest.

1.  Run the script from your terminal:
    ```bash
    python create_manifest.py
    ```
2.  This will create a file named `new_bates_manifest.xlsx` in the project directory. This file will contain paths to PDF files found on your machine. You can review and edit this file as needed.

**Option B: Manually Create a Manifest**

1.  Create an Excel file (e.g., `Bates_Stamping_Index_Template.xlsx`).
2.  This file must contain two columns:
    - `File Path`: The full, absolute path to the PDF document you want to stamp.
    - `Bates Prefix`: The text prefix for the Bates number (e.g., "DOC", "CASE001").

### Step 2: Run the Web Application

1.  Navigate to the project directory in your terminal.
2.  Start the web server by running:
    ```bash
    python app.py
    ```
3.  You will see output indicating that the server is running on `http://127.0.0.1:5000`.

### Step 3: Process Your Documents

1.  Open your web browser and go to `http://127.0.0.1:5000`.
2.  Click the "Choose File" or "Browse" button and select your Excel manifest file (e.g., `new_bates_manifest.xlsx`).
3.  Click "Upload and Process".
4.  The application will begin stamping the documents. You will see status messages on the web page upon completion.

### Step 4: Find Your Stamped Files

Once the process is complete, the newly stamped PDF files will be available in the `stamped_documents` folder within your project directory.
