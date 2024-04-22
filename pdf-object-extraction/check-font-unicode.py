import PyPDF2

def extract_to_unicode(pdf_file_path, to_unicode_reference):
    # Open the PDF file
    with open(pdf_file_path, 'rb') as pdf_file:
        # Create a PdfFileReader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Get the object number and generation number from the reference
        object_number, generation_number = to_unicode_reference

        # Get the object containing the ToUnicode mapping
        to_unicode_object = pdf_reader._get_indirect_object(object_number, generation_number)

        # Extract the encoding information from the ToUnicode object
        encoding_info = to_unicode_object.get_object().get_data()

        return encoding_info

# Path to your PDF file
pdf_file_path = 'input.pdf'

# Reference to the ToUnicode object (object number, generation number)
to_unicode_reference = (11, 0)

# Extract encoding information
encoding_info = extract_to_unicode(pdf_file_path, to_unicode_reference)

print("Encoding Information from ToUnicode Object:")
print(encoding_info)
