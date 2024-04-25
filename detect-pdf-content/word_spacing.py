def find_first_occurrence(string, char, start_index):
    try:
        return string.index(char, start_index)
    except ValueError:
        return -1

def write_array_to_file(array, filename):
    with open(filename, 'w') as file:
        for item in array:
            file.write(str(item) + '\n')
    
def split_text(input_string):
    text_with_spaces = []
    index = 0
    while index < len(input_string):
        if input_string[index] == '[':
            text_with_spaces.append(input_string[index])
            index += 1
        if input_string[index] == '(':
            find_closing_bracket = find_first_occurrence(input_string, ')', index)
            text = 'w:' + input_string[index:find_closing_bracket+1]
            text_with_spaces.append(text)
            index = find_closing_bracket + 1
        
        word_space =  find_first_occurrence(input_string, '(', index)
        if word_space != -1:
            space = input_string[index:word_space]
            text_with_spaces.append('s:'+space)
            index = word_space
        else:
            index +=1
    text_with_spaces.append(']')
    return text_with_spaces

def transform_input(input_string):
    # Split the input string into a list of strings
    transformed_input = []
    text_font = ''
    index = 0
    while index < len(input_string):
        if input_string[index] == '[':
            transformed_input.append(text_font)
            text_font = ''
            find_closing_bracket = find_first_occurrence(input_string, ']', index);
            transformed_input.extend(split_text(input_string[index:find_closing_bracket+1]))
            index = find_closing_bracket+1
        else:
            text_font+= input_string[index]
            index +=1
    return transformed_input




