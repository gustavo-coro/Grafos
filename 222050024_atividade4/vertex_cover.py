import networkx as nx
import random

def vertex_cover_approximation(G):
    C = set()
    E = [edge for edge in G.edges()]
    while E:
        (u, v) = random.choice(E)
        C.add(u)
        C.add(v)
        for edge in E:
            (u_line, v_line) = edge
            if ((u_line in C) or (v_line in C)):
                E.remove(edge)
    return C

def vertex_cover_greedy(Graph):
    G = Graph.copy()
    C = set()
    while G.edges():
        mdv = max(G.nodes(), key= lambda node: G.degree(node))
        C.add(mdv)
        G.remove_edges_from(list(G.edges(mdv)))
    return C

def write_result(G, C, File):
    File.write("Esquinas com Câmera: ")
    File.write(str(len(C)))
    File.write("\n\n")
    for node in C:
        File.write("Esquina de label: ")
        File.write(node)
        File.write("\nRuas cobertas pela câmera: \n")
        streets = set()
        for u, v in G.edges(node):
            name = G.get_edge_data(u,v)
            name = name["name"]
            if type(name) == list:
                for n in name:
                    streets.add(n)
                break
            streets.add(name)
        for name in streets:
            File.write(name)
            File.write("\n")
        File.write("\n")

G = nx.read_gml("222050024_atividade4/sjdr.gml")
VCA = open("vca.txt", "w")
VCG = open("vcg.txt", "w")

C = vertex_cover_approximation(G)
VCA.write("Algoritimo de aproximação\n")
write_result(G, C, VCA)

C = vertex_cover_greedy(G)
VCG.write("Algoritimo guloso\n")
write_result(G, C, VCG)

VCA.close()
VCG.close()