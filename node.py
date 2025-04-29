class Node:
    def __init__(self, document_name, data=None): 
        self.document_name = document_name
        self.data = data
        self.edges = {}

    def add_edge(self, neighbor_node, weight=1): # Create a directed edge to another node
        self.edges[neighbor_node] = weight

    def get_neighbors(self): # Retrieve all neighboring nodes
        return list(self.edges.keys())

    def __repr__(self):
        return f"Node({self.document_name})"
