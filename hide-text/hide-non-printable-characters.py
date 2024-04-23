import random

def generate_random_bit_sequence(length):
    return ''.join(random.choice('01') for _ in range(length))

def encode_bit_sequence(text, bit_sequence):
    encoded_text = ""
    bit_index = 0
    for char in text:

         # Check if the bit sequence is fully encoded
        if bit_index >= len(bit_sequence):
            encoded_text += char
            continue

        if char == ' ':
            encoded_text += ' '
            # Add an extra space before replacing it with a non-printable ASCII character
            if (bit_sequence[bit_index] == '0'):
                char = chr(22)
            else:
                char = chr(17)
        
       
        
        # Encode the current bit within the character
        encoded_char = char
        if ord(char) < 32:  # If the character is non-printable
            if bit_sequence[bit_index] == '1':
                # Set the LSB of the ASCII value to '1'
                encoded_char = chr(ord(char) | 1)
            else:
                # Set the LSB of the ASCII value to '0'
                encoded_char = chr(ord(char) & ~1)
            bit_index += 1
        encoded_text += encoded_char
    return encoded_text


def decode_bit_sequence(encoded_text):
    decoded_sequence = ""
    for char in encoded_text:
        # Check if the character is non-printable
        if ord(char) < 32:
            # Extract the LSB of the ASCII value
            if ord(char) == 22:
                decoded_sequence += '0'
            
            if ord(char) == 17:
                decoded_sequence += '1'
            
    return decoded_sequence

def main():
    paragraph = "dfkdjfd dfjd kdfjkdjfdkjd k jdfkd kjdkfjdk d djdkjdfkdj fkjd kdkdfjkjd jdk d kj dk jdkj"
    bit_sequence_length = 10
    random_bit_sequence = generate_random_bit_sequence(bit_sequence_length)
    print("Random Bit Sequence:", random_bit_sequence)

    # Encode the bit sequence within the paragraph
    encoded_paragraph = encode_bit_sequence(paragraph, random_bit_sequence)
    print("Encoded Paragraph:", encoded_paragraph)

    decoded_paragraph_bits = decode_bit_sequence(encoded_paragraph)
    print('Decoded paragraph bits: ', decoded_paragraph_bits)

if __name__ == "__main__":
    main()