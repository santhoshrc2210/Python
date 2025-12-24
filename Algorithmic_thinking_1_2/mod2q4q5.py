"""
Provided code for application portion of module 1

Helper class for implementing efficient version
of DPA algorithm
"""

# general imports
import random


class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm
    
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors
    
##Q4:
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

#Your task for this question is to implement the DPA algorithm,

    
def dpa_alg(num_nodes, num_edges):
    dir_graph = make_complete_graph(num_edges)
    dpa = DPATrial(num_edges)
    for node in range(num_edges, num_nodes):        
        rand_nodes = dpa.run_trial(num_edges)
        dir_graph[node] = set(rand_nodes)        
    return dir_graph
            
                   
#compute a DPA graph using the values from Question 3,

dpa_graph = dpa_alg(27770,13)


#exit()
# compute a (normalized) log/log plot of the points in the 
#graph's in-degree distribution

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

in_degree_dpa_graph = in_degree_distribution(dpa_graph)
####
total_in_degrees = 0.0
for node in in_degree_dpa_graph:
    total_in_degrees += in_degree_dpa_graph[node]


in_degree_dist_normal = {}
for node in in_degree_dpa_graph:
    in_degree_dist_normal[node] = in_degree_dpa_graph[node]/total_in_degrees

#####################################
import simpleplot
import math

dataset_in_degree_dist_normal_loglog = {}
#print math.log(100)

for key in in_degree_dist_normal:
    #print "key:", key
    if key != 0:
        dataset_in_degree_dist_normal_loglog[math.log(key)] = math.log(in_degree_dist_normal[key])
    
#print  dataset_in_degree_dist_normal_loglog 
simpleplot.plot_lines('log/log plot of in_degree distribution DPA graph', 600, 600, 'in_degree', 'number of nodes (normalized)', [dataset_in_degree_dist_normal_loglog], True, ['Normalized in-degree distribution of citation'])


#######Q5:
















