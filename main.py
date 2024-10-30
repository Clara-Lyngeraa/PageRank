import networkx as nx
import numpy as np

def page_rank(graph):
    n = len(graph)
    branching = [graph.out_degree(i) for i in graph.nodes()] #Outgoing edges from node i
    x_0 = [1/n for i in range(n)] #Initial probability distribution // initial guess for ?? Take and multiplyby n
    S = [1/n for i in range(n)]
    # D outgoing nodes from i less than 1
    m = 0.15
    print(f"Initial guess: {x_0}")
    for k in range(50): #outer loop
        # x_k+1 = m * S * x_k
        # Dangling = sum(1/n_j * x_k_j)
        for i in range(n):
            #(x_k+1)_i += dangling
            # (x_k+1)_i += (1-m) * sum(1/n_j * x_k_j)
            # x_k = x_k+1
            return i

def random_surfer(graph):
    m = 0.15
    return 0