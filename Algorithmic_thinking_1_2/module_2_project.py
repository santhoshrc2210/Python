
"""

#part-1:3  dictionaries corresponding to the 3 directed graphs shown in diagrams

"""

EX_GRAPH0 = dict()
#tail at node 0 and head at the nodes given in list
EX_GRAPH0[0] = set([1, 2])
EX_GRAPH0[1] = set([])
EX_GRAPH0[2] = set([])

#print(EX_GRAPH0)

EX_GRAPH1 = dict()
EX_GRAPH1[0] = set([1, 4, 5])
EX_GRAPH1[1] = set([2, 6])
EX_GRAPH1[2] = set([3])
EX_GRAPH1[3] = set([0])
EX_GRAPH1[4] = set([1])
EX_GRAPH1[5] = set([2])
EX_GRAPH1[6] = set([])

#print(EX_GRAPH1)



EX_GRAPH2 = dict()
EX_GRAPH2[0] = set([1, 4, 5])
EX_GRAPH2[1] = set([2, 6])
EX_GRAPH2[2] = set([3, 7])
EX_GRAPH2[3] = set([7])
EX_GRAPH2[4] = set([1])
EX_GRAPH2[5] = set([2])
EX_GRAPH2[6] = set([])
EX_GRAPH2[7] = set([3])
EX_GRAPH2[8] = set([1, 2])
EX_GRAPH2[9] = set([0, 3, 4, 5, 6, 7])

#print(EX_GRAPH2)


#########part-2:

def make_complete_graph(num_nodes):

    """
    #function to make a complete directed graph with input as number of nodes
    """
    complete_graph = dict()
    if num_nodes > 0:
        nth_node = 0
        while nth_node < num_nodes:
            complete_graph[nth_node] = set()
            pth_node = 0
            while pth_node < num_nodes:
                if pth_node != nth_node:
                    complete_graph[nth_node].add(pth_node)	
                pth_node += 1
            nth_node += 1
    return complete_graph
    

#print(make_complete_graph(4))



#########part-3:


def compute_in_degrees(digraph):
    """
   #function that takes directed graph (dictionary) and computes in-degree for each node 
    """

    in_degrees = {}
    for node in digraph:
        in_degrees[node]  = 0
        
    for node in digraph:
        for node_in in digraph[node]:
            in_degrees[node_in] +=1

    return in_degrees

print(compute_in_degrees(EX_GRAPH2))

#exit()
#########part-4:

def in_degree_distribution(digraph):
    """
    #function takes directed graph (dictionary) as input and computes distribution of in-degrees   
    """
    in_degrees_dist = dict()
  
    #part-1:use compute_in_degrees values max for keys of the dictionary
    in_degrees = compute_in_degrees(digraph)
    in_degrees_list = list()
    in_degrees_uniq = set()
    for node in in_degrees:
         in_degrees_uniq.add(in_degrees[node])
         in_degrees_list.append(in_degrees[node])

    for num_in_degree in in_degrees_uniq:
        in_degrees_dist[num_in_degree] = in_degrees_list.count(num_in_degree)


    return in_degrees_dist 
    



print(in_degree_distribution(EX_GRAPH2))
