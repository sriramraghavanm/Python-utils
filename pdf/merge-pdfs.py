import os
import datetime
from PyPDF2 import PdfReader, PdfWriter
import sys

def is_pdf_encrypted(pdf_path):
    try:
        with open(pdf_path, "rb") as f:
            reader = PdfReader(f)
            return reader.is_encrypted
    except Exception as e:
        print(f"[ERROR] Failed to check encryption for '{pdf_path}': {e}")
        return True  # Treat as encrypted if unreadable

def merge_pdfs(pdf_files, output_path):
    writer = PdfWriter()

    for pdf in pdf_files:
        if not os.path.exists(pdf):
            print(f"[ERROR] File not found: {pdf}")
            return
        if not pdf.lower().endswith(".pdf"):
            print(f"[ERROR] Not a valid PDF file: {pdf}")
            return
        if is_pdf_encrypted(pdf):
            print(f"[ERROR] PDF file is encrypted or password protected: {pdf}")
            return
        try:
            with open(pdf, "rb") as f:
                reader = PdfReader(f)
                for page in reader.pages:
                    writer.add_page(page)
        except Exception as e:
            print(f"[ERROR] Failed to process '{pdf}': {e}")
            return

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:
        with open(output_path, "wb") as f_out:
            writer.write(f_out)
        print(f"[SUCCESS] Merged PDF saved to: {output_path}")
    except Exception as e:
        print(f"[ERROR] Failed to write output file: {e}")

if __name__ == "__main__":
    # Specify the order of PDF files
    pdf_files = [
        r"C:\Users\someuser\Downloads\Simplii_January.pdf",
        r"C:\Users\someuser\Downloads\Simplii_February.pdf",
        r"C:\Users\someuser\Downloads\Simplii_March.pdf",
        r"C:\Users\someuser\Downloads\Simplii_April.pdf"
    ]

    today = datetime.date.today().strftime("%Y-%m-%d")
    output_dir = os.path.join(r"C:\temp\pdf", today)
    output_file_name = "Simplii.pdf"
    output_path = os.path.join(output_dir, output_file_name)

    merge_pdfs(pdf_files, output_path)
