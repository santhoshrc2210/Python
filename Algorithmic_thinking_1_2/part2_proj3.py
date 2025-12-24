"""
Project 3

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)
"""

import math
import alg_cluster
 
    
def closest_pair_strip(cluster_list, horiz_center, half_width):   
    """
    inputs Takes a list of Cluster objects and two floats: horiz_center and half_width
    outputs  return a tuple corresponding to the closest pair of clusters that lie in 
    the specified strip.
     the return pair of indices should be in ascending order.
    """
    
    points_list = list(cluster_list)
    mid_set = []
    for point in cluster_list:
        if abs(point.horiz_center()- horiz_center) < half_width:
            mid_set.append(point)
            
    mid_set.sort(key=lambda cluster: cluster.vert_center())
    
    mid_len = len(mid_set)
    
    min_dist_pair = [float("inf"), -1, -1]
    point_dist_pair = [None] * 3
    
    for idx1 in range(mid_len-1):
        start_loop = idx1+1
        stop_num = (idx1+3, (mid_len-1))
        stop_loop = min(stop_num) + 1
        for idx2 in range(start_loop, stop_loop):
            point_dist_pair[0] = mid_set[idx1].distance(mid_set[idx2])
            if point_dist_pair[0] < min_dist_pair[0]:
                min_dist_pair[0] = point_dist_pair[0] 
                min_dist_pair[1] = min(points_list.index(mid_set[idx1]), 
                                       points_list.index(mid_set[idx2]))
                min_dist_pair[2] = max(points_list.index(mid_set[idx1]), 
                                       points_list.index(mid_set[idx2]))
    return tuple(min_dist_pair)


def slow_closest_pair(cluster_list):    
    """
    input takes a list of cluster objects
    output returns a closest pair where the pair is represented by the tuple(dist, idx1, idx2)
     
    idx1 < idx2 where dist is the distance between the closest pair 
    cluster_list[idx1]and cluster_list[idx2]
    implement the brute-force closest pair method    
    """
    
    points_list = list(cluster_list)
    min_dist_pair = [float("inf"), -1, -1]
    len_points_list = len(points_list)
    
    for idx1 in range(len_points_list):
        for idx2 in range(len_points_list):
            if idx1 != idx2:
                distance = points_list[idx1].distance(points_list[idx2])
                if distance < min_dist_pair[0]:
                    min_dist_pair[0] = distance 
                    min_dist_pair[1] = min(idx1, idx2)
                    min_dist_pair[2] = max(idx1, idx2)
                    
                                                            
    return tuple(min_dist_pair)

##############################to overcome timeout error#############
                
def fast_closest_pair(cluster_list):  
    """
    input: takes a list of cluster objects
    output: returns a closest pair where the pair is represented by the tuple(dist, idx1, idx2)
     
    idx1 < idx2 where dist is the distance between the closest pair 
    cluster_list[idx1]and cluster_list[idx2]

    This function should implement the divide-and-conquer closest pair method   
    """
    
    points_list = list(cluster_list)
    num_of_points = len(points_list)
    
    if num_of_points <= 3:
        min_dist_pair = list(slow_closest_pair(cluster_list))
        
    else:
        
        idx_div2 = int(math.floor(num_of_points/2.0)) 
        
        points_list_left = list()
        for idx in range(idx_div2):
            points_list_left.append(points_list[idx]) 
        
        points_list_right = list()
        for idx in range(idx_div2, num_of_points):
            points_list_right.append(points_list[idx])
            
        min_dist_pair_left = list(fast_closest_pair(points_list_left))
        min_dist_pair_right = list(fast_closest_pair(points_list_right))
        
        min_dist_pair_right[1] = min_dist_pair_right[1] + idx_div2
        min_dist_pair_right[2] = min_dist_pair_right[2] + idx_div2
        
        
        if  min_dist_pair_left[0] <= min_dist_pair_right[0]:
            min_dist_pair = min_dist_pair_left
        #including equal to condition
        else:
            min_dist_pair = min_dist_pair_right
            
        mid = 0.5*(points_list[idx_div2-1].horiz_center() + points_list[idx_div2].horiz_center())
        
        dist_pair_closest_pair_strip = list(closest_pair_strip(cluster_list, mid, min_dist_pair[0]))
        
        min_num = round(dist_pair_closest_pair_strip[0]/min_dist_pair[0], 2)
        if min_num < 1:
            min_dist_pair = dist_pair_closest_pair_strip
                            
    return tuple(min_dist_pair)        

def fast_closest_pair1(cluster_list):  
    """
    input: takes a list of cluster objects
    output: returns a closest pair where the pair is represented by the tuple(dist, idx1, idx2)
     
    idx1 < idx2 where dist is the distance between the closest pair 
    cluster_list[idx1]and cluster_list[idx2]

    This function should implement the divide-and-conquer closest pair method   
    """
    
    points_list = list(cluster_list)
    num_of_points = len(points_list)
    
    if num_of_points <= 3:
        min_dist_pair = list(slow_closest_pair(cluster_list))
        
    else:
        
        idx_div2 = int(math.floor(num_of_points/2.0)) 
        
        points_list_left = list()
        for idx in range(idx_div2):
            points_list_left.append(points_list[idx]) 
        
        points_list_right = list()
        for idx in range(idx_div2, num_of_points):
            points_list_right.append(points_list[idx])
            
        min_dist_pair_left = list(fast_closest_pair(points_list_left))
        min_dist_pair_right = list(fast_closest_pair(points_list_right))
        
        min_dist_pair_right[1] = min_dist_pair_right[1] + idx_div2
        min_dist_pair_right[2] = min_dist_pair_right[2] + idx_div2
        
        
        if  min_dist_pair_left[0] <= min_dist_pair_right[0]:
            min_dist_pair = min_dist_pair_left
        #including equal to condition
        else:
            min_dist_pair = min_dist_pair_right
            
        mid = 0.5*(points_list[idx_div2-1].horiz_center() + points_list[idx_div2].horiz_center())
        
        dist_pair_closest_pair_strip = list(closest_pair_strip(cluster_list, mid, min_dist_pair[0]))
        
        if dist_pair_closest_pair_strip[0] < min_dist_pair[0]:
            min_dist_pair = dist_pair_closest_pair_strip
                            
    return tuple(min_dist_pair)        

###############################################################################

#########part-2################

def hierarchical_clustering(cluster_list, num_clusters):
    
    """
    input: Takes a list of Cluster objects and applies hierarchical clustering 
    as described in the pseudo-code HierarchicalClustering
    clustering process should proceed until num_clusters remain
    output: returns this list of clusters
    """
    
    num_of_points = len(cluster_list)
    
    #initialize n clusters
    points_list = list(cluster_list)
    points_list.sort(key=lambda cluster: cluster.horiz_center())    
        
    while num_of_points > num_clusters:
        points_list.sort(key=lambda cluster: cluster.horiz_center())
        min_dist_pair = fast_closest_pair1(points_list)
        points_list[min_dist_pair[1]].merge_clusters(points_list[min_dist_pair[2]])
        points_list.remove(points_list[min_dist_pair[2]])
        num_of_points = len(points_list)      
    return points_list


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    input: a list of Cluster objects, 
    num_clusters counties with the largest populations
    num_iterations of k-means clustering 
    output: list of clusters
    
    """
    cls_lst = list(cluster_list)
    k_centers = []
    nodelist_pop = list(cls_lst)
    nodelist_pop.sort(key=lambda cluster: cluster.total_population(), reverse=True)

    for idx in range(num_clusters):
        k_centers.append(alg_cluster.Cluster(set([]), nodelist_pop[idx].horiz_center(), nodelist_pop[idx].vert_center(), nodelist_pop[idx].total_population(), 0))

    for idx in range(num_iterations):
        
        kmeans_list = []
        idx2 = num_clusters
        while idx2 != 0:
            kmeans_list.append(alg_cluster.Cluster(set([]), 0, 0, 0, 0))
            idx2 -= 1
            
        for each in cls_lst:
            min_dist = float("inf")
            center_pos = 0
            for center in k_centers:
                dist = each.distance(center)
                if dist < min_dist:
                    min_dist = dist
                    center_pos = k_centers.index(center)

            kmeans_list[center_pos].merge_clusters(each)

        k_centers = list(kmeans_list)

    return kmeans_list
        
            
            
        
        
        
        
     









