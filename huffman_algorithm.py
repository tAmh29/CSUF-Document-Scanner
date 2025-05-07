import heapq # Heap Queue for priority queue operations

# Step 1: Define Huffman Node
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq
    
# Step 2: Build Huffman Tree
def build_huffman_tree(freq_map):
    heap = [HuffmanNode(char, freq) for char, freq in freq_map.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        new_node = HuffmanNode(None, left.freq + right.freq)
        new_node.left = left
        new_node.right = right
        heapq.heappush(heap, new_node)

    return heap[0]

# Step 3: Generate Huffman Codes
def build_codes(node, prefix="", code_map={}):
    if node is None:
        return
    
    if node.char is not None:
        code_map[node.char] = prefix
    
    build_codes(node.left, prefix + "0", code_map) #left child(0)
    build_codes(node.right, prefix + "1", code_map) #right child(1)

    return code_map 

# Step 4: Compute Huffman Encoding
def huffman_encode(text):
    freq_map = {char: text.count(char) for char in set(text)}
    root = build_huffman_tree(freq_map)
    codes = build_codes(root)
    encoded_text = ''.join(codes[char] for char in text)
    
    return encoded_text, codes

# Step 5: Translate Huffman Decoding
def huffman_decode(encoded_text, huffman_codes):
    reversed_codes = {code: char for char, code in huffman_codes.items()}

    decode_text = ""
    temp_code = ""

    for bit in encoded_text:
        temp_code += bit

        if temp_code in reversed_codes:
            decode_text += reversed_codes[temp_code]
            temp_code = ""
        
    return decode_text