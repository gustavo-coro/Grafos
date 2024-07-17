import networkx as nx


def valid_path_flow(edge_paths, graph_weight):
    aux = True
    for x in edge_paths:
        for y in x:
            if graph_weight[(y)] == 0:
                aux = False
                break
        if (aux == False):
            aux = True
        else:
            return x
    return list()


def start_slack_graph(G):
    F = G.copy()
    edges = G.reverse().edges()
    edges_with_weights = [(a, b, 0.0) for (a, b) in edges]
    F.add_weighted_edges_from(edges_with_weights)
    return F


def ford_fulkerson_max_flow(F, s, t):
    while True:
        path = list(nx.all_simple_edge_paths(F, s, t))
        valid_path = valid_path_flow(path, nx.get_edge_attributes(F, "weight"))
        if not valid_path:
            break

        min_weight = min(F[u][v]["weight"] for u, v in valid_path)
        for u, v in valid_path:
            F[u][v]["weight"] -= min_weight
            F[v][u]["weight"] += min_weight

    cap_corte = sum(F[u][s]["weight"] for u in F.successors(s))
    return cap_corte


G = nx.read_weighted_edgelist("entrada.txt", create_using=nx.DiGraph)
F = start_slack_graph(G)

s = next(node for node in G.nodes() if G.in_degree(node) == 0)
t = next(node for node in G.nodes() if G.out_degree(node) == 0)

# Usando o metodo implementado por mim
min_cut_value = ford_fulkerson_max_flow(F, s, t)
print("Capacidade do Corte (meu algoritmo) = ",
      ford_fulkerson_max_flow(F, s, t))

# Usando o metodo da networkx
min_cut_value = nx.minimum_cut_value(G, s, t, capacity="weight")
print("Capacidade do Corte (networkx) = ", min_cut_value)