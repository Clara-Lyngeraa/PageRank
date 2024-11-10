
import random
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

    #number of iterations needed for stabilisation
    stabilise = 0

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
            #print("Converged at iteration:", k)
            break
        
        #increase the number of iterations by 1
        stabilise += 1
        #update pagerank to new pagerank vector
        x_k = x_k_1

    #creating a dictionary of nodes and their final ranking
    rankings_dict = {node: x_k[i] for i, node in enumerate(G.nodes())}

    # Sort the dictionary by PageRank in descending order and take the top 10
    sorted_rankings = sorted(rankings_dict.items(), key=lambda item: item[1], reverse=True)

    top_10_rankings = sorted_rankings[:10]

    return top_10_rankings, stabilise

def random_surfer(G: nx.DiGraph):
    m = 0.15

    #number of nodes in the graph
    n = G.number_of_nodes()

    #Dict mapping each node with the number of times it is visited
    visited_dict = {i: 0 for i in G.nodes()}

    #random selected node to start
    current_node = random.choice(list(G.nodes))

    for i in range(50):
        #increase number of visits to current node in dictionary
        visited_dict[current_node] += 1

        #random number
        r = random.random()

        #with probability m move to another random node
        if r < m:
            current_node = random.choice(list(G.nodes))

        # with probability (1 − m) follow a random edge from the current node to another node.
        else: 
            neighbors_to_current_node = list(G.successors(current_node))

            #check if the node has any successors, otherwise it is dangling
            if neighbors_to_current_node:

                #select random neighboring node
                current_node = random.choice(neighbors_to_current_node)

            #in these cases the random surfer should always choose a random node.  
            else:
                current_node = random.choice(list(G.nodes))

    # Sort nodes by the number of visits in descending order
    sorted_visits = sorted(visited_dict.items(), key=lambda item: item[1], reverse=True)
    top_10_visited_nodes = sorted_visits[:10]

    return top_10_visited_nodes
   
def main():
    fh=open(sys.argv[1],'rb')
    G: nx.DiGraph=nx.read_adjlist(fh,create_using=nx.DiGraph()) #G the graph
    fh.close()
    highest_rankings, stabilise = page_rank(G)
    most_visited = random_surfer(G)

      # Write the top 10 nodes to a file
    with open("results.txt", "w") as f:
        f.write("Pagerank:\n")
        f.write("Top 10 highest ranking nodes:\n")
        for node, ranking in highest_rankings:
            f.write(f"Node {node}: {ranking}\n")
        f.write("\n")
        f.write(f"Number of iterations needed in pagerank: {stabilise}\n")

        f.write("\n")
        f.write("Random_surfer:\n")
        f.write("Top 10 most visited nodes:\n")
        for node, count in most_visited:
            f.write(f"Node {node}: {count} visits\n")
        

if __name__ == "__main__":
    main()   
