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
    

# Test the function with your input
input_string = "/F39 20.6625 Tf 126.285 1033.335 Td [(1)-1125(Assignmen)31(t)-375(2.5)]TJ/F39 17.2154 Tf 0 -36.125 Td [(1.1)-1125(Exercises)-375(1)]TJ/F37 14.3462 Tf 0 -26.202 Td [(Consider )-326(the)-327(pro)1(gram)]TJ/F42 14.3462 Tf 138.988 0 Td [(C)]TJ/F37 14.3462 Tf 15.763 0 Td [(and)-326(pre-)-327(and)-326(p)-27(ostconditions)]TJ/F42 14.3462 Tf 176.916 0 Td [(F)]TJ/F37 14.3462 Tf 15.727 0 Td [(and)]TJ/F42 14.3462 Tf 27.314 0 Td [(H)]TJ/F37 14.3462 Tf 17.429 0 Td [(as)-326(follo)27(ws:)]TJ"
output = transform_input(input_string)
print(output)
write_array_to_file(output,'output.txt')



