import networkx as nx
import random

G = nx.read_edgelist("entrada.txt", create_using=nx.DiGraph)

while G.number_of_nodes() != 0:
    size = G.number_of_nodes() - 1
    g_nodes = list(G.nodes)
    v_atual = g_nodes[random.randint(0, size)]
    rp = set()
    rm = set()
    rp.add(v_atual)
    rm.add(v_atual)

    w = set(G.successors(v_atual))
    w -= rp

    while len(w) != 0:
        successors = []
        rp = rp.union(w)
        for n in rp:
            successors.extend(G.successors(n))
        w = set(successors) - rp

    w = set(G.predecessors(v_atual))
    w -= rm

    while len(w) != 0:
        predecessors = []
        rm = rm.union(w)
        for n in rm:
            predecessors.extend(G.predecessors(n))
        w = set(predecessors) - rm
    
    cnd = rp.intersection(rm)
    print(cnd)
    
    for n in cnd:
        if G.has_node(n):
            G.remove_node(n)