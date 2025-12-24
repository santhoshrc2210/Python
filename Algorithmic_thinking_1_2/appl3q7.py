"""
Example code for creating and visualizing
cluster of county-based cancer risk data

Note that you must download the file
http://www.codeskulptor.org/#alg_clusters_matplotlib.py
to use the matplotlib version of this code
"""

# Flavor of Python - desktop or CodeSkulptor
DESKTOP = False

import math
import random
import urllib2
import alg_cluster

# conditional imports
if DESKTOP:
    import alg_project3_solution      # desktop project solution
    import alg_clusters_matplotlib
else:
    import user52_OsKV4OlxLH_0 as alg_project3_solution   # CodeSkulptor project solution
    import alg_clusters_simplegui
    import codeskulptor
    codeskulptor.set_timeout(10000)


###################################################
# Code to load data tables

# URLs for cancer risk data tables of various sizes
# Numbers indicate number of counties in data table

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"


def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]


############################################################
# Code to create sequential clustering
# Create alphabetical clusters for county data

def sequential_clustering(singleton_list, num_clusters):
    """
    Take a data table and create a list of clusters
    by partitioning the table into clusters based on its ordering
    
    Note that method may return num_clusters or num_clusters + 1 final clusters
    """
    
    cluster_list = []
    cluster_idx = 0
    total_clusters = len(singleton_list)
    cluster_size = float(total_clusters)  / num_clusters
    
    for cluster_idx in range(len(singleton_list)):
        new_cluster = singleton_list[cluster_idx]
        if math.floor(cluster_idx / cluster_size) != \
           math.floor((cluster_idx - 1) / cluster_size):
            cluster_list.append(new_cluster)
        else:
            cluster_list[-1] = cluster_list[-1].merge_clusters(new_cluster)
            
    return cluster_list
                

########################################################################
"""
application:3
Question:7
"""


def compute_distortion(cluster_list):
    """
    that takes a list of clusters and uses 
    cluster_error to compute its distortion
    """
    
    sum_distortion = 0.0
    
    
    for each_cluster in cluster_list:
        sum_distortion += each_cluster.cluster_error(data_table)
        
    return sum_distortion
        

data_table = load_data_table(DATA_111_URL)
    
singleton_list = []
for line in data_table:
    singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

#the distortions associated with the 16 output clusters produced by hierarchical clustering 
#on the 290 county data set are approximately 2.575×1011        
#cluster_list = alg_project3_solution.hierarchical_clustering(singleton_list, 16)
#print compute_distortion(cluster_list)   

# k-means clustering (with 5 iterations) on the 290 county data set are approximately 
#2.323×10 11
#cluster_list = alg_project3_solution.kmeans_clustering(singleton_list, 16, 5)
#print compute_distortion(cluster_list) 


#Now, use compute_distortion to compute the distortions of the two clusterings in questions 5 and 6.    
#cluster_list = alg_project3_solution.hierarchical_clustering(singleton_list, 9)
#print compute_distortion(cluster_list)    
#ans: 175163886916.0
    
    
#cluster_list = alg_project3_solution.kmeans_clustering(singleton_list, 9, 5)
#print compute_distortion(cluster_list)    
#ans: 271254226924.0




  
        






        




