
import sys
import networkx as nx
import numpy as np

#Vector x_k: entries corresponding to the pagerank score for each node in the graph at iteration k
def page_rank(G: nx.DiGraph):

    #number of nodes in the graph
    n = G.number_of_nodes()

    #the reverse graph to use
    rev_G: nx.DiGraph = G.reverse()

    #Outgoing edges from node i
    branching = np.array([G.out_degree(i) for i in G.nodes])

    #Nodes with no outgoing edges
    dangling_nodes = np.array([int(node) for node in G.nodes if G.out_degree(node) == 0])

    #Initial probability distribution. The first vector
    x_k = np.full(n, 1/n)

    m = 0.15

    # print("n -------------")
    # print(n)
    # print("g------------")
    # print(G)
    # print("rev_g------------")
    # print(rev_G)
    # print("nodes")
    # print(G.nodes)
    # print("brancing ------------")
    # print(branching)
    # print("dangling_nodes ------------")
    # print(dangling_nodes)
    # print("x_k------------")
    # print(x_k)
    # print("m ------------")
    # print(m)

     #outer loop. Multiply current vector by M until eigenvector is reached
    for k in range(50):

        #sum of the pagerank score for each of the dangling nodes divided by the total number of nodes
        dangling_sum = sum(x_k[j] / n for j in dangling_nodes) #maybe: dangling_sum = sum(x_k[j] for j in dangling_nodes) / n
        
        #new varibale to hold new pagerank calculation
        x_k_1 = np.zeros(n)

        #loop over all nodes
        for i in range(n):
            #using links to i, since A is sparse aka all other entries of A is 0. 
            # #So matrix multiplication is too performance expensive
            links_to_node_i = list(rev_G.successors(str(i))) 

            #what is happening here?
            link_sum = sum(x_k[int(j)] / branching[int(j)] for j in links_to_node_i if branching[int(j)] > 0)

            #update i'th entry in pagerank vector 
            x_k_1[i] = (1 - m) * (link_sum + dangling_sum) + m * (1 / n) #1/n from S matrix

        # Check for convergence
        if np.linalg.norm(x_k_1 - x_k, 1) < 0.0001:
            print("Converged at iteration:", k)
            break
        

        #update pagerank to new pagerank vector
        x_k = x_k_1
       
    print("Pagerank calculated to be:")
    print(x_k)


def main():
    fh=open(sys.argv[1],'rb')
    G: nx.DiGraph=nx.read_adjlist(fh,create_using=nx.DiGraph()) #G the graph
    fh.close()
    page_rank(G)


if __name__ == "__main__":
    main()   
