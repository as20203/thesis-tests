import random

def generate_random_bit_sequence(length):
    return ''.join(random.choice('01') for _ in range(length))

def encode_bit_sequence(text, bit_sequence):
    encoded_text = ""
    bit_index = 0
    for char in text:
        if char == ' ':
            # Encode the current bit within the space character
            encoded_char = char
            if bit_index < len(bit_sequence):
                if bit_sequence[bit_index] == '1':
                    # Set the LSB of the ASCII value of space to '1'
                    encoded_char = chr(ord(char) | 1)
                else:
                    # Set the LSB of the ASCII value of space to '0'
                    encoded_char = chr(ord(char) & ~1)
                bit_index += 1
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
    paragraph = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
    bit_sequence_length = 10
    random_bit_sequence = generate_random_bit_sequence(bit_sequence_length)
    print("Random Bit Sequence:", random_bit_sequence)

    # Add spaces between words in the paragraph
    paragraph_with_spaces = ' '.join(paragraph.split())
    print("Paragraph with Spaces:", paragraph_with_spaces)

    # Encode the bit sequence within the spaces
    encoded_paragraph = encode_bit_sequence(paragraph_with_spaces, random_bit_sequence)
    print("Encoded Paragraph:", encoded_paragraph)

    decoded_bit_sequence = decode_bit_sequence(encoded_paragraph)
    print("Decoded Bit Sequence:", decoded_bit_sequence)


if __name__ == "__main__":
    main()