import os
import huffman_algorithm as huffman
from bitarray import bitarray
from datetime import datetime
from pathlib import Path


#Creates directories needed for storing huffman file outputs and then later decompressing those files
def create_huffman_directories():

    print(__file__)

    current_directory = os.path.dirname(__file__)
    print(current_directory)

    compression_directory = os.path.join(current_directory, "huffmanCompressions")
    huffman_code_directories = os.path.join(current_directory, "huffmanCodes")

    print(compression_directory)
    print(huffman_code_directories)

    # if the mainFileDirectory is not present then create it. 
    if not os.path.exists(compression_directory):
        os.makedirs(compression_directory)
        print(f"Directory Created: {compression_directory}")

    # if the referenceFileDirectory is not present then create it. 
    if not os.path.exists(huffman_code_directories):
        os.makedirs(huffman_code_directories)
        print(f"Directory Created: {huffman_code_directories}")
    
    return (compression_directory,huffman_code_directories)

def get_output_file_path(directory_path, file_name, creation_time, extension):

    full_file_name = file_name + "_" + creation_time + "_" + extension

    full_output_path = Path(directory_path) / full_file_name

    return full_output_path

def get_current_time():
    current_time = datetime.now()
    current_time_string = str(current_time.month) + "_" + str(current_time.day) + "_" + str(current_time.hour) + "_" + str(current_time.minute) + "." + str(current_time.second)

    return current_time_string

#calls the huffman algo huffman_encode function
def encode_log(log_file):

    encoded_text,code = huffman.huffman_encode(log_file)

    return encoded_text, code

#calls the huffman algo huffman_decode function
def decode_log(compressed_log_file, huffman_codes):

    decompressed_text = huffman.huffman_decode(compressed_log_file,huffman_codes)

    return decompressed_text

def read_file(file_path):
    
    with open(file_path, 'r') as file:
        text = ' '.join(line.strip() for line in file) # Read the content of the file line by line
    file.close() # Close the file after reading 
    return text

def write_file(file_path, data_to_write):
    
    with open(file_path, 'w') as file:
        file.write(data_to_write)

    return file_path

#sets up log file path 

def to_bitarray_write(file_path, encoded_text):
    
    #Converts the text to a bit array for storage
    bits = bitarray(encoded_text)
    with open(file_path, 'wb') as file:
        bits.tofile(file)
    print(f"\nData written to {file_path}...")

    # Read the binary data from the file and convert back to a binary string
    bits = bitarray()
    with open(file_path, 'rb') as file:
        bits.fromfile(file)
    encoded_text_from_file = bits.to01()

    # Ensure the length of the binary string matches the original length
    encoded_text_from_file = encoded_text_from_file[:len(encoded_text)]

    return encoded_text_from_file

def read_to_bitarray(file_path):

    bits = bitarray()
    with open(file_path, 'rb') as file:
        bits.fromfile(file)
    encoded_text_from_file = bits.to01()

    return encoded_text_from_file

