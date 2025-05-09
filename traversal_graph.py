import os

def create_traversal_graph(log_path):
    graph = {}
    current_section = None

    with open(log_path, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]

    for i, line in enumerate(lines):
        # Detect section like "#A Section"
        if line.startswith("#") and len(line) > 2 and "Section" in line:
            current_section = line[1]
            if current_section not in graph:
                graph[current_section] = []
            continue

        # Match lines like: A: 5 > B: 20
        if ">" in line and ":" in line and "$" not in line:
            src_part, tgt_part = map(str.strip, line.split(">"))
            src_letter = src_part.split(":")[0].strip()
            tgt_letter = tgt_part.split(":")[0].strip()
            if src_letter not in graph:
                graph[src_letter] = []
            graph[src_letter].append(tgt_letter)

    return graph
