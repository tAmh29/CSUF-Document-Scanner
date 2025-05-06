import os
import huffman_handler

class PlagiarismLog:
    def __init__(self):
        self.nickname_map = {}     # Maps nicknames (A, B, etc.) to filenames
        self.buffer_length = 0
        self.sections = {}         # Holds log entries for each section (A, B, C...)

    def add_nickname(self, letter, filename):
        """Assigns a nickname letter to a filename."""
        self.nickname_map[letter] = filename

    def set_buffer_length(self, length):
        """Sets the buffer length for context checks."""
        self.buffer_length = length

    def add_reference(self, src_letter, src_index, target_letter, target_index, ref_label, ref_start, ref_end):
        """Adds a reference found between two documents."""
        if src_letter not in self.sections:
            self.sections[src_letter] = []
        self.sections[src_letter].append({
            'src_index': src_index,
            'target_letter': target_letter,
            'target_index': target_index,
            'ref_label': ref_label,
            'ref_start': ref_start,
            'ref_end': ref_end
        })

    def add_not_found(self, src_letter, src_label, src_index):
        """Adds an entry indicating a reference was not found in other documents."""
        if src_letter not in self.sections:
            self.sections[src_letter] = []
        self.sections[src_letter].append({
            'src_label': src_label,
            'src_index': src_index,
            'not_found': True
        })

    def compress_log(self, log_file):

        huffman_output_directory, huffman_codes_output = huffman_handler.create_huffman_directories()
        time_of_compression = huffman_handler.get_current_time()
        encoded_file_ouput = huffman_handler.get_output_file_path(huffman_output_directory,"encoded",time_of_compression,".bin")
        huffman_code_file_output = huffman_handler.get_output_file_path(huffman_codes_output,"huffman_codes",time_of_compression,".txt")
        encoded_text, code = huffman_handler.encode_log(log_file)
        huffman_handler.to_bitarray_write(encoded_file_ouput, encoded_text)
        huffman_handler.write_file(huffman_code_file_output,code)

        return encoded_file_ouput, huffman_code_file_output
        
    def write_log(self, filename):
        """Writes the collected log data to a file inside the 'logOutput' directory."""
        # Ensure the output directory exists
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logOutput")
        os.makedirs(output_dir, exist_ok=True)

        # Full path to the log file
        full_path = os.path.join(output_dir, filename)

        with open(full_path, 'w') as f:
            # Header: Nickname-Filename assignments
            f.write("#@ Nickname-Filename values\n\n")
            for letter, fname in self.nickname_map.items():
                f.write(f"{letter} = {fname}\n*\n")

            # Buffer length section
            f.write(f"\n#? {self.buffer_length} Buffer length\n\n")

            # Log sections
            for letter in sorted(self.sections.keys()):
                f.write(f"#{letter} Section\n\n")
                for entry in self.sections[letter]:
                    if entry.get('not_found'):
                        f.write(f"{entry['src_label']}: {entry['src_index']} > $\n")
                        f.write("% -1\n*\n")
                    else:
                        f.write(f"{letter}: {entry['src_index']} > {entry['target_letter']}: {entry['target_index']}\n")
                        f.write(f"% {entry['ref_label']}: {entry['ref_start']}-{entry['ref_end']}\n*\n")
                f.write("\n")

        self.compress_log(full_path)
