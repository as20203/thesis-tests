import PyPDF2

def modify_pdf_text(input_pdf_path, output_pdf_path, text_to_replace, replacement_text):
    with open(input_pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            print(page)
            content = page.get_contents()
            print(type(content))
            if isinstance(content, PyPDF2.generic._data_structures.EncodedStreamObject):
                decoded_data = content.get_data().decode()
                print((decoded_data))
                with open("decoded_content.txt", "w") as file:
                    file.write(decoded_data)
                for obj in content:
                   
                    if isinstance(obj, PyPDF2.generic.TextStringObject):
                       
                        if text_to_replace in obj:
                            new_obj = obj.replace(text_to_replace.encode(), replacement_text.encode())
                            page.mergeObject(obj, new_obj)

            writer.add_page(page)

        with open(output_pdf_path, 'wb') as output_file:
            writer.write(output_file)

# Example usage:
input_pdf = 'input.pdf'
output_pdf = 'output-text-modified.pdf'
text_to_replace = 'Old text'
replacement_text = 'New text'

modify_pdf_text(input_pdf, output_pdf, text_to_replace, replacement_text)
