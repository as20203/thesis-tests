import random

def generate_bit_sequence(length):
    return ''.join(random.choice('01') for _ in range(length))

def encode_bit_sequence(bit_sequence):
    # Convert the binary string to a list of integers
    bit_list = [int(bit_sequence[i:i+8], 2) for i in range(0, len(bit_sequence), 8)]
    print('bit_list: ', bit_list)
    # Convert integers to corresponding ASCII characters
    encoded_text = ''.join(chr(bit) for bit in bit_list)
    return encoded_text

def hide_bit_sequence(text, encoded_bit_sequence):
    # Choose a random index to hide the bit sequence within the text
    index = random.randint(0, len(text) - len(encoded_bit_sequence))
    # Insert the encoded bit sequence into the text at the chosen index
    return text[:index] + encoded_bit_sequence + text[index:]

def decode_bit_sequence(encoded_text):
    # Convert each character in the encoded text back to its ASCII integer value
    ascii_values = [ord(char) for char in encoded_text]
    print(ascii_values)
    # Convert ASCII integers to binary strings and concatenate them
    bit_sequence = ''.join(format(value, '08b') for value in ascii_values)
    return bit_sequence

def main():
    text = "The quick brown fox jumped over the lazy dog."
    bit_sequence = generate_bit_sequence(16)  # Change the length as needed
    encoded_bit_sequence = encode_bit_sequence(bit_sequence)
    hidden_text = hide_bit_sequence(text, encoded_bit_sequence)
    print("Original Text:", text)
    print("Hidden Bit Sequence:", bit_sequence)
    print("Encoded Bit Sequence:", encoded_bit_sequence.split(' '))
    print("Text with Hidden Bit Sequence:", hidden_text)

    decoded_bit_sequence = decode_bit_sequence(encoded_bit_sequence)
    print("Decoded Bit Sequence:", decoded_bit_sequence)
if __name__ == "__main__":
    main()
