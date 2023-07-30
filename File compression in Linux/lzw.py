def compress(input_file, output_file):
    # Initialize the dictionary with single character entries
    dictionary = {chr(i): i for i in range(256)}
    next_code = 256  # Next available dictionary code

    # Read the input file
    with open(input_file, 'rb') as f:
        data = f.read()

    compressed_data = []
    current_code = ''
    for byte in data:
        # Convert byte to character
        character = chr(byte)

        # Append the character to the current code
        current_code += character

        # Check if the current code is in the dictionary
        if current_code not in dictionary:
            # Add the current code to the dictionary
            dictionary[current_code] = next_code
            next_code += 1

            # Write the code for the previous code to the output file
            compressed_data.append(dictionary[current_code[:-1]])

            # Start a new code with the current character
            current_code = character

    # Write the last code to the output file
    compressed_data.append(dictionary[current_code])

    # Write the compressed data to the output file
    with open(output_file, 'wb') as f:
        for code in compressed_data:
            # Write 2 bytes per code
            f.write((code >> 8).to_bytes(1, byteorder='big'))
            f.write((code & 0xFF).to_bytes(1, byteorder='big'))

    print('Compression complete.')


def decompress(input_file, output_file):
    # Initialize the dictionary with single character entries
    dictionary = {i: chr(i) for i in range(256)}
    next_code = 256  # Next available dictionary code

    # Read the input file
    with open(input_file, 'rb') as f:
        data = f.read()

    decompressed_data = []
    current_code = ''
    previous_code = None
    for i in range(0, len(data), 2):
        # Read 2 bytes per code
        code = int.from_bytes(data[i:i+2], byteorder='big')

        # Check if the code is in the dictionary
        if code in dictionary:
            entry = dictionary[code]
        elif code == next_code:
            entry = current_code + current_code[0]
        else:
            raise ValueError('Invalid compressed data')

        # Write the entry to the output file
        decompressed_data.append(entry)

        if previous_code is not None:
            # Add the previous code + entry[0] to the dictionary
            dictionary[next_code] = dictionary[previous_code] + entry[0]
            next_code += 1

        previous_code = code
        current_code = entry

    # Write the decompressed data to the output file
    with open(output_file, 'wb') as f:
        f.write(''.join(decompressed_data).encode())

    print('Decompression complete.')


# Usage: compress(input_file_path, compressed_file_path)
compress('input.txt', 'compressed.bin')

# Usage: decompress(compressed_file_path, output_file_path)
decompress('compressed.bin', 'output.txt')
