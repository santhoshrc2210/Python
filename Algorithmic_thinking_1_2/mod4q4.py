##########################################################################

"""

project-2

"""
import random

class Queue:
    """
    A simple implementation of a FIFO queue.
    """

    def __init__(self):
        """ 
        Initialize the queue.
        """
        self._items = []

    def __len__(self):
        """
        Return the number of items in the queue.
        """
        return len(self._items)
    
    def __iter__(self):
        """
        Create an iterator for the queue.
        """
        for item in self._items:
            yield item

    def __str__(self):
        """
        Return a string representation of the queue.
        """
        return str(self._items)

    def enqueue(self, item):
        """
        Add item to the queue.
        """        
        self._items.append(item)

    def dequeue(self):
        """
        Remove and return the least recently inserted item.
        """
        return self._items.pop(0)

    def clear(self):
        """
        Remove all items from the queue.
        """
        self._items = []
        


def bfs_visited(ugraph, start_node):
    """
    Takes the undirected graph ugraph and the node start_node and returns the 
    set consisting of all nodes that are visited by a breadth-first search that
    starts at start_node.
    """
    #queue
    q_bfs = Queue()    
    #visited is set of all nodes visited by the algorithm
    visited = set()
    
    visited.add(start_node)
    q_bfs.enqueue(start_node)
    
    while len(q_bfs) != 0:
        node_neighb = q_bfs.dequeue()
        for neighb in ugraph[node_neighb]:
            if neighb not in visited:
                visited.add(neighb)
                q_bfs.enqueue(neighb)
                
    return visited




def cc_visited(ugraph):
    """
    Takes the undirected graph ugraph and returns a list of sets, where each 
    set consists of all the nodes (and nothing else) in a connected component, 
    and there is exactly one set in the list for each connected component in 
    ugraph and nothing else
    """
    cc_visited_list = list()
    remaining_nodes = list(ugraph.keys())
    #print (remaining_nodes)
    cc_node = set()
    
    while remaining_nodes:
        
        if (len(remaining_nodes)) > 1:
            node_index = random.randint(0, (len(remaining_nodes)-1)) 
        else:
            node_index = 0
            
        node = remaining_nodes[node_index]
        cc_node = bfs_visited(ugraph, node)
        cc_visited_list.append(cc_node)
        remaining_nodes.remove(node)
        
    #remove dupplicate cc
    cc_visited_list_new = list()
    for con_comp in cc_visited_list:
        lst_cc = list(con_comp)
        lst_cc.sort(reverse=True)
        cc_visited_list_new.append(lst_cc)
    
    cc_visited_list_2 = list()
    for con_comp  in cc_visited_list_new:
        if con_comp not in cc_visited_list_2:
            cc_visited_list_2.append(con_comp)
    
    cc_visited_list_3 = list()
    for con_comp in cc_visited_list_2:
        cc_new = set(con_comp)
        cc_visited_list_3.append(cc_new)
        
                                            
    return cc_visited_list_3
  
    

def largest_cc_size(ugraph):
    """
    Takes the undirected graph ugraph and returns the size (an integer) of the 
    largest connected component in ugraph
    """
    visited_cc = cc_visited(ugraph)
    largest_len = 0
    for index in range(len(visited_cc)):        
        len_index = len(visited_cc[index])
        if len_index >= largest_len:
            largest_len = len_index            
            
    return largest_len
        
        
    

def compute_resilience(ugraph, attack_order):
    """
     Takes the undirected graph ugraph, a list of nodes attack_order and 
    iterates through the nodes in attack_order. For each node in the list, the 
    function removes the given node and its edges from the graph and then 
    computes the size of the largest connected component for the resulting 
    graph. The function should return a list whose k+1th entry is the size of 
    the largest connected component in the graph after the removal of the first 
    k nodes in attack_order. The first entry (indexed by zero) is the size of 
    the largest connected component in the original graph.
    
    """
    largest_cc_list = list()
    largest_cc_orig = largest_cc_size(ugraph)
    largest_cc_list.insert(0, largest_cc_orig)
    count = 0
    for node_rem in attack_order:
        ugraph.pop(node_rem)       
        for node in ugraph:
            #if node_rem in ugraph[node]:
            ugraph[node].discard(node_rem)
        largest_cc_list.append(largest_cc_size(ugraph))
        count += 1
        print "added", count
    
        
    
    return largest_cc_list
                
                
#######################################################################


"""
Provided code for Application portion of Module 2
"""

# general imports
import urllib2
import random
import time
import math

# CodeSkulptor import
#import simpleplot
#import codeskulptor
#codeskulptor.set_timeout(60)

# Desktop imports
#import matplotlib.pyplot as plt


############################################
# Provided code

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order
    


##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph


"""
Provided code for application portion of module 2

Helper class for implementing efficient version
of UPA algorithm
"""


class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm
    
    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that each node number
        appears in correct ratio
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors


def make_er_graph(num_nodes, probability_edge):

    """
    function to make a random undirected graph with input as number of nodes
    """
    #probability_edge = 0.3
    
    #initialize graph
    er_graph = dict()
    if num_nodes > 0:
        nth_node = 0
        while nth_node < num_nodes:
            er_graph[nth_node] = set()
            nth_node += 1
    
    nth_node = 0        
    while nth_node < num_nodes:
        pth_node = 0
        while pth_node < num_nodes:
            rand_num = random.random()
            if rand_num < probability_edge and pth_node != nth_node:
                er_graph[nth_node].add(pth_node)
                er_graph[pth_node].add(nth_node)
            pth_node += 1
        nth_node += 1    
                                                                                                                                           
    return er_graph

#print  make_er_graph(6, 0.2)

def make_complete_graph(num_nodes):
    """
    function to make a complete undirected graph with input as number of nodes
    """
    complete_undir_graph = dict()
    #initialize graph
    if num_nodes > 0:
        nth_node = 0
        while nth_node < num_nodes:
            complete_undir_graph[nth_node] = set()
            nth_node += 1
    
    nth_node = 0        
    while nth_node < num_nodes:
        pth_node = 0
        while pth_node < num_nodes:
            if pth_node != nth_node:
                complete_undir_graph[nth_node].add(pth_node)
                complete_undir_graph[pth_node].add(nth_node)
            pth_node += 1
        nth_node += 1
                
    return complete_undir_graph
 
#print make_complete_graph(3)    
    
#you will modify this code to generate undirected UPA graphs    
def upa_alg(num_nodes, num_edges):
    upa_graph = make_complete_graph(num_edges)
    upa = UPATrial(num_edges)
    for node in range(num_edges, num_nodes):        
        rand_nodes = upa.run_trial(num_edges)
        upa_graph[node] = rand_nodes        
        for node_neigh in rand_nodes:            
            upa_graph[node_neigh].add(node)

    return upa_graph

#print  upa_alg(5, 3)       



###########################################
#function to calculate number of edges in undirected graph
def find_num_edges(inp_graph):
    num_edges = 0
    for node in inp_graph:
        num_edges += len(inp_graph[node])
    
    return num_edges/4   

#print make_complete_graph(4)
#print find_num_edges(make_complete_graph(4))
#print "num_edges:", find_num_edges(load_graph(NETWORK_URL))

#To begin, you should determine the probability 
#p such that the ER graph computed using this edge probability has 
#approximately the same number of edges as the computer network. 

#for num in range(0, 10):    
#    print num/1000.0, find_num_edges(make_er_graph(1239, num/1000.0))

#ans: p = 0.004    


#Likewise, you should compute an integer 
#m such that the number of edges in the UPA graph is close to the number 
#of edges in the computer network. 
#for num in range(1, 10):
#    print num ,find_num_edges(upa_alg(1239, num))
    
#ans: m=2
#exit ()
####################################################
    


#load three graphs
compnw_graph = load_graph(NETWORK_URL)
er_graph = make_er_graph(1239, 0.004)
upa_graph = upa_alg(1239, 2)

#for each of the three graphs (computer network, ER, UPA), compute a random attack order

compnw_rand_att_ord = targeted_order(compnw_graph)
er_rand_att_ord = targeted_order(er_graph)
upa_rand_att_ord = targeted_order(upa_graph) 
#use this attack order in compute_resilience compute the resilience of the graph.
#compnw_cc_list = compute_resilience(compnw_graph, compnw_rand_att_ord)
#print compnw_cc_list
#er_cc_list = compute_resilience(er_graph, er_rand_att_ord) 
#print er_cc_list
#upa_cc_list = compute_resilience(upa_graph, upa_rand_att_ord)
#print upa_cc_list

#plot the graphs        
import simpleplot

dataset_compnw = {}
dataset_er = {}
dataset_upa = {}

#computed and saved
compnw_cc_list = [1239, 1158, 1150, 1148, 1142, 1136, 1129, 1127, 1124, 1120, 1119, 1110, 1109, 1101, 1100, 1098, 1097, 1066, 1065, 1064, 1055, 1050, 1049, 1047, 1037, 1035, 1034, 1028, 1025, 1018, 1017, 1012, 1008, 1007, 998, 990, 989, 985, 962, 938, 937, 933, 929, 928, 926, 879, 876, 860, 817, 810, 783, 781, 759, 752, 751, 672, 652, 499, 481, 478, 463, 463, 461, 457, 457, 410, 405, 373, 370, 370, 348, 348, 311, 311, 308, 295, 283, 281, 281, 279, 216, 214, 211, 211, 210, 210, 172, 172, 172, 172, 169, 169, 169, 159, 159, 159, 159, 159, 159, 159, 159, 156, 129, 127, 127, 104, 102, 86, 86, 86, 86, 86, 86, 86, 80, 80, 80, 75, 75, 75, 75, 75, 74, 74, 74, 74, 74, 74, 71, 71, 71, 71, 71, 64, 64, 64, 64, 64, 64, 64, 64, 58, 58, 40, 40, 40, 40, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 32, 32, 32, 32, 32, 32, 31, 31, 31, 31, 31, 27, 20, 17, 17, 17, 17, 17, 17, 17, 17, 15, 15, 15, 12, 12, 12, 12, 12, 12, 12, 12, 8, 8, 8, 8, 8, 8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]

er_cc_list = [1239, 1238, 1237, 1236, 1235, 1234, 1233, 1232, 1231, 1230, 1229, 1228, 1227, 1226, 1225, 1224, 1223, 1222, 1221, 1220, 1219, 1218, 1217, 1216, 1215, 1214, 1213, 1212, 1211, 1210, 1209, 1208, 1207, 1206, 1205, 1204, 1203, 1202, 1201, 1200, 1199, 1198, 1197, 1196, 1195, 1194, 1193, 1192, 1191, 1190, 1189, 1188, 1187, 1186, 1185, 1184, 1183, 1182, 1181, 1180, 1179, 1178, 1177, 1176, 1175, 1174, 1173, 1172, 1171, 1170, 1169, 1168, 1167, 1166, 1165, 1164, 1163, 1162, 1161, 1160, 1159, 1158, 1157, 1156, 1155, 1154, 1153, 1152, 1151, 1150, 1149, 1148, 1147, 1146, 1145, 1144, 1143, 1142, 1141, 1140, 1139, 1138, 1137, 1136, 1135, 1134, 1133, 1132, 1131, 1130, 1129, 1128, 1127, 1126, 1125, 1124, 1123, 1122, 1121, 1120, 1119, 1118, 1117, 1116, 1115, 1114, 1113, 1112, 1111, 1110, 1109, 1108, 1107, 1106, 1105, 1104, 1103, 1102, 1101, 1100, 1099, 1098, 1097, 1096, 1095, 1094, 1093, 1092, 1091, 1090, 1089, 1088, 1087, 1086, 1085, 1084, 1083, 1082, 1081, 1080, 1079, 1078, 1077, 1076, 1075, 1074, 1073, 1072, 1071, 1070, 1069, 1068, 1067, 1066, 1065, 1064, 1063, 1062, 1061, 1060, 1059, 1058, 1057, 1056, 1055, 1054, 1053, 1052, 1051, 1050, 1049, 1048, 1047, 1046, 1045, 1044, 1043, 1042, 1041, 1040, 1039, 1038, 1037, 1036, 1035, 1034, 1033, 1032, 1031, 1030, 1029, 1028, 1027, 1026, 1025, 1024, 1023, 1022, 1021, 1020, 1019, 1018, 1017, 1016, 1015, 1014, 1013, 1012, 1011, 1010, 1009, 1008, 1007, 1006, 1005, 1004, 1003, 1002, 1001, 1000, 998, 997, 996, 995, 994, 993, 992, 991, 990, 989, 988, 987, 986, 985, 984, 983, 982, 981, 980, 979, 978, 977, 976, 975, 974, 973, 972, 971, 970, 969, 968, 967, 966, 965, 964, 963, 962, 961, 960, 959, 958, 957, 956, 955, 954, 953, 952, 951, 950, 948, 947, 946, 945, 944, 943, 942, 941, 940, 939, 938, 937, 936, 935, 934, 933, 932, 931, 930, 929, 928, 927, 926, 925, 924, 923, 922, 921, 920, 919, 918, 917, 916, 915, 914, 913, 912, 911, 910, 909, 908, 907, 906, 905, 904, 903, 902, 901, 900, 899, 897, 896, 895, 894, 893, 892, 891, 890, 889, 888, 887, 886, 885, 884, 883, 882, 881, 880, 878, 877, 876, 875, 874, 873, 872, 871, 870, 869, 868, 867, 866, 865, 864, 863, 862, 861, 860, 859, 858, 857, 855, 854, 853, 852, 851, 850, 849, 848, 847, 846, 845, 844, 843, 842, 841, 840, 839, 838, 836, 835, 834, 833, 832, 831, 830, 829, 828, 827, 826, 825, 823, 822, 821, 820, 819, 818, 817, 816, 815, 814, 813, 812, 811, 810, 809, 807, 806, 805, 804, 803, 802, 801, 800, 799, 798, 797, 796, 795, 793, 792, 791, 790, 789, 786, 785, 784, 780, 779, 778, 777, 776, 774, 773, 772, 771, 770, 769, 768, 767, 765, 764, 763, 762, 761, 760, 759, 758, 756, 755, 754, 753, 752, 751, 749, 747, 746, 745, 744, 743, 742, 741, 740, 739, 738, 737, 735, 733, 732, 731, 730, 729, 728, 727, 726, 724, 723, 722, 721, 720, 719, 718, 717, 716, 714, 712, 711, 710, 709, 708, 707, 706, 705, 703, 702, 701, 699, 697, 696, 695, 694, 693, 692, 691, 690, 689, 688, 685, 684, 682, 681, 679, 678, 676, 675, 674, 673, 672, 671, 670, 668, 667, 666, 661, 659, 658, 657, 656, 655, 654, 652, 651, 650, 649, 643, 641, 640, 639, 638, 637, 636, 632, 631, 629, 628, 624, 623, 622, 619, 618, 617, 616, 615, 614, 612, 611, 610, 609, 608, 607, 606, 604, 603, 602, 598, 597, 596, 594, 593, 591, 590, 588, 585, 584, 581, 577, 575, 573, 572, 570, 565, 564, 552, 551, 547, 546, 544, 535, 534, 530, 526, 525, 523, 508, 506, 504, 500, 494, 493, 491, 490, 487, 484, 480, 474, 473, 471, 470, 457, 453, 449, 442, 439, 436, 435, 433, 432, 431, 426, 418, 406, 406, 405, 398, 397, 393, 376, 359, 358, 356, 353, 347, 344, 328, 326, 324, 320, 302, 302, 283, 283, 264, 257, 248, 236, 236, 216, 190, 179, 179, 179, 179, 175, 166, 166, 147, 123, 114, 114, 89, 89, 89, 89, 89, 89, 82, 82, 82, 82, 82, 82, 82, 82, 82, 41, 41, 41, 38, 33, 33, 33, 33, 33, 33, 33, 33, 28, 28, 28, 28, 28, 28, 28, 28, 20, 14, 14, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 10, 10, 10, 10, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]

upa_cc_list = [1239, 1238, 1237, 1234, 1233, 1231, 1229, 1228, 1226, 1225, 1223, 1221, 1220, 1218, 1214, 1212, 1209, 1207, 1205, 1203, 1202, 1198, 1196, 1195, 1192, 1190, 1189, 1186, 1183, 1179, 1176, 1174, 1173, 1170, 1168, 1166, 1165, 1162, 1157, 1155, 1151, 1149, 1147, 1146, 1145, 1143, 1142, 1140, 1137, 1133, 1131, 1130, 1129, 1127, 1124, 1119, 1116, 1114, 1111, 1107, 1105, 1103, 1101, 1098, 1097, 1094, 1091, 1089, 1088, 1084, 1080, 1076, 1074, 1070, 1067, 1063, 1060, 1056, 1054, 1052, 1048, 1046, 1043, 1042, 1038, 1035, 1032, 1029, 1024, 1023, 1020, 1019, 1016, 1014, 1013, 1012, 1007, 1000, 998, 997, 990, 982, 978, 977, 976, 974, 973, 970, 968, 966, 964, 958, 955, 952, 948, 946, 944, 940, 935, 930, 924, 922, 920, 917, 908, 904, 901, 899, 898, 895, 888, 886, 879, 877, 874, 867, 864, 851, 849, 846, 835, 826, 822, 801, 796, 793, 791, 787, 784, 773, 767, 760, 755, 748, 739, 735, 709, 675, 672, 672, 666, 656, 629, 627, 595, 591, 573, 571, 571, 557, 544, 526, 515, 513, 498, 498, 493, 479, 479, 475, 471, 471, 322, 322, 292, 286, 286, 286, 286, 286, 283, 283, 268, 196, 180, 180, 82, 82, 82, 82, 82, 82, 77, 64, 64, 64, 64, 54, 54, 54, 54, 54, 42, 42, 42, 39, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 12, 12, 12, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]


nodes_rem = 0
for y_cord in compnw_cc_list:    
    dataset_compnw[y_cord] = nodes_rem
    nodes_rem +=1

nodes_rem = 0
for y_cord in er_cc_list:    
    dataset_er[y_cord] = nodes_rem
    nodes_rem +=1 

nodes_rem = 0
for y_cord in upa_cc_list:    
    dataset_upa[y_cord] = nodes_rem
    nodes_rem +=1     
    
simpleplot.plot_lines('Resilience of Network graph, ER graph, and UPA graph', 600, 
                      600, 'Number of nodes removed', 'Size of the largest connect component', 
                      [dataset_compnw,dataset_er, dataset_upa], True, 
                      ['Network graph', 'ER graph (p=0.004)', 'UPA graph(m=2)'])
    
                                                                  
    
    
    
    
            
            
            
            
                
    
    
    
    
    
    
    
    
    
    
    
    
    
