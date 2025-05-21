import PyPDF2
import os

def rotate_pdf(input_pdf, output_pdf):
    # Validate input file
    if not os.path.isfile(input_pdf):
        print(f"Error: The file '{input_pdf}' does not exist.")
        return

    try:
        # Open the input PDF file
        with open(input_pdf, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()

            # Rotate each page by 90 degrees anti-clockwise
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                page.rotate(90)
                writer.add_page(page)

            # Create output directory if it does not exist
            output_dir = os.path.dirname(output_pdf)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                print(f"Info: The directory '{output_dir}' has been created.")

            # Write the rotated pages to the output PDF file
            with open(output_pdf, 'wb') as output_file:
                writer.write(output_file)

        print(f"Success: The file '{output_pdf}' has been created with rotated pages.")

    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")

# Example usage
input_pdf = 'C:/Users/someuser/Downloads/DevOps+Project.pdf'
output_pdf = 'C:/Temp/pdf/DevOps+Project.pdf'
rotate_pdf(input_pdf, output_pdf)
