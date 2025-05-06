import os
from Algorithm import bfs, dfs

def create_traversal_graph(log_path=None):
    if log_path is None:
        log_path = os.path.join(os.path.dirname(__file__), "plagiarism_log.txt")

    graph = {}
    with open(log_path, 'r') as file:
        for line in file:
            if "::" not in line:
                continue
            parts = line.strip().split("::")
            connection = parts[0].strip()
            if "-->" not in connection:
                continue
            src, dest = connection.split("-->")
            src, dest = src.strip(), dest.strip()

            if src not in graph:
                graph[src] = []
            graph[src].append(dest)
    return graph
