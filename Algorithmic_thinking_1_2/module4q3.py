import random
###########################
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

###############################################

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
    

##############################

##############################
# For this question, your task is to implement fast_targeted_order
def fast_targeted_order(ugraph):
    
    ugraph_orig = ugraph
    
    DegreeSets = dict()
    for degree in range(len(ugraph)):
        DegreeSets[degree] = set()
        
    for node in ugraph:
        degree = len(ugraph[node])
        DegreeSets[degree].add(node)
        
    list_nodes_deg = list()
    i = 0
    
    len_ugraph = len(ugraph)
    
    for k in range((len_ugraph-1), -1, -1):
        while DegreeSets[k]:
            temp_list = list(DegreeSets[k])
            rand_node = random.choice(temp_list)
            DegreeSets[k].discard(rand_node)
            for neighb in ugraph[rand_node]:
                degree_neighb = len(ugraph[neighb])
                DegreeSets[degree_neighb].discard(neighb)
                DegreeSets[degree_neighb-1].add(neighb)
                ugraph[neighb].remove(rand_node)
            
            list_nodes_deg.insert(i, rand_node)
            i += 1
            
            ugraph.pop(rand_node)
            

    return list_nodes_deg 
 
##############################           
#calculated dataset from desktop python using above listed functions

#dataset_fast = dict()

#for n in range(10, 1000, 10):
#    graph = upa_alg(n,5)
#    start_time = time.perf_counter()
#    #fast_targeted_order(graph)
#    targeted_order(graph)
#    end_time = time.perf_counter()
#    dataset_fast[n] = end_time-start_time

#print(dataset_fast)

##############################

import simpleplot

dataset_fast_target_order = {770: 0.0031035467982292175, 260: 0.0008725300431251526, 520: 0.0020869411528110504, 10: 3.186613321304321e-05, 780: 0.0031493790447711945, 270: 0.0009110383689403534, 530: 0.002074398100376129, 20: 0.00013520196080207825, 790: 0.0031963102519512177, 280: 0.0009334683418273926, 540: 0.0021590963006019592, 30: 8.45976173877716e-05, 800: 0.0032502934336662292, 290: 0.0009895451366901398, 550: 0.0021936967968940735, 40: 0.00011292845010757446, 810: 0.003298584371805191, 300: 0.0010398775339126587, 560: 0.002249881625175476, 50: 0.0001441948115825653, 820: 0.0033965855836868286, 310: 0.0010578706860542297, 570: 0.002286415547132492, 60: 0.00017394497990608215, 830: 0.0033879317343235016, 320: 0.0017077215015888214, 580: 0.002349376678466797, 70: 0.00020465999841690063, 840: 0.0034878142178058624, 330: 0.0011399202048778534, 590: 0.0023802481591701508, 80: 0.00023473426699638367, 850: 0.0035105235874652863, 340: 0.0011773817241191864, 600: 0.0024325288832187653, 90: 0.00027088820934295654, 860: 0.0035701021552085876, 350: 0.0013524405658245087, 610: 0.002491191029548645, 100: 0.0003029480576515198, 870: 0.003636658191680908, 360: 0.0013679489493370056, 620: 0.0025193579494953156, 110: 0.00033884868025779724, 880: 0.0037338286638259888, 370: 0.001410704106092453, 630: 0.0025839954614639282, 120: 0.000380098819732666, 890: 0.003720935434103012, 380: 0.0014457963407039642, 640: 0.002584856003522873, 130: 0.0003970824182033539, 900: 0.003775276243686676, 390: 0.001505330204963684, 650: 0.0026617832481861115, 140: 0.00043351948261260986, 910: 0.004222244024276733, 400: 0.0015339143574237823, 660: 0.002694513648748398, 150: 0.0004724264144897461, 920: 0.0042627230286598206, 410: 0.001577034592628479, 670: 0.002737615257501602, 160: 0.000496838241815567, 930: 0.004315134137868881, 420: 0.0016276761889457703, 680: 0.0027983710169792175, 170: 0.0005333758890628815, 940: 0.004371214658021927, 430: 0.0016728676855564117, 690: 0.0028631724417209625, 180: 0.0005760490894317627, 950: 0.004469461739063263, 440: 0.0017320476472377777, 700: 0.0027683526277542114, 190: 0.0005998089909553528, 960: 0.004592042416334152, 450: 0.001746438443660736, 710: 0.0027585774660110474, 200: 0.0006383694708347321, 970: 0.0045445747673511505, 460: 0.0018074028193950653, 720: 0.00284750759601593, 210: 0.0006735548377037048, 980: 0.004618600010871887, 470: 0.0018289275467395782, 730: 0.0028708912432193756, 220: 0.0007038824260234833, 990: 0.004648707807064056, 480: 0.0019009299576282501, 740: 0.002967745065689087, 230: 0.0007713772356510162, 490: 0.0019459202885627747, 750: 0.0029857009649276733, 240: 0.0008054077625274658, 500: 0.001958843320608139, 760: 0.003042396157979965, 250: 0.0008480995893478394, 510: 0.002005498856306076}
dataset_target_order = {770: 0.017036736011505127, 260: 0.002064574509859085, 520: 0.0076997652649879456, 10: 1.862272620201111e-05, 780: 0.017302781343460083, 270: 0.0022434666752815247, 530: 0.007942117750644684, 20: 3.7901103496551514e-05, 790: 0.017795901745557785, 280: 0.0023758895695209503, 540: 0.008257504552602768, 30: 6.448104977607727e-05, 800: 0.018229950219392776, 290: 0.0029082484543323517, 550: 0.008519504219293594, 40: 9.267404675483704e-05, 810: 0.018617261201143265, 300: 0.002703160047531128, 560: 0.008821267634630203, 50: 0.00013155117630958557, 820: 0.019040092825889587, 310: 0.0029133930802345276, 570: 0.009082235395908356, 60: 0.0001726485788822174, 830: 0.019724667072296143, 320: 0.0030946284532546997, 580: 0.009429924190044403, 70: 0.00021922960877418518, 840: 0.019866187125444412, 330: 0.0032289065420627594, 590: 0.009992241859436035, 80: 0.0002757422626018524, 850: 0.020356692373752594, 340: 0.003397475928068161, 600: 0.010047882795333862, 90: 0.0003325454890727997, 860: 0.020761296153068542, 350: 0.003680255264043808, 610: 0.010406672954559326, 100: 0.0003948882222175598, 870: 0.021550633013248444, 360: 0.003908105194568634, 620: 0.010704126209020615, 110: 0.0004587024450302124, 880: 0.021727897226810455, 370: 0.0040755681693553925, 630: 0.011005088686943054, 120: 0.0005355030298233032, 890: 0.02201024442911148, 380: 0.004389703273773193, 640: 0.011460639536380768, 130: 0.0006064362823963165, 900: 0.023002441972494125, 390: 0.004538048058748245, 650: 0.011758629232645035, 140: 0.0007137060165405273, 910: 0.023359261453151703, 400: 0.00481826439499855, 660: 0.012083545327186584, 150: 0.000771835446357727, 920: 0.023512352257966995, 410: 0.004935454577207565, 670: 0.01237604022026062, 160: 0.000867847353219986, 930: 0.024281587451696396, 420: 0.005176752805709839, 680: 0.013099677860736847, 170: 0.0009546279907226562, 940: 0.02484305202960968, 430: 0.005374882370233536, 690: 0.014024317264556885, 180: 0.0010950341820716858, 950: 0.02521255612373352, 440: 0.0057008713483810425, 700: 0.014209970831871033, 190: 0.0012079030275344849, 960: 0.025725699961185455, 450: 0.005829457193613052, 710: 0.014542963355779648, 200: 0.0013205520808696747, 970: 0.026102058589458466, 460: 0.006119739264249802, 720: 0.015039760619401932, 210: 0.001439657062292099, 980: 0.026608679443597794, 470: 0.006383907049894333, 730: 0.015462279319763184, 220: 0.0015431717038154602, 990: 0.027180265635252, 480: 0.006594806909561157, 740: 0.015686437487602234, 230: 0.001744292676448822, 490: 0.006886281073093414, 750: 0.016548365354537964, 240: 0.0018773265182971954, 500: 0.007133081555366516, 760: 0.01653222367167473, 250: 0.0019720494747161865, 510: 0.007424596697092056}

simpleplot.plot_lines('Regular vs Fast Computaion of targeted order', 800, 600, 'Size of UPA Grap, m=5', 'Running time in seconds', 
                      [dataset_fast_target_order, dataset_target_order ], True, 
                      ['fast_target_order', 'target_order'])


















                           
        
        
    
        
        
    
