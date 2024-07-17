import networkx as nx
from random import choice

def independent_set (G: nx.Graph) -> list:
    i_set = []
    while G.number_of_nodes():
        node = choice(list(G.nodes()))
        i_set.append(node)
        for n in list(G.neighbors(node)):
            G.remove_node(n)
        G.remove_node(node)
    return i_set

G = nx.read_gml("Tabuleiro_com_incompatibilidades.gml")
while True:
    H = G.copy()
    result = independent_set(H)
    if (len(result) == 8):
        break

for v in result:
    print(v)