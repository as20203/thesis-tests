
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import DecodedStreamObject, EncodedStreamObject, NameObject
import os
import detect_pdf_lines, word_spacing, modifed_pdf_lines

def replace_text(content, transformed_input_output, encoded_bit_sequence, threshold):
    lines = content.splitlines()
    page_pdf_content = []
    result = ""
    in_text = False
    for line in lines:
        if line == "BT":
            page_pdf_content.append(line)
            in_text = True

        elif line == "ET":
            page_pdf_content.append(line)
            in_text = False

        elif in_text:
            cmd = line[-2:]
            if cmd.lower() == 'tj':
                transformed_input = word_spacing.transform_input(line)
                transformed_input.append("TJ")
                # print("Line: - ", line + "\n")
                # print('Transformed line:- ', transformed_input)
                # print('Lines in transformed input:- ', detect_pdf_lines.detectPdfLines(transformed_input))
                transformed_input_output.extend(transformed_input)
                page_pdf_content.extend(transformed_input)
            else:
                page_pdf_content.append(line)
        else:
            page_pdf_content.append(line)
        page_pdf_content.append("\\n")
        result += line + "\n"
    # word_spacing.write_array_to_file(page_pdf_content,'page_pdf_content.txt')
    output = detect_pdf_lines.detectPdfLines(page_pdf_content)
    updated_output = modifed_pdf_lines.modified_pdf_lines(output, encoded_bit_sequence, threshold)
    # word_spacing.write_array_to_file(updated_output, 'modified_pdf_content.txt')
    # word_spacing.write_array_to_file(output,'page_pdf_lines.txt')
    # with open('result.txt', 'w') as file:
    #         file.write(result)
    updated_result = '\n'.join(updated_output)
    return updated_result


def process_data(object, replacements, threshold = 50, encoded_bit_sequence = ''):
    data = object.get_data()
    decoded_data = data.decode()

    replaced_data = replace_text(decoded_data, replacements, encoded_bit_sequence, threshold)
    encoded_data = replaced_data.encode()
    if object.decoded_self is not None:
        object.decoded_self.set_data(encoded_data)
    else:
        object.set_data(encoded_data)



def encode_pdf(output_filename, input_filePath, output_filePath, encoded_bit_sequence, threshold = 50):
    transformed_input_output =  []
    reader = PdfReader(input_filePath)
    writer = PdfWriter()
    for page_number in range(0, len(reader.pages)):

        page = reader.pages[page_number]
        contents = page.get_contents()

        if isinstance(contents, DecodedStreamObject) or isinstance(contents, EncodedStreamObject):
            process_data(contents, transformed_input_output, threshold, encoded_bit_sequence, )
        elif len(contents) > 0:
            for obj in contents:
                if isinstance(obj, DecodedStreamObject) or isinstance(obj, EncodedStreamObject):
                    streamObj = obj.get_object()
                    process_data(streamObj, transformed_input_output, threshold, encoded_bit_sequence)

        
        page[NameObject("/Contents")] = contents.decoded_self
        writer.add_page(page)
    
    word_spacing.write_array_to_file(transformed_input_output,f'{output_filePath}/transformed-output.txt')
    output = detect_pdf_lines.detectPdfLines(transformed_input_output)
    word_spacing.write_array_to_file(output,f'{output_filePath}/output.txt')

    output_filename = f"{output_filePath}/{output_filename}.{threshold}.result.pdf"
    with open(output_filename, 'wb') as out_file:
        writer.write(out_file)
    return output_filename.replace(os.path.splitext(output_filename)[1], "")