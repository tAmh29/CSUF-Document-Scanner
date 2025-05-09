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
# import networkx as nx
# import matplotlib.pyplot as plt

# map_data = {
#     "A": ["B", "C"],
#     "B": ["D"],
#     "C": ["D", "E"],
#     "D": [],
#     "E": []
# }

# G = nx.DiGraph()  # use nx.Graph() for undirected

# # Add edges
# for node, neighbors in map_data.items():
#     for neighbor in neighbors:
#         G.add_edge(node, neighbor)

# # Draw the graph
# pos = nx.spring_layout(G)
# nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=14)
# plt.show()


# from main_gui import draw_from_log

# if __name__ == "__main__":
#     print("Hello from r_graph_visualizer.")
#     loc = "logOutput/log_5_9_4_21.12.txt"
#     draw_from_log(loc)

import networkx as nx
import matplotlib.pyplot as plt
from log_handler import PlagiarismLog
## USE ME
def graphLog(plag_log):

    try:
        plt.clf()
        plt.cla()
        plt.close()
    except:
        print("plt clf,cla,close error")

    SETTINGS = {} ## settings go here
    Graph = nx.DiGraph()
    ## loading data into new structure
    for section, data in plag_log.sections.items(): ## section is always gonna be first part of connection.
        #print("Key:",key,"\nValue:",value)
        for edge in data: ## each dict in the list of dicts.
            u_node = plag_log.nickname_map[section]
            v_node = str(edge["ref_label"]).replace(edge["target_letter"],plag_log.nickname_map[edge["target_letter"]])
            weight = "<"+str(edge["ref_start"])+"-"+str(edge["ref_end"])+">"
            Graph.add_edge(u_node,v_node,weight=weight)
    ## drawing graph
    pos = nx.random_layout(Graph)
    nx.draw(Graph,pos,with_labels=True, node_color = 'red', node_size = 2000, font_size =12, arrows=True)
    edge_labels = nx.get_edge_attributes(Graph,"weight")
    nx.draw_networkx_edge_labels(Graph,pos,edge_labels=edge_labels, font_color="black")

    plt.title("Reference Graph model")
    plt.show()

if __name__ == "__main__":
    dummy = PlagiarismLog()
    dummy = dummy.parse_log("logOutput\log_5_9_4_21.12.txt")
    graphLog(dummy)