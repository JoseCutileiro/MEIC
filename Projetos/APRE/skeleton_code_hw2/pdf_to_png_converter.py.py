import os
import fitz  # PyMuPDF library

def convert_pdf_to_png(pdf_path, output_folder):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Iterate through each page
    for page_number in range(pdf_document.page_count):
        # Get the page
        page = pdf_document[page_number]

        # Convert the page to a pixmap
        image = page.get_pixmap()

        # Save the pixmap as a PNG file
        image.save(os.path.join(output_folder, f"{os.path.basename(pdf_path)[:-4]}.png"))

    # Close the PDF file
    pdf_document.close()

def convert_all_pdfs(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            convert_pdf_to_png(pdf_path, output_folder)

if __name__ == "__main__":
    # Replace 'input_folder' with the path to the folder containing your PDFs
    input_folder = "C:\\Users\\guipa\\OneDrive\\Documentos\\GitHub\\DL_homeworks\\skeleton_code_hw2"

    # Replace 'output_folder' with the path to the folder where you want to save the PNGs
    output_folder = "C:\\Users\\guipa\\OneDrive\\Documentos\\GitHub\\DL_homeworks\\skeleton_code_hw2\\img"

    convert_all_pdfs(input_folder, output_folder)
