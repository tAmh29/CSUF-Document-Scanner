from node import Node

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl


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