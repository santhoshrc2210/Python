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
    
def random_order(inp_graph):
    list_nodes = list()
    for node in inp_graph:
        list_nodes.append(node)
    random.shuffle(list_nodes)
    
    return list_nodes

#print random_order(make_complete_graph(8))

#load three graphs
compnw_graph = load_graph(NETWORK_URL)
er_graph = make_er_graph(1239, 0.004)
upa_graph = upa_alg(1239, 2)

#for each of the three graphs (computer network, ER, UPA), compute a random attack order

compnw_rand_att_ord = random_order(compnw_graph)
er_rand_att_ord = random_order(er_graph)
upa_rand_att_ord = random_order(upa_graph) 
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

#computed in codeskulptor (simulation time: 5 hrs run serially) and saved
compnw_cc_list = [1239, 1236, 1235, 1234, 1233, 1231, 1230, 1229, 1228, 1227, 1226, 1225, 1224, 1218, 1217, 1210, 1209, 1206, 1205, 1204, 1203, 1201, 1200, 1199, 1198, 1193, 1192, 1191, 1190, 1189, 1188, 1187, 1186, 1185, 1183, 1182, 1181, 1180, 1177, 1176, 1175, 1174, 1173, 1169, 1168, 1167, 1161, 1160, 1159, 1158, 1154, 1153, 1152, 1151, 1150, 1149, 1144, 1144, 1143, 1142, 1141, 1140, 1136, 1135, 1134, 1133, 1129, 1128, 1126, 1123, 1122, 1121, 1120, 1116, 1114, 1113, 1113, 1112, 1111, 1110, 1108, 1107, 1106, 1105, 1104, 1103, 1100, 1099, 1098, 1097, 1096, 1096, 1095, 1094, 1093, 1092, 1071, 1070, 1069, 1068, 1067, 1066, 1064, 1062, 1061, 1060, 1059, 1058, 1057, 1053, 1052, 1051, 1050, 1049, 1048, 1047, 1046, 1044, 1043, 1042, 1039, 1038, 1037, 1036, 1036, 1035, 1034, 1033, 1032, 1031, 1030, 1029, 1028, 1027, 1027, 1026, 1025, 1024, 1023, 1022, 1021, 1020, 1020, 1019, 1016, 1015, 1014, 1013, 1012, 1009, 1003, 990, 989, 988, 984, 983, 982, 981, 980, 979, 978, 977, 974, 973, 973, 972, 971, 970, 969, 968, 967, 966, 965, 964, 962, 961, 960, 959, 956, 955, 954, 953, 952, 952, 951, 950, 948, 947, 946, 945, 944, 943, 942, 915, 914, 913, 911, 910, 909, 907, 906, 905, 904, 903, 902, 901, 900, 899, 897, 896, 895, 894, 887, 887, 881, 879, 878, 877, 876, 874, 873, 872, 868, 865, 865, 863, 861, 860, 858, 857, 856, 855, 854, 854, 853, 852, 852, 851, 846, 845, 845, 840, 840, 838, 837, 836, 836, 835, 834, 833, 832, 831, 830, 829, 828, 827, 824, 824, 823, 822, 821, 820, 819, 818, 817, 816, 815, 814, 813, 812, 811, 808, 807, 806, 804, 801, 798, 792, 786, 785, 785, 784, 783, 782, 781, 780, 779, 778, 777, 776, 775, 775, 773, 772, 771, 747, 747, 746, 745, 744, 744, 743, 741, 740, 740, 740, 739, 739, 738, 734, 733, 733, 732, 732, 731, 730, 729, 728, 728, 727, 726, 725, 724, 724, 724, 723, 722, 719, 716, 714, 711, 710, 709, 708, 707, 707, 705, 704, 703, 701, 700, 699, 698, 697, 694, 694, 693, 692, 691, 691, 691, 690, 689, 688, 687, 685, 684, 683, 683, 682, 682, 681, 681, 680, 678, 669, 668, 667, 666, 666, 665, 664, 664, 663, 662, 662, 662, 661, 660, 659, 658, 657, 657, 656, 655, 654, 653, 652, 651, 651, 650, 650, 649, 649, 648, 647, 646, 646, 645, 644, 642, 641, 641, 641, 640, 639, 638, 637, 637, 637, 636, 635, 634, 630, 630, 627, 626, 626, 625, 624, 624, 623, 623, 623, 622, 621, 620, 619, 618, 617, 616, 616, 615, 613, 613, 611, 610, 609, 608, 608, 604, 603, 603, 598, 597, 596, 595, 595, 594, 594, 593, 593, 592, 591, 591, 590, 590, 588, 587, 586, 583, 583, 583, 582, 580, 579, 566, 564, 563, 563, 563, 563, 563, 562, 561, 560, 559, 559, 559, 558, 557, 557, 556, 556, 554, 553, 552, 551, 551, 550, 546, 546, 540, 528, 528, 527, 526, 525, 524, 524, 523, 523, 522, 521, 520, 520, 519, 519, 518, 517, 516, 515, 510, 508, 508, 507, 506, 486, 485, 484, 483, 482, 481, 480, 480, 480, 480, 478, 478, 477, 477, 473, 472, 472, 471, 470, 470, 469, 468, 467, 467, 467, 467, 466, 465, 465, 465, 464, 462, 461, 460, 460, 459, 458, 456, 453, 452, 452, 452, 451, 449, 449, 449, 448, 448, 447, 446, 445, 443, 443, 442, 441, 440, 440, 439, 438, 430, 429, 429, 428, 427, 427, 426, 426, 426, 425, 425, 425, 424, 423, 422, 415, 415, 415, 414, 414, 413, 413, 413, 412, 412, 412, 411, 410, 409, 408, 407, 405, 404, 403, 402, 401, 401, 400, 399, 399, 399, 399, 399, 398, 397, 396, 395, 394, 394, 394, 394, 393, 393, 392, 387, 386, 384, 383, 383, 382, 382, 381, 380, 380, 380, 379, 378, 376, 375, 375, 374, 374, 373, 372, 372, 371, 371, 370, 369, 369, 369, 368, 368, 368, 367, 366, 365, 365, 365, 365, 364, 363, 362, 362, 354, 354, 353, 351, 350, 348, 347, 347, 346, 346, 346, 346, 346, 342, 341, 340, 339, 339, 339, 338, 336, 336, 335, 334, 333, 333, 333, 332, 331, 330, 330, 329, 329, 327, 327, 323, 322, 321, 320, 319, 316, 316, 315, 314, 314, 314, 313, 313, 312, 311, 310, 309, 308, 307, 299, 298, 298, 298, 298, 267, 266, 266, 266, 266, 266, 265, 265, 265, 265, 265, 265, 264, 261, 261, 260, 260, 259, 258, 258, 258, 258, 257, 256, 255, 255, 254, 249, 248, 248, 248, 247, 247, 247, 246, 246, 239, 238, 238, 238, 234, 233, 232, 230, 230, 227, 222, 161, 161, 160, 160, 160, 157, 157, 157, 156, 156, 156, 156, 156, 156, 156, 155, 154, 154, 154, 154, 154, 154, 154, 154, 154, 154, 153, 153, 152, 151, 151, 150, 149, 149, 149, 148, 147, 147, 147, 147, 147, 146, 145, 144, 144, 144, 144, 144, 144, 144, 144, 144, 143, 143, 143, 142, 142, 142, 142, 142, 141, 141, 141, 140, 139, 138, 138, 137, 136, 136, 136, 57, 57, 57, 57, 56, 56, 56, 56, 56, 56, 56, 56, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 54, 54, 54, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 52, 52, 51, 51, 51, 50, 50, 50, 49, 48, 47, 47, 47, 47, 47, 46, 46, 46, 46, 46, 45, 44, 44, 44, 44, 44, 43, 42, 42, 41, 41, 40, 40, 40, 40, 39, 39, 39, 39, 39, 38, 38, 38, 37, 37, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 34, 34, 34, 34, 33, 32, 32, 32, 31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 16, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 11, 11, 11, 11, 10, 10, 10, 10, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 7, 7, 7, 7, 7, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]

er_cc_list = [1239, 1238, 1237, 1236, 1235, 1234, 1233, 1232, 1231, 1230, 1229, 1228, 1227, 1226, 1225, 1224, 1223, 1222, 1221, 1220, 1219, 1218, 1217, 1216, 1215, 1214, 1213, 1212, 1211, 1210, 1209, 1208, 1207, 1206, 1205, 1204, 1203, 1202, 1201, 1200, 1199, 1198, 1197, 1196, 1195, 1194, 1193, 1192, 1191, 1190, 1189, 1188, 1187, 1186, 1185, 1184, 1183, 1182, 1181, 1180, 1179, 1178, 1177, 1176, 1175, 1174, 1173, 1172, 1171, 1170, 1169, 1168, 1167, 1166, 1165, 1164, 1163, 1162, 1161, 1160, 1159, 1158, 1157, 1156, 1155, 1154, 1153, 1152, 1151, 1150, 1149, 1148, 1147, 1146, 1145, 1144, 1143, 1142, 1141, 1140, 1139, 1138, 1137, 1136, 1135, 1134, 1133, 1132, 1131, 1130, 1129, 1128, 1127, 1126, 1125, 1124, 1123, 1122, 1121, 1120, 1119, 1118, 1117, 1116, 1115, 1114, 1113, 1112, 1111, 1110, 1109, 1108, 1107, 1106, 1105, 1104, 1103, 1102, 1101, 1100, 1099, 1098, 1097, 1096, 1095, 1094, 1093, 1092, 1091, 1090, 1089, 1088, 1087, 1086, 1085, 1084, 1083, 1082, 1081, 1080, 1079, 1078, 1077, 1076, 1075, 1074, 1073, 1072, 1071, 1070, 1069, 1068, 1067, 1066, 1065, 1064, 1063, 1062, 1061, 1060, 1059, 1058, 1057, 1056, 1055, 1054, 1053, 1052, 1051, 1050, 1049, 1048, 1047, 1046, 1045, 1044, 1043, 1042, 1041, 1040, 1039, 1038, 1037, 1036, 1035, 1034, 1033, 1032, 1031, 1030, 1029, 1028, 1027, 1026, 1025, 1024, 1023, 1022, 1021, 1020, 1019, 1018, 1017, 1016, 1015, 1014, 1013, 1012, 1011, 1010, 1009, 1008, 1007, 1006, 1005, 1004, 1003, 1002, 1001, 1000, 999, 998, 997, 996, 995, 994, 993, 992, 991, 990, 989, 988, 987, 986, 985, 984, 983, 982, 981, 980, 979, 978, 977, 976, 975, 974, 973, 972, 971, 970, 969, 968, 967, 966, 965, 964, 963, 962, 961, 960, 959, 958, 957, 956, 955, 954, 953, 952, 951, 950, 949, 948, 947, 946, 945, 944, 943, 942, 941, 940, 939, 938, 937, 936, 935, 934, 933, 932, 931, 930, 929, 928, 927, 926, 925, 924, 923, 922, 921, 920, 919, 918, 917, 916, 915, 914, 913, 912, 911, 910, 909, 908, 907, 906, 905, 904, 903, 902, 900, 899, 898, 897, 896, 895, 894, 893, 892, 891, 890, 889, 888, 887, 886, 885, 884, 883, 882, 881, 880, 879, 878, 877, 876, 875, 874, 873, 872, 871, 870, 869, 868, 867, 866, 865, 864, 863, 862, 861, 860, 859, 858, 857, 856, 855, 854, 853, 852, 851, 850, 849, 848, 847, 846, 844, 843, 842, 841, 840, 839, 838, 837, 836, 835, 834, 833, 832, 831, 830, 829, 828, 827, 826, 825, 824, 823, 822, 821, 820, 819, 818, 817, 816, 815, 814, 813, 812, 811, 810, 809, 808, 807, 806, 805, 804, 803, 802, 801, 800, 799, 798, 797, 796, 795, 794, 793, 792, 791, 790, 789, 788, 787, 786, 785, 784, 783, 782, 781, 780, 779, 778, 777, 776, 775, 774, 773, 772, 771, 770, 769, 768, 767, 766, 765, 764, 763, 762, 761, 760, 759, 758, 757, 756, 755, 754, 753, 752, 751, 750, 749, 748, 747, 746, 745, 743, 742, 741, 740, 739, 738, 737, 736, 735, 734, 733, 732, 731, 730, 729, 728, 727, 726, 725, 724, 723, 722, 721, 720, 719, 718, 717, 716, 715, 714, 713, 712, 711, 710, 709, 708, 707, 706, 705, 704, 703, 702, 701, 700, 699, 698, 697, 696, 695, 694, 693, 692, 691, 690, 689, 688, 686, 685, 684, 683, 682, 681, 680, 679, 678, 677, 676, 675, 674, 673, 672, 671, 670, 669, 668, 667, 666, 665, 664, 663, 662, 661, 660, 659, 658, 657, 656, 655, 654, 653, 652, 651, 650, 649, 648, 647, 646, 645, 644, 643, 642, 641, 640, 639, 638, 636, 635, 634, 633, 632, 631, 630, 629, 628, 627, 626, 625, 624, 623, 622, 621, 620, 619, 618, 617, 616, 615, 614, 613, 612, 611, 610, 609, 608, 607, 606, 605, 604, 603, 602, 601, 600, 599, 598, 596, 595, 594, 593, 592, 591, 590, 589, 588, 587, 586, 585, 584, 583, 582, 581, 579, 578, 577, 576, 575, 574, 574, 573, 572, 571, 570, 569, 568, 567, 566, 565, 564, 563, 562, 561, 560, 559, 558, 557, 555, 554, 553, 552, 551, 550, 549, 548, 547, 546, 545, 544, 543, 542, 541, 540, 539, 538, 537, 536, 535, 534, 533, 532, 531, 530, 529, 528, 527, 526, 525, 524, 523, 522, 521, 521, 520, 519, 518, 517, 516, 515, 514, 513, 511, 510, 509, 508, 507, 506, 505, 504, 502, 501, 500, 499, 498, 496, 495, 494, 493, 492, 491, 490, 489, 488, 487, 486, 485, 483, 482, 481, 481, 480, 479, 478, 477, 476, 475, 474, 473, 472, 471, 470, 469, 468, 467, 466, 465, 464, 463, 462, 461, 460, 459, 458, 457, 456, 455, 454, 453, 452, 451, 449, 448, 447, 446, 444, 443, 442, 441, 440, 439, 438, 436, 435, 434, 433, 432, 431, 430, 429, 428, 427, 426, 425, 424, 423, 422, 421, 419, 418, 417, 417, 416, 415, 414, 413, 412, 411, 407, 406, 405, 404, 403, 402, 401, 400, 398, 396, 395, 394, 394, 393, 392, 391, 390, 388, 387, 386, 385, 384, 383, 382, 381, 380, 379, 378, 377, 377, 376, 374, 373, 372, 371, 370, 366, 365, 364, 364, 362, 360, 359, 358, 357, 356, 353, 352, 351, 350, 349, 348, 346, 345, 344, 343, 342, 341, 340, 339, 338, 337, 336, 335, 334, 333, 332, 331, 331, 330, 329, 326, 325, 324, 323, 323, 322, 321, 320, 319, 317, 316, 315, 314, 312, 311, 310, 309, 308, 307, 305, 304, 303, 301, 300, 299, 297, 295, 294, 293, 292, 290, 290, 289, 288, 286, 286, 285, 284, 283, 282, 282, 281, 280, 278, 277, 276, 274, 273, 272, 271, 270, 269, 268, 267, 266, 264, 263, 262, 260, 259, 258, 257, 256, 254, 251, 251, 249, 248, 247, 246, 246, 245, 244, 244, 244, 243, 242, 241, 240, 240, 239, 238, 235, 233, 230, 229, 228, 225, 224, 223, 221, 220, 219, 215, 213, 212, 211, 210, 209, 208, 208, 207, 207, 205, 204, 204, 204, 203, 200, 200, 200, 200, 198, 196, 194, 191, 188, 187, 186, 185, 184, 183, 183, 181, 181, 180, 179, 177, 176, 176, 175, 172, 171, 170, 170, 165, 165, 164, 162, 155, 155, 154, 154, 153, 151, 151, 149, 148, 148, 147, 146, 145, 144, 140, 137, 136, 135, 131, 130, 129, 128, 127, 126, 125, 120, 118, 118, 118, 116, 115, 113, 113, 113, 112, 111, 111, 111, 108, 108, 105, 102, 102, 102, 100, 99, 98, 91, 91, 90, 88, 87, 87, 87, 72, 71, 68, 68, 68, 68, 68, 58, 58, 58, 58, 58, 58, 56, 56, 56, 56, 56, 35, 35, 35, 33, 33, 33, 33, 33, 33, 31, 19, 19, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 11, 11, 11, 11, 11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]

upa_cc_list = [1239, 1238, 1237, 1236, 1235, 1234, 1233, 1232, 1231, 1230, 1229, 1228, 1227, 1226, 1225, 1224, 1223, 1222, 1221, 1220, 1219, 1218, 1217, 1216, 1215, 1214, 1213, 1212, 1211, 1210, 1209, 1208, 1207, 1206, 1205, 1204, 1203, 1202, 1201, 1200, 1199, 1198, 1197, 1196, 1195, 1194, 1193, 1192, 1191, 1190, 1189, 1188, 1187, 1186, 1185, 1184, 1183, 1182, 1181, 1180, 1179, 1178, 1177, 1176, 1175, 1174, 1173, 1172, 1171, 1170, 1169, 1168, 1167, 1166, 1165, 1164, 1163, 1162, 1161, 1159, 1158, 1157, 1156, 1155, 1154, 1153, 1152, 1151, 1150, 1149, 1148, 1147, 1146, 1145, 1144, 1143, 1142, 1141, 1140, 1139, 1138, 1137, 1136, 1135, 1134, 1133, 1131, 1129, 1128, 1127, 1126, 1125, 1124, 1123, 1122, 1121, 1120, 1119, 1118, 1117, 1115, 1114, 1113, 1111, 1110, 1109, 1108, 1107, 1106, 1105, 1104, 1102, 1101, 1100, 1099, 1097, 1096, 1095, 1094, 1093, 1092, 1090, 1085, 1084, 1083, 1082, 1081, 1080, 1079, 1078, 1077, 1076, 1075, 1073, 1072, 1071, 1069, 1068, 1067, 1066, 1065, 1064, 1063, 1062, 1061, 1060, 1059, 1058, 1057, 1056, 1055, 1054, 1053, 1050, 1049, 1048, 1047, 1046, 1046, 1045, 1044, 1043, 1042, 1041, 1040, 1039, 1038, 1037, 1036, 1035, 1034, 1033, 1032, 1031, 1030, 1029, 1028, 1027, 1026, 1025, 1024, 1023, 1022, 1021, 1020, 1019, 1018, 1017, 1016, 1015, 1014, 1012, 1011, 1010, 1010, 1009, 1008, 1007, 1006, 1005, 1004, 1003, 1002, 1001, 1000, 999, 997, 996, 995, 994, 993, 992, 991, 990, 989, 988, 987, 985, 984, 983, 982, 981, 980, 978, 977, 976, 975, 974, 973, 972, 971, 968, 965, 964, 963, 962, 961, 960, 959, 958, 956, 954, 953, 952, 951, 950, 949, 948, 947, 945, 942, 941, 940, 939, 938, 935, 934, 932, 931, 930, 929, 928, 927, 926, 925, 924, 923, 923, 922, 920, 919, 918, 917, 916, 915, 914, 912, 911, 910, 909, 908, 907, 905, 904, 903, 902, 901, 900, 899, 898, 897, 896, 895, 894, 892, 891, 890, 889, 887, 885, 884, 883, 882, 881, 880, 879, 878, 877, 876, 875, 873, 872, 865, 864, 863, 862, 860, 859, 857, 855, 854, 853, 852, 850, 848, 847, 846, 845, 844, 843, 842, 841, 840, 839, 837, 835, 834, 831, 830, 828, 828, 827, 824, 823, 822, 821, 819, 818, 817, 816, 815, 814, 813, 812, 808, 806, 805, 803, 802, 801, 800, 800, 799, 798, 797, 797, 795, 794, 793, 792, 791, 789, 787, 786, 785, 784, 783, 783, 782, 781, 780, 779, 778, 778, 777, 775, 775, 774, 771, 770, 769, 767, 765, 764, 763, 762, 761, 760, 759, 757, 756, 755, 754, 753, 752, 749, 747, 746, 745, 744, 741, 739, 736, 735, 734, 733, 730, 730, 729, 728, 727, 725, 724, 723, 721, 721, 720, 719, 719, 718, 717, 716, 715, 714, 713, 712, 711, 710, 709, 708, 707, 704, 703, 702, 696, 695, 694, 693, 692, 690, 689, 687, 686, 685, 684, 683, 681, 680, 679, 676, 675, 675, 674, 673, 672, 671, 670, 664, 663, 662, 660, 660, 660, 659, 658, 650, 649, 647, 646, 645, 643, 643, 642, 641, 640, 639, 638, 635, 634, 633, 632, 631, 630, 629, 624, 620, 619, 618, 616, 615, 613, 613, 612, 611, 609, 600, 599, 597, 596, 595, 593, 592, 591, 588, 587, 586, 585, 584, 583, 582, 581, 581, 580, 579, 575, 574, 573, 572, 571, 567, 566, 565, 561, 560, 559, 559, 556, 555, 554, 552, 551, 550, 549, 549, 549, 548, 547, 541, 540, 540, 540, 539, 538, 537, 536, 535, 532, 532, 528, 527, 526, 525, 520, 519, 518, 515, 514, 514, 513, 512, 511, 510, 509, 508, 506, 504, 504, 504, 503, 503, 502, 502, 500, 499, 498, 493, 491, 490, 489, 488, 487, 480, 478, 477, 476, 475, 475, 474, 474, 473, 472, 472, 471, 471, 470, 469, 469, 468, 467, 467, 466, 465, 464, 463, 463, 462, 461, 459, 457, 456, 455, 453, 450, 449, 449, 448, 447, 447, 446, 446, 446, 445, 444, 443, 442, 442, 441, 441, 440, 439, 438, 437, 437, 436, 435, 433, 430, 429, 429, 429, 428, 428, 428, 426, 425, 424, 423, 421, 420, 420, 417, 415, 415, 414, 413, 411, 410, 408, 407, 406, 404, 403, 403, 383, 383, 382, 381, 380, 380, 379, 379, 378, 377, 376, 375, 373, 372, 371, 370, 370, 368, 367, 367, 367, 366, 366, 365, 362, 358, 357, 356, 356, 355, 345, 344, 341, 341, 340, 339, 338, 331, 330, 329, 328, 328, 327, 326, 325, 324, 324, 324, 321, 320, 316, 316, 315, 315, 314, 313, 312, 311, 309, 307, 307, 305, 304, 303, 303, 303, 303, 302, 299, 297, 296, 295, 292, 291, 290, 289, 287, 240, 239, 236, 236, 234, 232, 229, 226, 226, 225, 225, 191, 191, 189, 188, 188, 187, 158, 157, 157, 157, 157, 156, 156, 156, 156, 156, 156, 154, 154, 153, 149, 149, 149, 149, 149, 145, 145, 145, 137, 136, 124, 124, 124, 123, 123, 123, 123, 123, 123, 117, 117, 116, 116, 115, 114, 111, 111, 111, 111, 111, 111, 55, 55, 54, 50, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 48, 48, 48, 48, 48, 48, 48, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 21, 21, 21, 21, 21, 21, 21, 21, 21, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]


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
    
                                                                  
    
    
    
    
            
            
            
            
                
    
    
    
    
    
    
    
    
    
    
    
    
    
