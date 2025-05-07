# import networkx as nx
# import matplotlib.pyplot as plt

# print("start")

# #G = nx.Graph()
# #G.add_nodes_from(range(0,10))G = nx.petersen_graph()
# G = nx.petersen_graph()
# subax1 = plt.subplot(121)
# nx.draw(G, with_labels=True, font_weight='bold')
# subax2 = plt.subplot(122)
# nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
# plt.show()
import networkx as nx
import matplotlib.pyplot as plt

map_data = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["D", "E"],
    "D": [],
    "E": []
}

G = nx.DiGraph()  # use nx.Graph() for undirected

# Add edges
for node, neighbors in map_data.items():
    for neighbor in neighbors:
        G.add_edge(node, neighbor)

# Draw the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=14)
plt.show()
