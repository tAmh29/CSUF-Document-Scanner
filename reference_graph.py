from node import Node

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
from log_handler import PlagiarismLog

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
    
    ## Basically networkx has it's own graph datastructure
    ## we turn the ReferenceGraph object into a nx.Graph object and it will plot itself.
    def visualize_graph(self, **options): 
        netx_graph = nx.DiGraph()
        netx_graph.add_nodes_from(self.nodes)
        print(list(netx_graph.nodes))
        
        for node in self.nodes.values(): # for each node in the graph
            for neighbor_node in node.get_neighbors(): ## iterate thru list of neighbors ## we have a list of keys now.
                #print("neighbor:",neighbor)
                #print("self.nodes:",self.nodes)
                #neighbor_node = self.nodes[neighbor]
                #new_edge = tuple(node.document_name,neighbor_node.document_name,{'weight': node.edges[neighbor_node]}) ### of form, start end, weight (2, 3, {'weight': 3.1415})
                #print(node.edges[neighbor_node])
                netx_graph.add_edge(node.document_name,neighbor_node.document_name,weight=node.edges[neighbor_node])
                print("found valid edge")
        
        print(netx_graph)
        pos = nx.random_layout(netx_graph)
        nx.draw(netx_graph,pos,None,**options) ##tookout with_labels=True since it's true by default
        plt.show()
        
        
        
def build_reference_graph_from_log(log_path):
    log = PlagiarismLog()
    parsed = log.parse_log(log_path)

    graph = ReferenceGraph()

    print("\nBuilding Reference Graph from Log...\n")

    # Add main document nodes (A, B, etc.)
    for letter, filename in parsed.nickname_map.items():
        graph.add_node(letter, data={"filename": filename})
        print(f"Added doc node: {letter} ({filename})")

    # Add edges and reference nodes
    for src_letter, entries in parsed.sections.items():
        for entry in entries:
            if entry.get("not_found"):
                print(f"Skipping {entry.get('ref_label', '?')} (not found)")
                continue

            ref_label = entry["ref_label"]        # e.g., B.1
            target_letter = entry["target_letter"]  # e.g., B
            ref_start = entry["ref_start"]
            ref_end = entry["ref_end"]

            # Add the reference node if not already added
            graph.add_node(ref_label, data={
                "target": target_letter,
                "start": ref_start,
                "end": ref_end
            })
            print(f"Added ref node: {ref_label} ({target_letter}[{ref_start}-{ref_end}])")

            # Create edge from source document to the reference node
            graph.add_edge(src_letter, ref_label)
            print(f"Edge: {src_letter} → {ref_label}")

    print("\nReference graph build complete.\n")
    return graph
