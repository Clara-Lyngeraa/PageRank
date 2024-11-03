import sys
import networkx as nx
import numpy as np

#Vector x_k: entries corresponding to the pagerank score for each node in the graph at iteration k
def page_rank(G):
    n = G.number_of_nodes()
    rev_G = G.reverse()
    branching = [G.out_degree(i) for i in G.nodes] #Outgoing edges from node i
    dangling_nodes = [node for node in G.nodes if G.out_degree(node) == 0] #List of nodes with no outgoing edges
    x_0 = [1/n for i in range(n)] #Initial probability distribution // initial guess for ?? Take and multiplyby n
    m = 0.15
    S = np.full((n, n), 1/n)
    print(n)
    print("-------------")
    print(rev_G)
    print("-------------")
    print(branching)
    print("-------------")
    print(dangling_nodes)
    print("-------------")
    print(x_0)
    print("-------------")
    print(m)

    x_k = x_0
    Sx_k = np.dot(S, x_k)  #should be 1/n in all entries of the column vector S using the lemma that all entries in x_k sums to 1.
    print("Sx_k")
    print(Sx_k)
    for k in range(50): #outer loop. Multiply current vector by M until eigenvector is reached
        dangling_sum = sum(x_k[j] / n for j in dangling_nodes) #sum of the pagerank score for each of the dangling nodes divided by the total number of nodes
        for i in range(n): #loop over all nodes
            # Initialize an array to hold the contribution from A
            A_x_k = np.zeros(n)
            #loop over reversedgraph:
            backlinks_to_node_i = list(rev_G.predecessors(i))
            for link in backlinks_to_node_i:
                out_degree_link = G.outdegree(link)
                if out_degree_link > 0:  # Avoid division by zero
                    A_x_k[i] += x_k[link] / out_degree_link

            x_k_one = (1-m)*A_x_k+(1-m)*dangling_sum+m*Sx_k
            x_k = x_k_one

def random_surfer(graph):
    m = 0.15
    return 0
    

def main():
    fh=open(sys.argv[1],'rb')
    G: nx.DiGraph=nx.read_adjlist(fh,create_using=nx.DiGraph()) #G the graph
    fh.close()

    setup(G)


if __name__ == "__main__":
    main()   

        



    

    

