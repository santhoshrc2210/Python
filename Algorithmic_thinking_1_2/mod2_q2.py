#######Question:2

import random


###part-1:
#For every ordered pair of distinct nodes (i,j) modified algorithm adds the
#directed edge from i to j with probability p

probability_edge = 0.3;
num_nodes = 1000;
dir_graph = dict ()


for node in range(num_nodes):
    dir_graph[node] = set()
    for tail_node in range(num_nodes):
        rand_num = random.random()
        if rand_num < probability_edge and tail_node != node:          
            dir_graph[node].add(tail_node)
                
#print dir_graph
        
            
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

#print(compute_in_degrees(EX_GRAPH2))

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

#citation_graph = load_graph(CITATION_URL)

###################Q:1

####part:1
#Your task for this question is to compute the in-degree distribution 
#for this citation graph
in_degree_citation_graph = in_degree_distribution(dir_graph)

#print in_degree_citation_graph[7]

#####part:2
##Once you have computed this distribution, you should normalize the distribution 
#(make the values in the dictionary sum to one)
total_in_degrees = 0.0
for node in in_degree_citation_graph:
    total_in_degrees += in_degree_citation_graph[node]

in_degree_dist_normal = {}
for node in in_degree_citation_graph:
    in_degree_dist_normal[node] = in_degree_citation_graph[node]/total_in_degrees
    
#print in_degree_dist_normal[8]
    
###part:3
# then compute a log/log plot of the points in this normalized distribution


import simpleplot
import math

dataset_in_degree_dist_normal_loglog = {}
#print math.log(100)

for key in in_degree_dist_normal:
    #print "key:", key
    if key != 0:
        dataset_in_degree_dist_normal_loglog[math.log(key)] = math.log(in_degree_dist_normal[key])
    
#print  dataset_in_degree_dist_normal_loglog 
simpleplot.plot_lines('Normalized in-degree distribution of citation', 600, 600, 'log of number of in_degrees', 'log of number of papers with in_degrees (normalized)', [dataset_in_degree_dist_normal_loglog], True, ['Normalized in-degree distribution of citation'])

############Q:2

#Q.2.1 :

#Ans:yes the expected value of the in-degree is the same for every as the probability
#to form a link is p same for every link

#Q.2.2:
#Ans: ER graph shows the number of nodes with high in-degree is similar to that with low in-degree
#most of the nodes are centered around the graph as the graph peaks at the centre

#Q.2.3:
#Ans: No the shapes are very different, ER graph looks similar to a gaussian distribution as the
#links are assigned randomly.
# citation graph shows there are many papers with large number of citations and few papers
#with lower number of citations as this goes to show that few papers are more relavent than others
#














