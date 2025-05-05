from log_handler import PlagiarismLog

log = PlagiarismLog()
log.add_nickname('A', 'essay.txt')
log.add_nickname('B', 'source.txt')
log.set_buffer_length(10)

log.add_reference('A', 50, 'B', 200, 'B.1', 200, 210)
log.add_not_found('B', 'B.1', 200)

log.write_log("log_test_output.txt")
