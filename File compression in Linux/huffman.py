import heapq
import pickle

def build_frequency_table(data):
    frequency_table = {}
    for byte in data:
        if byte in frequency_table:
            frequency_table[byte] += 1
        else:
            frequency_table[byte] = 1
    return frequency_table

class HuffmanNode:
    def __init__(self, byte=None, frequency=0):
        self.byte = byte
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

def build_huffman_tree(frequency_table):
    priority_queue = []
    for byte, frequency in frequency_table.items():
        node = HuffmanNode(byte, frequency)
        heapq.heappush(priority_queue, node)

    while len(priority_queue) > 1:
        left_node = heapq.heappop(priority_queue)
        right_node = heapq.heappop(priority_queue)
        internal_node = HuffmanNode(frequency=left_node.frequency + right_node.frequency)
        internal_node.left = left_node
        internal_node.right = right_node
        heapq.heappush(priority_queue, internal_node)

    return heapq.heappop(priority_queue)

def build_huffman_code_table(huffman_tree):
    code_table = {}
    def traverse(node, code):
        if node.byte is not None:
            code_table[node.byte] = code
        else:
            traverse(node.left, code + '0')
            traverse(node.right, code + '1')

    traverse(huffman_tree, '')
    return code_table

def compress_huffman(input_file, output_file):
    with open(input_file, 'rb') as file:
        data = file.read()

    frequency_table = build_frequency_table(data)
    huffman_tree = build_huffman_tree(frequency_table)
    code_table = build_huffman_code_table(huffman_tree)

    with open(output_file, 'wb') as file:
        pickle.dump(frequency_table, file)
        file.write(len(data).to_bytes(4, byteorder='big'))
        current_byte = 0
        bit_count = 0
        for byte in data:
            code = code_table[byte]
            for bit in code:
                current_byte <<= 1
                if bit == '1':
                    current_byte |= 1
                bit_count += 1
                if bit_count == 8:
                    file.write(current_byte.to_bytes(1, byteorder='big'))
                    current_byte = 0
                    bit_count = 0

        if bit_count > 0:
            current_byte <<= (8 - bit_count)
            file.write(current_byte.to_bytes(1, byteorder='big'))

def decompress_huffman(input_file, output_file):
    with open(input_file, 'rb') as file:
        frequency_table = pickle.load(file)
        original_size = int.from_bytes(file.read(4), byteorder='big')

        huffman_tree = build_huffman_tree(frequency_table)

        with open(output_file, 'wb') as output:
            current_node = huffman_tree
            remaining_bits = original_size
            byte = file.read(1)
            while byte:
                bits = bin(int.from_bytes(byte, byteorder='big'))[2:].rjust(8, '0')
                for bit in bits:
                    if bit == '0':
                        current_node = current_node.left
                    else:
                        current_node = current_node.right

                    if current_node.byte is not None:
                        output.write(current_node.byte.to_bytes(1, byteorder='big'))
                        remaining_bits -= 1
                        if remaining_bits == 0:
                            return

                        current_node = huffman_tree

                byte = file.read(1)

# Example usage for Huffman coding compression
compress_huffman('input.txt', 'compressed.bin')
decompress_huffman('compressed.bin', 'output.txt')



