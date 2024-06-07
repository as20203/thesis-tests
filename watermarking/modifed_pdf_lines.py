def count_negative_space_indices(array, threshold=-50):
    count = 0

    for item in array:
        if item.startswith('s:'):
            try:
                value = int(item[2:])
                if value < threshold:
                    count += 1
            except ValueError:
                # Handle the case where the value part is not a valid integer
                continue

    return count

def count_bits(bit_sequence):
    count_ones = bit_sequence.count('1')
    count_zeros = bit_sequence.count('0')
    
    return count_ones, count_zeros



def modify_word(word, update_str = ''):
    updated_word = ''
    for char in word:
        if char == ')':
            updated_word+= update_str + char
        else:
            updated_word+= char
    return updated_word

def modify_last_word(content):
    updated_content = content.copy()
    index = len(updated_content) - 1
    foundLastWord = False
    while not(foundLastWord) and index >= 0:
        item = updated_content[index]
        if item.startswith("w:") and item.endswith(")"):
            updated_content[index] = modify_word(item,'nl')
            foundLastWord = True
            index = -1
        else:
            index -= 1
    return updated_content




def modify_line_spaces(line_text, space_value = 0, encoded_bit_sequence = ''):
    updated_content = line_text.copy()
    bit_list_index = 0
    index = 0
    space_count = count_negative_space_indices(updated_content)
    # print('Space count: ', space_count)

    ones_count, zeros_count = count_bits(encoded_bit_sequence[:space_count])
    # print(ones_count, zeros_count)
    bit_list = list(encoded_bit_sequence)
    line_length_change = (ones_count-zeros_count) * space_value
    one_space_value = space_value
    zeros_space_value = space_value

    if line_length_change > 0:
        one_space_value -= line_length_change/ones_count
    if line_length_change < 0:
        zeros_space_value -= line_length_change/zeros_count
    
    # is_ones_greater = False
    # if ones_count >= zeros_count:
    #     is_ones_greater = True

    ## Decide which ones will increase the space 
    ## and which will decrease so difference is close to zero.
    ## if ones are greater than zero

    ## To-do
    ## pass the bit string here
    ## detect total spaces in each line say 5.
    ## 2 ones 3 zeros
    ## difference of changes should be close to zero in each line.
    ### 1000111
    ## append it to each line.
    # space_identifier = 'I'
    # space_separator = [']','TJ','\n','1 0 0 rg 1 0 0 RG', '\n', '[({})]TJ'.format(space_identifier), '\n', '0 g 0 G', '\n', '[']
    while index < len(updated_content):
    # for index,item in enumerate(updated_content):
        item = updated_content[index]
        # spaces_difference = 0
        if item.startswith("s:"):
            space = int(item[2:])
            ## Space between words is usually negative.
            ## used -50
            ## Space between characters is usually positive
            ## if negative it represents kerning and the value is usually quite low.
            ## fix this so that this is fixed.
            if space < 0 and space < -50:
                bit = bit_list[bit_list_index]

                # space_count+=1
                # if space_count % 2 == 0:
                #     space += space_value
                # else:
                #     space -= space_value
                if bit  == "1":
                    space -= one_space_value
                    # if is_ones_greater:
                    #     space += space_value
                    #     spaces_difference += space_value
                    # elif not(is_ones_greater) and (count_difference) != 0:
                    #     space += (space_value * 2)
                    #     spaces_difference  += (space_value * 2)
                    #     count_difference -= 1
                else:
                    space += zeros_space_value
                    # if not(is_ones_greater):
                    #     space -= space_value
                    #     spaces_difference -= space_value
                    # elif (is_ones_greater) and (count_difference) != 0:
                    #     space -= (space_value * 2)
                    #     spaces_difference -= (space_value * 2)
                    #     count_difference -= 1
                bit_list_index += 1
                # space_count+=1
                updated_content[index] = 's:{}'.format(space)
                # updated_content[index:index] = space_separator
                # index += len(space_separator)
        index += 1

    return updated_content


           

def modified_pdf_lines(pdf_lines, encoded_bit_sequence = '', threshold = 50):
    updated_pdf_lines = []
    pdf_line = ''
    for item in pdf_lines:
        content_adjustment = item['line-adjustment']
        line_text = item['content']
        ## Fix content adjustment
        if isinstance(content_adjustment, list):
            for index, item in enumerate(content_adjustment):
                if item != '\\n' and index != len(content_adjustment) - 1:
                    updated_pdf_lines.append(item)
                if index == len(content_adjustment) - 1:
                    pdf_line+=item
        else:
            pdf_line += content_adjustment
            # updated_pdf_lines.append(content_adjustment)

        if line_text and isinstance(line_text,list):
            ## Do our changes here
            ## modify spaces or change words etc.
            ## ToDo write code that will now modify the words and spaces.
            # modified_content = modify_last_word(content_text)
            modified_content = modify_line_spaces(line_text, threshold, encoded_bit_sequence)


            ## join content as updated result.
            
            for item in modified_content:
                if item == '\\n':
                   updated_pdf_lines.append(pdf_line)
                   pdf_line = ''
                else:
                    ## Replacing all spaces and words with custom inputs
                    if item.startswith('s:'):
                        item = item.replace('s:', '')
                    elif item.startswith('w:'):
                        item = item.replace('w:', '')
                    pdf_line += item
                
                # updated_pdf_lines.append(item)
    return updated_pdf_lines


    
        

            
                

