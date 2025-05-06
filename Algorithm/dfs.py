def dfs(graph, node, visited=None, result=None):
    if visited is None:
        visited = set()
    if result is None:
        result = []

    if node not in visited:
        visited.add(node)
        result.append(node)
        for neighbor in graph.get(node, []):
            dfs(graph, neighbor, visited, result)
    return result