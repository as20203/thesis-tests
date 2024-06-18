import os
import encode_pdf
from datetime import datetime
import decode_pdf
import Levenshtein
import random

def generate_random_bit_sequence(length):
    random.seed(12345)
    return ''.join(random.choice('01') for _ in range(length))

def list_pdf_files(directory):
    pdf_files = []
    
    # Iterate through all the files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_files.append(filename)
    
    return pdf_files


def create_output_folder(current_directory, base_folder_name, current_time):
    
    
    # Create the folder name with the timestamp
    folder_name_with_timestamp = f"{base_folder_name}_{current_time}"
    
    # Define the path for the new folder
    output_folder_path = os.path.join(current_directory, folder_name_with_timestamp)
    
    # Create the folder if it doesn't exist
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
        print(f"Folder '{folder_name_with_timestamp}' created successfully at {output_folder_path}")
    else:
        print(f"Folder '{folder_name_with_timestamp}' already exists at {output_folder_path}")
    return output_folder_path


def read_parameters(file_path):
    parameters = {}
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Strip whitespace from the line
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Split the line into key and value
                key, value = line.split('=', 1)
                
                # Strip whitespace from key and value
                key = key.strip()
                value = value.strip()
                
                # Convert value to appropriate type if necessary
                if value.isdigit():
                    value = int(value)
                elif value.replace('.', '', 1).isdigit() and value.count('.') < 2:
                    value = float(value)
                elif value.lower() in ['true', 'false']:
                    value = value.lower() == 'true'
                
                # Add to dictionary
                parameters[key] = value
    except Exception as e:
        print(f"Error reading parameters from file: {e}")
    
    return parameters




def compute_edit_distance(str1, str2):
    return Levenshtein.distance(str1, str2)



if __name__ == "__main__":

    file_path = 'parameters.txt'
    params = read_parameters(file_path)

    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    in_file = params['input']
    base_folder_name = params['baseFoldername']
    sequence_length = params['sequenceLength']
    threshold = params['threshold']
    current_directory = os.getcwd()
    output_folder_path = create_output_folder(current_directory, base_folder_name, current_time)
    
    # Example usage
    pdf_files = list_pdf_files(in_file)

    ## Read all files in a folder
    combined_pdf_error_rate = 0
    for pdf_file in pdf_files:
        encoded_bit_sequence = generate_random_bit_sequence(sequence_length)
        print(encoded_bit_sequence)
        input_filename = pdf_file.replace(os.path.splitext(pdf_file)[1], "")
        output_filename = f"{current_time}_{input_filename}"
        filename_base = in_file + input_filename + '.pdf'
        current_directory = output_folder_path
        output_file_path = create_output_folder(current_directory, input_filename,current_time)
        ## Encode the pdf
        scanned_filename = encode_pdf.encode_pdf(output_filename, filename_base, output_file_path, encoded_bit_sequence, threshold)

        ## Decode the pdf
        original_pdf = decode_pdf.get_pdf_lines(in_file + input_filename, output_file_path)
        modified_pdf = decode_pdf.get_pdf_lines(scanned_filename, output_file_path, encoded_bit_sequence)
        print(modified_pdf)
        result,  decoded_string = decode_pdf.get_decoded_text(original_pdf, modified_pdf, len(encoded_bit_sequence))

        # pdf_error_rate = decode_pdf.get_decoded_text_substring(encoded_bit_sequence,result)
        ## compute edit distance
        levenshtein_distance = compute_edit_distance(encoded_bit_sequence, decoded_string)
        print('Encoded String: ', encoded_bit_sequence)
        print('Decoded String: ', decoded_string)
        print(levenshtein_distance)
        # combined_pdf_error_rate += pdf_error_rate
    
    # print('Combined pdf error rate : ', combined_pdf_error_rate/len(pdf_files))
