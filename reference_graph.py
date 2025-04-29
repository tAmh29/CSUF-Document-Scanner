from node import Node

class ReferenceGraph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, document_name, data=None): # Create a new node for the document
        # If the document already exists, update its data
        if document_name not in self.nodes:
            self.nodes[document_name] = Node(document_name, data)

    def add_edge(self, from_doc, to_doc, weight=1): # Create a directed edge from one document to another
        if from_doc in self.nodes and to_doc in self.nodes:
            self.nodes[from_doc].add_edge(self.nodes[to_doc], weight)

    def get_node(self, document_name): # Retrieve a node by its document name
        return self.nodes.get(document_name)

    def display_graph(self): # Display the graph in a readable format
        for node in self.nodes.values():
            print(f"{node.document_name} -> {[neighbor.document_name for neighbor in node.get_neighbors()]}")
