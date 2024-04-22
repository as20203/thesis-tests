import random

def generate_random_bit_sequence(length):
    return ''.join(random.choice('01') for _ in range(length))

def add_spaces_between_words(sentence, num_spaces):
    words = sentence.split()
    spaces_indices = random.sample(range(len(words) - 1), num_spaces)
    spaces_indices.sort()
    for index in spaces_indices:
        words[index] += ' '
    return ' '.join(words)

def encode_bit_sequence(text, bit_sequence):
    encoded_text = ""
    for bit, char in zip(bit_sequence, text):
        print(bit, char)
        if char == ' ':
            # Encode the bit sequence within the space character
            if bit == '1':
                # Set the LSB of the ASCII value of space to '1'
                encoded_char = chr(ord(char) | 1)
            else:
                # Set the LSB of the ASCII value of space to '0'
                encoded_char = chr(ord(char) & ~1)
        else:
            encoded_char = char
        encoded_text += encoded_char
    return encoded_text

def decode_bit_sequence(text):
    decoded_sequence = ""
    for char in text:
        if char == ' ':
            # Extract the LSB of the ASCII value of the space character
            bit = ord(char) & 1
            decoded_sequence += str(bit)
    return decoded_sequence

def main():
    text = "The quick brown fox jumped over the lazy dog."
    num_spaces = 2  # Change the number of spaces as needed
    random_bit_sequence = generate_random_bit_sequence(num_spaces)
    print("Random Bit Sequence:", random_bit_sequence)

    # Add spaces between words in the sentence
    text_with_spaces = add_spaces_between_words(text, num_spaces)
    print("Text with Spaces:", text_with_spaces)

    # Encode the bit sequence within the spaces
    encoded_text = encode_bit_sequence(text_with_spaces, random_bit_sequence)
    print("Encoded Text:", encoded_text)

    decoded_bit_sequence = decode_bit_sequence(encoded_text)
    print("Decoded Bit Sequence:", decoded_bit_sequence)

if __name__ == "__main__":
    main()