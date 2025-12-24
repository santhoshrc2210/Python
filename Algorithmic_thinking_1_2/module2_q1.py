"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""

# general imports
import urllib2

# Set timeout for CodeSkulptor if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

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

#

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

citation_graph = load_graph(CITATION_URL)

###################Q:1

####part:1
#Your task for this question is to compute the in-degree distribution 
#for this citation graph
in_degree_citation_graph = in_degree_distribution(citation_graph)

print in_degree_citation_graph[8]

#####part:2
##Once you have computed this distribution, you should normalize the distribution 
#(make the values in the dictionary sum to one)
total_in_degrees = 0.0
for node in in_degree_citation_graph:
    total_in_degrees += in_degree_citation_graph[node]

in_degree_dist_normal = {}
for node in in_degree_citation_graph:
    in_degree_dist_normal[node] = in_degree_citation_graph[node]/total_in_degrees
    
print in_degree_dist_normal[8]
    
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
simpleplot.plot_lines('Normalized in-degree distribution of citation', 600, 600, 'number of in_degrees', 'number of papers with in_degrees (normalized)', [dataset_in_degree_dist_normal_loglog], True, ['Normalized in-degree distribution of citation'])
