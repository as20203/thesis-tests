import re

def detect_spaces(string):
    # Using regular expression to split the string into words and spaces
    tokens = re.findall(r'\S+|\s', string)
    # Removing punctuation marks from the result
    tokens = [token.strip('.') for token in tokens]
    return tokens

input_string = "my  name is jawad."
result = detect_spaces(input_string)