
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
    
    for node_rem in attack_order:
        ugraph.pop(node_rem)       
        for node in ugraph:
            if node_rem in ugraph[node]:
                ugraph[node].remove(node_rem)
        largest_cc_list.append(largest_cc_size(ugraph))       
    
        
    
    return largest_cc_list
                
                

        
        
        
        
    
    
    
    
    
    
    
    
    
            
            
            
            
            
