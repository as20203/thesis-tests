import PyPDF2

def reduce_word_spacing(input_pdf, output_pdf, spacing_reduction):
    # Open the PDF file
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        # Iterate through each page
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]

            # Get the text content of the page
            text_content = page.extract_text()

            # Reduce the spacing between words
            all_text = text_content.encode('latin-1', 'ignore').decode('utf-8')
            cleaned_text = '  '.join(all_text.split())
            print(cleaned_text)

        # Write the modified PDF to the output file
        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

if __name__ == "__main__":
    input_pdf = "input.pdf"
    output_pdf = "output.pdf"
    spacing_reduction = 2  # Adjust spacing reduction by 2 units (you can change this as needed)

    reduce_word_spacing(input_pdf, output_pdf, spacing_reduction)