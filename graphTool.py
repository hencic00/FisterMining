import networkx as nx # full docs: https://networkx.github.io/documentation/stable/tutorial.html
#
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_node(1) # adds one node at a time
G.add_nodes_from([2, 3]) # adds list of nodes

G = nx.petersen_graph()
plt.subplot(121)

nx.draw(G, with_labels=True, font_weight='bold')
plt.subplot(122)

nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')

plt.show()