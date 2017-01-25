# NetRank

import networkx as nx, pandas as pd, matplotlib.pyplot as plt
import colorsys, random, sys
import util as u

if __name__ == "__main__":

    SEASON_INPUT_FILE = pd.read_csv(sys.argv[1])

    G, _ = u.build_season_graph(SEASON_INPUT_FILE, -1, "margin_of_victory")
    nodes_added = 0
    acc           = ["boston_college", "clemson", "duke", "florida-state", \
                     "georgia-tech", "louisville", "miami-fl", "notre-dame", \
                     "pittsburgh", "wake-forest", "virginia-tech", "syracuse", \
                     "maryland"]
    for i, node in enumerate(G.nodes()):
        if node not in acc:
            G.remove_node(node)

    # pos = nx.graphviz_layout(G, prog = "dot")
    pos = nx.circular_layout(G)

    nx.draw( \
                     G, \
                     # arrows             = False, \
                     node_size          = 4000, \
                     # alpha              = 0.75, \
                     width              = 1, \
                     node_color         = "#7890cd", \
                     edge_color         = "gray", \
                     with_labels        = True, \
                     font_color         = "white", \
                     pos                = pos)

    edge_labels = dict([((u,v,),d['weight']) for u,v,d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels)

    plt.draw()
    plt.show()
