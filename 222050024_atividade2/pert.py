import networkx as nx

G = nx.read_weighted_edgelist("entrada.txt", create_using=nx.DiGraph, nodetype=int)

node_list = list(nx.topological_sort(G))

t = {}
for i in node_list:
    max_weight = 0
    for j in G.predecessors(i):
        max_weight = max(max_weight, t[j] + G[j][i]['weight'])
    t[i] = max_weight

f = {}
crit = []
tl = dict.fromkeys(G.nodes(), t[max(t, key=t.get)])
for i in reversed(node_list):
    min_weight = tl[i]
    for j in G.successors(i):
        min_weight = min(min_weight, tl[j] - G[i][j]['weight'])
    tl[i] = min_weight
    f[i] = tl[i] - t[i]
    if f[i] == 0:
        crit.append(i)

print("Tempos mais cedo:", t)
print("Tempos mais tarde:", tl)
print("Folgas:", f)
print("Caminho critico:", crit)