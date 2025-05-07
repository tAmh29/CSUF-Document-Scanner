from log_handler import PlagiarismLog
import huffman_handler
import os

log = PlagiarismLog()
log.add_nickname('A', 'essay.txt')
log.add_nickname('B', 'source.txt')
log.set_buffer_length(10)

log.add_reference('A', 50, 'B', 200, 'B.1', 200, 210)
log.add_reference('A', 70, 'B', 260, 'B.2', 260, 280)
log.add_reference('A', 145, 'C', 180, 'C.1', 180, 200)
log.add_not_found('B', 'B.1', 200)

log.write_log("log_test_output.txt")

parsed_log = log.parse_log("logOutput/log_test_output.txt")

# Access recovered data
print(log.nickname_map)
print(log.buffer_length)
print(log.sections['A'])  # list of dicts
