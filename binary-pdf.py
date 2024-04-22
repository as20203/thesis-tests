def read_pdf_binary(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
    return binary_data

def binary_to_hex(binary_string):
    # Convert binary string to bytes
    binary_bytes = bytes(str(binary_string), 'utf-8')
    
    # Convert bytes to hexadecimal
    hexadecimal_string = binary_bytes.hex()
    
    return hexadecimal_string

if __name__ == "__main__":
    pdf_file_path = "input.pdf"
    binary_data = read_pdf_binary(pdf_file_path)
    print("Binary data of the PDF file:")
    print(binary_data)
    # hexadecimal_content = binary_to_hex(binary_data)
    # print("Hexadecimal content of the PDF document:")
    # print(hexadecimal_content)