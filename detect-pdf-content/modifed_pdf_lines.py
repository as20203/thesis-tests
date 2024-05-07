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




def modify_line_spaces(line_text, space_value = 0):
    updated_content = line_text.copy()
    space_count = 0
    index = 0
    space_identifier = 'I'
    space_separator = [']','TJ','\n','1 0 0 rg 1 0 0 RG', '\n', '[({})]TJ'.format(space_identifier), '\n', '0 g 0 G', '\n', '[']
    while index < len(updated_content):
    # for index,item in enumerate(updated_content):
        item = updated_content[index]
        if item.startswith("s:"):
            space = int(item[2:])
            ## Space between words is usually negative.
            ## used -50
            ## Space between characters is usually positive
            ## if negative it represents kerning and the value is usually quite low.
            if space < 0 and space < -50:
                space_count+=1
                if space_count % 2 == 0:
                    space += space_value
                else:
                    space -= space_value
                updated_content[index] = 's:{}'.format(space)
                updated_content[index:index] = space_separator
                index += len(space_separator)
        index += 1

    return updated_content


           

def modified_pdf_lines(pdf_lines):
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
            modified_content = modify_line_spaces(line_text, 0)


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


    
        

            
                

