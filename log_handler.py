import os
import huffman_handler
import re
from datetime import datetime

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


    def checkOverlap(start_a,end_a,start_b,end_b):
        return max(start_a,start_b) < min(end_a,end_b)


    # returns <"Overlap"> if there is an overlap
    # returns <"Join"> if two indices touch like (1,2)(3,4)
    def add_reference(self, src_letter, src_index, target_letter, target_index, ref_label, ref_start, ref_end):
        """Adds a reference found between two documents."""
        if src_letter not in self.sections: ### if we don't have an exact duplicate
            self.sections[src_letter] = []
        ## We need to look for a linked reference here.
        count_a = 0
        print("outside loop")
        for reference in self.sections[src_letter]:
            print("inloop",count_a)
            count_a += 1
            ## this basically checks if there is overlap between indicies e.g. (2,5) and (3,7)
            if (target_letter == reference["target_letter"]):
                if (max(ref_start,reference["ref_start"]) <= min(ref_end,reference["ref_end"])): ## double check this if weird overlapping stuff happens
                    reference["src_index"] = min(src_index,reference["src_index"]) ## new src index
                    ## no new target letter
                    reference["target_index"]= min(target_index,reference["target_index"]) ## new target index
                    ## keep old reference label. may need to return that reference was modified
                    reference["ref_start"] = min(ref_start,reference["ref_start"]) ## new ref start
                    reference["ref_end"] = max(ref_end,reference["ref_end"]) ## new ref end
                    self.clean_log(src_letter,target_letter)
                    return "Overlap"
                ## are the two adjacent?
                elif (ref_end + 1 == reference["ref_start"]):
                    ### so if new insertion is before an existing reference
                    reference["src_index"] = src_index ##starting index so it's given the new one
                    ## target letter the same
                    reference["target_index"] = target_index ## starting index
                    ## no ref label change
                    reference["ref_start"] = ref_start ## strting index
                    #ref end stays the same
                    self.clean_log(src_letter,target_letter)
                    return "Before"
                elif (reference["ref_end"]+ 1 == ref_start):
                    ##new insertion after existing reference
                    ##src starting index stays same
                    ##target letter stays the same
                    ##target index stays the same
                    ## no ref label change
                    ## no ref start change
                    reference["ref_end"] = ref_end
                    self.clean_log(src_letter,target_letter)
                    return "After"
        self.sections[src_letter].append({
            'src_index': src_index,
            'target_letter': target_letter,
            'target_index': target_index,
            'ref_label': ref_label,
            'ref_start': ref_start,
            'ref_end': ref_end
        })
        self.clean_log(src_letter,target_letter)
        return "New"



    ## This is a bodged solution to the poor writing of the above algorithm 
    def clean_log(self,src_letter,target_letter):
        for reference in self.sections[src_letter]: ###a is
            if reference["target_letter"] != target_letter:
                continue
            for other_reference in self.sections[src_letter]:
                if (other_reference["target_letter"] != target_letter) or (reference == other_reference):
                    continue
                if(max(reference["ref_start"],other_reference["ref_start"])) <= min(reference["ref_end"],other_reference["ref_end"]):
                    reference["src_index"]= min(reference["src_index"],other_reference["src_index"])
                    reference["target_index"]= min(other_reference["target_index"],reference["target_index"])
                    reference["ref_start"] = min(other_reference["ref_start"],reference["ref_start"])
                    reference["ref_end"] = max(other_reference["ref_end"],reference["ref_end"])
                elif (other_reference["ref_end"] + 1 == reference["ref_start"]):
                    reference["src_index"] = other_reference["src_index"]
                    reference["target_index"] = other_reference["target_index"]
                    reference["ref_start"] = other_reference["ref_start"]
                elif (reference["ref_end"]+ 1 == other_reference["ref_start"]):
                    reference["ref_end"] = other_reference["ref_end"]
        #self.del_duplicates(src_letter,target_letter)


    # def del_duplicates(self,src_letter,target_letter):
        
    #     # for a in self.sections[src_letter]:
    #     #     for b in self.sections[src_letter]:
    #     #         if (a["src_index"] == b["src_index"]):
    #     #             if (a["ref_start"] == b["ref_start"]) and (a["ref_end"] == b["ref_end"]):
    #     #                 if (a["target_index"] == b["target_index"]) and (a["target_letter"] == b["target_letter"]):
    #     #                     if (a["ref_label"] != b["ref_label"]):
    #     new_ref_list = []
    #     new_ref_list.append(self.sections[src_letter][0])
    #     for i in range(1,len(self.sections[src_letter])):

    def dedup_dicts(data, ignore_key):
        seen = set()
        result = []
        for item in data:
            # Create a hashable representation excluding the ignore_key
            identity = tuple(sorted((k, v) for k, v in item.items() if k != ignore_key))
            if identity not in seen:
                seen.add(identity)
                result.append(item)
        return result


                                
                            


    def add_not_found(self, src_letter, src_label, src_index):
        """Adds an entry indicating a reference was not found in other documents."""
        if src_letter not in self.sections:
            self.sections[src_letter] = []
        self.sections[src_letter].append({
            'src_label': src_label,
            'src_index': src_index,
            'not_found': True
        })

    def get_creation_time(self):

        current_time = datetime.now()
        current_time_string = str(current_time.month) + "_" + str(current_time.day) + "_" + str(current_time.hour) + "_" + str(current_time.minute) + "." + str(current_time.second) 

        return current_time_string

    def compress_log(self, log_file):

        huffman_output_directory, huffman_codes_output = huffman_handler.create_huffman_directories()
        time_of_compression = huffman_handler.get_current_time()
        encoded_file_ouput = huffman_handler.get_output_file_path(huffman_output_directory,"encoded",time_of_compression,".bin")
        huffman_code_file_output = huffman_handler.get_output_file_path(huffman_codes_output,"huffman_codes",time_of_compression,".txt")
        encoded_text, code = huffman_handler.encode_log(log_file)
        huffman_handler.to_bitarray_write(encoded_file_ouput, encoded_text)
        huffman_handler.write_file(huffman_code_file_output,code)

        return encoded_file_ouput, huffman_code_file_output
        
    def write_log(self):
        """Writes the collected log data to a file inside the 'logOutput' directory."""
        # Ensure the output directory exists
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logOutput")
        os.makedirs(output_dir, exist_ok=True)

        # Full path to the log file
        full_filename = "log_" + self.get_creation_time() + ".txt"
        full_path = os.path.join(output_dir, full_filename)

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

        return full_path




#    def parse_log(self, filepath):
#        """Parses a plagiarism log file and returns a PlagiarismLog object."""
#        log = PlagiarismLog()
#
#        current_section = None
#        with open(filepath, 'r') as f:
#            lines = [line.strip() for line in f if line.strip()]
#
#        i = 0
#        while i < len(lines):
#            line = lines[i]
#
#            if line.startswith('#@'):
#                i += 1
#                while i < len(lines) and lines[i] != '*' and not lines[i].startswith('#'):
#                    if '=' in lines[i]:
#                        letter, filename = map(str.strip, lines[i].split('='))
#                        log.add_nickname(letter, filename)
#                    i += 1
#                i += 1  # skip the '*' after each mapping
#                continue
#
#            elif line.startswith('#?'):
#                # Extract buffer length
#                match = re.search(r'#\? (\d+)', line)
#                if match:
#                    log.set_buffer_length(int(match.group(1)))
#                i += 1
#                continue
#
#            elif line.startswith('#') and len(line) == 2:
#                current_section = line[1]
#                i += 1
#                continue
#
#            # Handle section content
#            if current_section and ':' in line and '>' in line:
#                # Read source line
#                if '>' in line and '$' in line:
#                    # Not found entry
#                    src_label, rest = line.split(':')
#                    src_index = int(rest.split('>')[0].strip())
#                    log.add_not_found(current_section, line.split('>')[0].strip(), src_index)
#                    i += 1  # move to the % line
#                    i += 1  # skip '*'
#                    continue
#                else:
#                    # Standard match entry
#                    src_info, target_info = map(str.strip, line.split('>'))
#                    src_letter, src_index = src_info.split(':')
#                    target_letter, target_index = target_info.split(':')
#
#                    i += 1
#                    ref_line = lines[i]
#                    i += 1  # skip '*'
#                    if '%' in ref_line:
#                        _, ref_data = ref_line.split('%', 1)
#                        ref_data = ref_data.strip()
#                        ref_label, ref_range = ref_data.split(':')
#                        ref_start, ref_end = map(int, ref_range.strip().split('-'))
#
#                        log.add_reference(
#                            src_letter.strip(),
#                            int(src_index),
#                            target_letter.strip(),
#                            int(target_index),
#                            ref_label.strip(),
#                            ref_start,
#                            ref_end
#                        )
#                    continue
#            else:
#                i += 1
#
#        return log
#   

    def parse_log(self, filepath):
        log = PlagiarismLog()

        current_section = None
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]

        i = 0
        while i < len(lines):
            line = lines[i]

            # Nickname-Filename section
            if line.startswith('#@'):
                i += 1
                while i < len(lines):
                    if lines[i] == '*':
                        i += 1
                        continue
                    elif lines[i].startswith('#'):
                        break
                    if '=' in lines[i]:
                        letter, filename = map(str.strip, lines[i].split('='))
                        log.add_nickname(letter, filename)
                    i += 1
                continue

            # Buffer length
            elif line.startswith('#?'):
                match = re.search(r'#\? (\d+)', line)
                if match:
                    log.set_buffer_length(int(match.group(1)))
                i += 1
                continue

            # Section start
            elif line.startswith('#') and len(line) > 1:
                current_section = line[1]
                i += 1
                continue

            # Process entries within a section
            if current_section:
                # Detect standard match: A: 15 > B: 105
                if '>' in line and ':' in line and not '$' in line:
                    src_part, tgt_part = map(str.strip, line.split('>'))
                    src_letter, src_index = src_part.split(':')
                    tgt_letter, tgt_index = tgt_part.split(':')

                    i += 1
                    if i < len(lines) and lines[i].startswith('%'):
                        ref_line = lines[i][1:].strip()  # remove leading %
                        ref_label, ref_range = ref_line.split(':')
                        ref_start, ref_end = map(int, ref_range.strip().split('-'))

                        log.add_reference(
                            src_letter,
                            int(src_index),
                            tgt_letter,
                            int(tgt_index),
                            ref_label.strip(),
                            ref_start,
                            ref_end
                        )
                        i += 1  # skip '*'
                        if i < len(lines) and lines[i] == '*':
                            i += 1
                    else:
                        # malformed block — skip
                        i += 1
                    continue

                # Not found line: B.1: 105 > $
                elif '>' in line and '$' in line:
                    left, _ = map(str.strip, line.split('>'))
                    src_label, src_index = map(str.strip, left.split(':'))

                    log.add_not_found(current_section, src_label, int(src_index))

                    i += 1  # % -1 line
                    i += 1  # '*' line
                    continue

            i += 1

        return log


