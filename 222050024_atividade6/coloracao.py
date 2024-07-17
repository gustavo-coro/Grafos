import networkx as nx
from random import choice

def chromatic_partition (G: nx.Graph) -> list:
    i_set = []
    while G.number_of_nodes():
        node = choice(list(G.nodes()))
        i_set.append(node)
        for n in list(G.neighbors(node)):
            G.remove_node(n)
        G.remove_node(node)
    return i_set

G = nx.read_gml("Tabuleiro_com_incompatibilidades.gml")
color = 0 # each number represents a color
while G.number_of_nodes():
    H = G.copy()
    result = chromatic_partition(H)
    print('Color ', color)
    print(result)
    for v in result:
        G.remove_node(v)
    print('---------')
    color += 1