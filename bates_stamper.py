import os
import pandas as pd
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import re
import string

def create_stamp_pdf(page_width, page_height, bates_number):
    """Creates a PDF with the Bates number stamp."""
    packet = io.BytesIO()
    # Create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=(page_width, page_height))
    # Position the stamp at the bottom right
    x_position = page_width - 100
    y_position = 20
    can.drawString(x_position, y_position, bates_number)
    can.save()

    packet.seek(0)
    return PdfReader(packet)

def apply_bates_stamping(manifest_path, output_dir):
    """
    Reads a manifest file and applies Bates stamping to the specified PDFs.
    """
    df = pd.read_excel(manifest_path)
    processed_files = []
    errors = []
    bates_counter = 1

    for index, row in df.iterrows():
        # Aggressively clean the file path to remove non-printable characters and normalize it.
        raw_path = row['File Path']
        
        # 1. Ensure it's a string and filter out non-printable characters.
        printable = set(string.printable)
        cleaned_path = ''.join(filter(lambda x: x in printable, str(raw_path)))
        # 2. Normalize path separators and remove leading/trailing whitespace.
        source_path = os.path.normpath(cleaned_path.strip())

        bates_prefix = row['Bates Prefix']

        if not os.path.exists(source_path):
            errors.append(f"File not found: {source_path}")
            continue

        try:
            reader = PdfReader(source_path)
            writer = PdfWriter()

            for i, page in enumerate(reader.pages):
                bates_number = f"{bates_prefix}{bates_counter:06d}"
                stamp_pdf = create_stamp_pdf(page.mediabox.width, page.mediabox.height, bates_number)
                page.merge_page(stamp_pdf.pages[0])
                writer.add_page(page)
                bates_counter += 1
            
            # Sanitize the filename to remove invalid characters
            base_name = os.path.basename(source_path)
            sanitized_name = re.sub(r'[<>:"/\\|?*]', '_', base_name)
            output_filename = os.path.join(output_dir, sanitized_name)
            with open(output_filename, "wb") as output_pdf:
                writer.write(output_pdf)
            processed_files.append(output_filename)
        except Exception as e:
            errors.append(f"Could not process {source_path}: {e}")

    return processed_files, errors