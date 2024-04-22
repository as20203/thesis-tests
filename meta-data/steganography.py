import PyPDF2

def embed_message(input_pdf, output_pdf, message):
    # Open the input PDF file
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        # Embed the message in the metadata of the first page
        first_page = reader.pages[0]
        print(first_page)
    


        # Add all pages from the input PDF to the output PDF
        for page in reader.pages:
            writer.add_page(page)
        
        writer.add_metadata(
        {
        "/Title": message,
        })

        # Write the modified PDF to the output file
        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

def extract_message(pdf_file):
    # Open the PDF file
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        # Extract the message from the metadata of the first page
        meta = reader.metadata
        return meta.title

if __name__ == "__main__":
    input_pdf = "input.pdf"
    output_pdf = "output-steganography.pdf"
    message = "Copyright/student-10099738."

    # Embed the message in the input PDF
    embed_message(input_pdf, output_pdf, message)

    # Extract the message from the output PDF
    extracted_message = extract_message(output_pdf)
    print("Extracted message:", extracted_message)