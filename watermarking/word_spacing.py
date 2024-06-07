def find_first_occurrence_closing(string, char, start_index):
    try:
        char_index = string.index(char, start_index)
        while string[char_index+1:char_index+3] != 'TJ':
            char_index = string.index(char, char_index + 1)
        return char_index
    except ValueError:
        return -1
    
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
            find_closing_bracket = find_first_occurrence_closing(input_string, ']', index);
            transformed_input.extend(split_text(input_string[index:find_closing_bracket+1]))
            index = find_closing_bracket+1
        else:
            text_font+= input_string[index]
            index +=1
    return transformed_input

# input_string = ' [-490(F)82(or)]TJ/F43 14.3462 Tf 42.098 0 Td [(f)167(f)]TJ/F47 14.3462 Tf 15.62 0 Td [(true)]TJ/F43 14.3462 Tf 33.195 0 Td [(g)167(g)]TJ/F42 14.3462 Tf 15.62 0 Td [(C)]TJ/F43 9.9626 Tf 11.081 5.206 Td [(0)]TJ/F43 14.3462 Tf 6.903 -5.206 Td [(f)167(f)]TJ/F47 14.3462 Tf 15.621 0 Td [(true)]TJ/F43 14.3462 Tf 33.194 0 Td [(g)167(g)]TJ/F37 14.3462 Tf 11.955 0 Td [(,)-270(w)28(e)-256(ha)27(v)28(e)]TJ/F47 14.3462 Tf 58.804 0 Td [(true)]TJ/F43 14.3462 Tf 30.64 0 Td [(!)]TJ/F50 14.3462 Tf 15.457 0 Td [(wp)]TJ/F37 14.3462 Tf 16.753 0 Td [([)]TJ/F42 14.3462 Tf 3.902 0 Td [(C)]TJ/F43 9.9626 Tf 11.081 5.206 Td [(0)]TJ/F37 14.3462 Tf 3.237 -5.206 Td [(]\050)]TJ/F47 14.3462 Tf 9.365 0 Td [(true)]TJ/F37 14.3462 Tf 29.529 0 Td [(\051,)-270(whic)28(h)-256(simpli\014es)-255(to)]TJ/F47 14.3462 Tf 128.569 0 Td [(true)]TJ/F43 14.3462 Tf 30.64 0 Td [(!)]TJ/F47 14.3462 Tf 15.457 0 Td [(true)]TJ/F37 14.3462 Tf 29.529 0 Td [(,)]TJ -550.3 -16.936 Td [(whic)27(h)-326(is)-326(trivially)-327(true.)]TJ'
# print(transform_input(input_string))



