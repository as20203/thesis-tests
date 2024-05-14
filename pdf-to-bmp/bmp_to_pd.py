import pytesseract
from pdf2image import convert_from_path
import cv2
import pandas as pd
import numpy as np

pages = convert_from_path('loren-ipsum/loren_ipsum_text_thesis.pdf', 300)

master_page_par_line_list = []
master_ocr_image = ""

#function to resize image in order to append to other images using cv2
def vconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    w_min = min(im.shape[1] for im in im_list)
    im_list_resize = [cv2.resize(im, (w_min, int(im.shape[0] * w_min / im.shape[1])), interpolation=interpolation)
                      for im in im_list]
    return cv2.vconcat(im_list_resize)

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


#iterate through every page
for i, page in enumerate(pages):
    
    #Convert the image to grayscale and apply thresholding
    image = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2GRAY)
    _, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    
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
    for index, row in data_frame:
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


    for entry in page_par_line_dict:
        splitted_key = entry.split('_')
        entry_value = page_par_line_dict[entry]
        master_page_par_line_list.append({
            'page_number' : splitted_key[0],
            'paragraph_number' : splitted_key[1],
            'line_number' : splitted_key[2],
            'entry_text' : entry_value['text'],
            'bounding_box' : entry_value['box']
        })
    
    #draw bounding boxes for the lines detected in that image
    for line in page_par_line_dict.values():
        for key in line.keys():
            if key.startswith('space'):
                print('key',key,'value',line[key])
                cv2.rectangle(image, (line[key][0], line[key][1]), (line[key][2], line[key][3]), (0, 0, 255), 1)
        if line['box'] is not None:
            cv2.rectangle(image, (line['box'][0], line['box'][1]), (line['box'][2], line['box'][3]), (0, 0, 255), 2)
    
    if(master_ocr_image == ""):
        master_ocr_image = image
    
    #append the processed image with bounding box drawn to a vertically stacked master image for the whole pdf
    master_ocr_image = vconcat_resize_min([master_ocr_image, image])

#resize the master image and save it to your local working directory
resized_img = cv2.resize(master_ocr_image, (0, 0), fx=0.5, fy=0.5)
cv2.imwrite('master_ocr_image.jpg', resized_img)

#master ocr df with all pages, paragraph, lines, text and bounding box info
master_ocr_df = pd.DataFrame(master_page_par_line_list)
