import PyPDF2

# Open the PDF file
with open('input.pdf', 'rb') as pdf_file:
    # Create a PdfFileReader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Get the trailer dictionary
    trailer = pdf_reader.trailer

    # Get the cross-reference table offset
    xref_offset = trailer['/Root']['/Size']

    # Find the object using its object number
    object_number = 11
    object_offset = None

    # Iterate through the cross-reference table to find the object's offset
    for i in range(xref_offset):
        # Get the byte offset of the object
        byte_offset = pdf_reader.xref[i]

        # Check if the object number matches
        if byte_offset[0] == object_number:
            # Get the byte offset of the object
            object_offset = byte_offset[1]
            break

    if object_offset is not None:
        # Seek to the object's offset in the PDF file
        pdf_file.seek(object_offset)

        # Read the object content
        object_content = pdf_file.read()

        # Print or process the object content as needed
        print("Object 11 content:", object_content)

# Close the PDF file
pdf_file.close()