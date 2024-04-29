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
           

def modified_pdf_lines(pdf_lines):
    updated_pdf_lines = []
    pdf_line = ''
    for item in pdf_lines:
        content_adjustment = item['line-adjustment']
        content_text = item['content']
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

        if content_text and isinstance(content_text,list):
            ## Do our changes here
            ## modify spaces or change words etc.
            ## ToDo write code that will now modify the words and spaces.
            modified_content = modify_last_word(content_text)

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
    
        

            
                

