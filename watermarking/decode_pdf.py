import pytesseract
from pdf2image import convert_from_path
import cv2
import pandas as pd
import numpy as np
import platform

def detect_word_space(previous_word, current_word):
    # previous_word = data_frame.iloc[index - 1]
    # current_word  = data_frame.iloc[index]
    # left is x coordinate and top is y coordinate
    if (previous_word is not None and previous_word['line_num'] == current_word['line_num']):
        space_top_left_x = previous_word['left'] + previous_word['width']
        space_top_left_y = previous_word['top']
        space_bottom_right_x = current_word['left']
        space_bottom_right_y =  current_word['top'] + current_word['height']
        return (space_top_left_x, space_top_left_y, space_bottom_right_x, space_bottom_right_y)
    return None


## returns longest line in a page
def get_max_width_line(page_par_line_dict = {}):
    longest_line_width = None
    line_information = None
    for entry in page_par_line_dict:
        line = page_par_line_dict[entry]['box']
        line_width = abs(line[2] - line[0])

        if longest_line_width is None or line_width > longest_line_width:
            longest_line_width = line_width
            line_information = entry
    return longest_line_width, line_information



def get_pdf_lines(filename, output_file_path, encoded_bit_sequence=''):
    is_modified_image = True if encoded_bit_sequence != '' else False
    master_ocr_image = ""
    pages = None
    pdf_lines = []

    if platform.system() == 'Windows':
        poppler_path = "C:\\Program Files\\poppler-23.11.0\\Library\\" + "bin"
        pages = convert_from_path(f"{filename}.pdf", dpi='450',grayscale=True, fmt='bmp', poppler_path=poppler_path)

    else:
        pages = convert_from_path(f"{filename}.pdf", dpi='450',grayscale=True, fmt='bmp')

    #iterate through every page
    for i, page in enumerate(pages):
        print(f"{output_file_path}/{filename}-original-{page}-{i}.jpg")
        original_image_name = f"{filename}-original-{i}.jpg"
        cv2.imwrite(original_image_name, np.array(page))
        #Convert the image to grayscale and apply thresholding
        ## To-Do: check if image is grayscale or not here.
        modified_image = cv2.imread(original_image_name, cv2.IMREAD_COLOR)

        _, image = cv2.threshold(np.array(page), 127, 255, cv2.THRESH_BINARY)
        
        #perform OCR on image using pytesseract. The --psm 6 flag tells pytesseract to do it line by line
        data = pytesseract.image_to_data(image,config='--oem 3 --psm 6', output_type='dict')
        #keep track of which page is being processed
        page_num = i + 1
        
        #this df contains the raw ocr results by pytesseract
        #later we will group it together to make sensible lines
        df = pd.DataFrame(data)
        df = df[df["conf"] > 0]
        df["page_num"] = page_num
        #for each page, paragraph and line combination, create line text and bounding box dimension
        page_par_line_dict = {}
        data_frame = df.iterrows()
        prev_word = None
        for _, row in data_frame:
            ## each row is a word.
            page_par_line = f"{page_num}_{row['par_num']}_{row['line_num']}"
            if(page_par_line not in page_par_line_dict):
                ## First character of the line.
                page_par_line_dict[page_par_line] = {
                    "text": str(row["text"]) + " ", 
                    "box": (row['left'], row['top'], row['left'] + row['width'], row['top'] + row['height'])
                    }
            else:
                ## To-do detect word spaces here:
                space = detect_word_space(prev_word, row)
                page_par_line_dict[page_par_line][f"space_{prev_word['text']}_{row['text']}"] = space
                page_par_line_dict[page_par_line]["text"] = page_par_line_dict[page_par_line]["text"] + str(row["text"]) + " "
                ## Detects the lines and for bounding box gets the maximum for right lower edge and minimum for top right edge
                page_par_line_dict[page_par_line]['box'] = (min(page_par_line_dict[page_par_line]['box'][0], row['left']), 
                                                    min(page_par_line_dict[page_par_line]['box'][1], row['top']), 
                                                    max(page_par_line_dict[page_par_line]['box'][2], row['left'] + row['width']), 
                                                    max(page_par_line_dict[page_par_line]['box'][3], row['top'] + row['height']))
            prev_word = row

        

        longest_line_width, _ = get_max_width_line(page_par_line_dict)
        scaling_factor = 1000
        #draw bounding boxes for the lines detected in that image
        with open(filename + '.txt', 'w') as file:
            for entry in page_par_line_dict:
                splitted_key = entry.split('_')
                line = page_par_line_dict[entry]
                space_counter = 0
                pdf_line =  {  'page_number' : splitted_key[0],
                              'paragraph_number' : splitted_key[1],
                              'line_number' : splitted_key[2],
                               'words': []
                            }
                encoded_sequence_counter = 0
                for key in line.keys():
                    if key.startswith('space'):
                        if is_modified_image:
                            is_one_space =  (0,255,0) ## Green
                            is_zero_space = (0,0,255)  ## Red
                            text = encoded_bit_sequence[encoded_sequence_counter] 
                            color = is_one_space if  text == '1' else is_zero_space
                            rectangle = cv2.rectangle(modified_image, (line[key][0], line[key][1]), (line[key][2], line[key][3]), color, 3)
                            cv2.putText(rectangle, text, (line[key][0], line[key][1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,139), 3)

                            encoded_sequence_counter +=1
                        width = abs(line[key][2] -  line[key][0])/longest_line_width * scaling_factor
                        file.write(str(f"key: {key}, value: {line[key]}, width: {width}" + '\n'))
                        pdf_line['words'].append({
                            'key': f"{key}_{space_counter}",
                            'width': width,
                            'coordinates': line[key]
                        })
                        space_counter += 1
                pdf_lines.append(pdf_line)
                encoded_sequence_counter = 0
        
        if is_modified_image:
            master_ocr_image = modified_image
            modified_image_name = f"{filename}-modified-{i}.bmp"
            cv2.imwrite(modified_image_name, master_ocr_image)
    return pdf_lines



def get_decoded_text(original_pdf = [], modified_pdf = [], encoded_sequence_length = 0):
    # decoded_pdf_lines = []
    decoded_string = ''
    print('original pdf', original_pdf)
    print('modified pdf', modified_pdf)
    for index, _ in enumerate(modified_pdf):
        ## add out of bounds error detection logic here.
        if index < len(modified_pdf) and index < len(original_pdf):
            modified_line = modified_pdf[index]
            original_line = original_pdf[index]
            # modified_line_number = f"{modified_line['page_number']}_{modified_line['paragraph_number']}_{modified_line['line_number']}"
            # original_line_number = f"{original_line['page_number']}_{original_line['paragraph_number']}_{original_line['line_number']}"

            ## check if the line numbers are the same.
            # if (original_line_number == modified_line_number):
            original_line_word_spaces = original_line['words']
            modified_word_spaces = modified_line['words']
            for index, _ in enumerate(modified_word_spaces):
                modifed_word_space = modified_word_spaces[index]
                ## To-do in case keys don't match increase index by 2 else by 1 for better comparison of words.
                original_word_space = original_line_word_spaces[index] if index < len(original_line_word_spaces) else None
                ## check if the key for the word in the line is same
                print('original key: ', original_word_space['key'],  'modified key: ', modifed_word_space['key'])
                if (original_word_space is not None):
                    modified_word_space_width = modifed_word_space['width']
                    original_word_space_width = original_word_space['width']
                    ## Check if its a 1 or 0.
                    if (modified_word_space_width > original_word_space_width):
                        decoded_string+= '1'
                    elif (modified_word_space_width < original_word_space_width):
                        decoded_string+= '0'
                    else:
                        decoded_string+= 'x'

            ## Decoded line in each string
            # decoded_pdf_lines.append({ 'line_number': modified_line_number, 'decoded_string': decoded_string})
    return decoded_string

# def check_decoded_string(original_bit_string, decoded_string):
#     # start_index = 0
#     # start = original_bit_string.find(decoded_string, start_index)
#     # decoded_bit_index = 0
#     decoded_bit_strings = []
#     original_bit_index = 0
#     correction = ''
#     incorrect_bits_count = 0
#     for i in range(len(decoded_string)):
#         if original_bit_string >= len(original_bit_string):
#             original_bit_index = 0
#             decoded_bit_strings.append(correction)
#             correction = ''
#         validation_original_bit_string = original_bit_string[original_bit_index]
#         if decoded_string[i] != validation_original_bit_string:
#             correction+='x'
#             incorrect_bits_count+=1
#         else:
#             correction += decoded_string[i]
#         original_bit_index += 1

    
    # if (is_binary_string(correction)):
    #     print('decode is correct.')
    # return correction, incorrect_bits_count


def check_decoded_string(original_bit_string, decoded_string):
    # start_index = 0
    # start = original_bit_string.find(decoded_string, start_index)
    # decoded_bit_index = 0
    print('Decoded string', decoded_string)
    decoded_bit_strings = []
    original_bit_index = 0
    docoded_string = ''
    incorrect_bits_count = 0
    for i in range(len(decoded_string)):
        if original_bit_index >= len(original_bit_string):
            original_bit_index = 0
            decoded_bit_strings.append(docoded_string)
            docoded_string = ''
        validation_original_bit_string = original_bit_string[original_bit_index]
        if decoded_string[i] != validation_original_bit_string:
            docoded_string+='x'
            incorrect_bits_count+=1
        else:
            docoded_string += decoded_string[i]
        original_bit_index += 1

    return decoded_bit_strings

        # if (is_binary_string(correction)):
    #     print('decode is correct.')
    # return correction, incorrect_bits_count

           
def is_binary_string(s):
    return set(s).issubset({'0', '1'})

# def get_decoded_text_substring(original_bit_string, decoded_pdf_lines):
#     total_error_rate = 0
#     for line in decoded_pdf_lines:
#         line_error_rate = 0
#         decoded_string = line['decoded_string']
#         correction_string, incorrect_bits_count = check_decoded_string(original_bit_string, decoded_string)
#         line_error_rate = incorrect_bits_count/len(decoded_string) if len(decoded_string) != 0 else 0
#         total_error_rate += line_error_rate
#         print('Line Number: ', line['line_number'])
#         print('Decoded string: ', decoded_string) 
#         print('correction', correction_string)

#     pdf_error_rate = total_error_rate/len(decoded_pdf_lines)
#     print('Total error rate: ', pdf_error_rate)
#     return pdf_error_rate
    

    

            


## To-do fix this original bit string.
# original_bitstring = '1011011010110010100000110110100001010010100010011000100011011000101001001001110100010100001000001001'
# filenames = ['loren-ipsum/loren_ipsum_text_thesis','loren-ipsum/loren_ipsum_text_thesis.result.50']
# original_pdf = get_pdf_lines(filenames[0])
# modified_pdf = get_pdf_lines(filenames[1])
# result = get_decoded_text(original_pdf, modified_pdf)

# result_strings = get_decoded_text_substring(original_bitstring,result)