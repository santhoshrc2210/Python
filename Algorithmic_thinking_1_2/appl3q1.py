

"""
Cluster class for Module 3
"""

import math

##################################################################################
class Cluster:
    """
    Class for creating and merging clusters of counties
    """
    
    def __init__(self, fips_codes, horiz_pos, vert_pos, population, risk):
        """
        Create a cluster based the models a set of counties' data
        """
        self._fips_codes = fips_codes
        self._horiz_center = horiz_pos
        self._vert_center = vert_pos
        self._total_population = population
        self._averaged_risk = risk
        
        
    def __repr__(self):
        """
        String representation assuming the module is "alg_cluster".
        """
        rep = "alg_cluster.Cluster("
        rep += str(self._fips_codes) + ", "
        rep += str(self._horiz_center) + ", "
        rep += str(self._vert_center) + ", "
        rep += str(self._total_population) + ", "
        rep += str(self._averaged_risk) + ")"
        return rep


    def fips_codes(self):
        """
        Get the cluster's set of FIPS codes
        """
        return self._fips_codes
    
    def horiz_center(self):
        """
        Get the averged horizontal center of cluster
        """
        return self._horiz_center
    
    def vert_center(self):
        """
        Get the averaged vertical center of the cluster
        """
        return self._vert_center
    
    def total_population(self):
        """
        Get the total population for the cluster
        """
        return self._total_population
    
    def averaged_risk(self):
        """
        Get the averaged risk for the cluster
        """
        return self._averaged_risk
   
        
    def copy(self):
        """
        Return a copy of a cluster
        """
        copy_cluster = Cluster(set(self._fips_codes), self._horiz_center, self._vert_center,
                               self._total_population, self._averaged_risk)
        return copy_cluster


    def distance(self, other_cluster):
        """
        Compute the Euclidean distance between two clusters
        """
        vert_dist = self._vert_center - other_cluster.vert_center()
        horiz_dist = self._horiz_center - other_cluster.horiz_center()
        return math.sqrt(vert_dist ** 2 + horiz_dist ** 2)
        
    def merge_clusters(self, other_cluster):
        """
        Merge one cluster into another
        The merge uses the relatively populations of each
        cluster in computing a new center and risk
        
        Note that this method mutates self
        """
        if len(other_cluster.fips_codes()) == 0:
            return self
        else:
            self._fips_codes.update(set(other_cluster.fips_codes()))
 
            # compute weights for averaging
            self_weight = float(self._total_population)                        
            other_weight = float(other_cluster.total_population())
            self._total_population = self._total_population + other_cluster.total_population()
            self_weight /= self._total_population
            other_weight /= self._total_population
                    
            # update center and risk using weights
            self._vert_center = self_weight * self._vert_center + other_weight * other_cluster.vert_center()
            self._horiz_center = self_weight * self._horiz_center + other_weight * other_cluster.horiz_center()
            self._averaged_risk = self_weight * self._averaged_risk + other_weight * other_cluster.averaged_risk()
            return self

    def cluster_error(self, data_table):
        """
        Input: data_table is the original table of cancer data used in creating the cluster.
        
        Output: The error as the sum of the square of the distance from each county
        in the cluster to the cluster center (weighted by its population)
        """
        # Build hash table to accelerate error computation
        fips_to_line = {}
        for line_idx in range(len(data_table)):
            line = data_table[line_idx]
            fips_to_line[line[0]] = line_idx
        
        # compute error as weighted squared distance from counties to cluster center
        total_error = 0
        counties = self.fips_codes()
        for county in counties:
            line = data_table[fips_to_line[county]]
            singleton_cluster = Cluster(set([line[0]]), line[1], line[2], line[3], line[4])
            singleton_distance = self.distance(singleton_cluster)
            total_error += (singleton_distance ** 2) * singleton_cluster.total_population()
        return total_error

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
        
        if dist_pair_closest_pair_strip[0] < min_dist_pair[0]:
            min_dist_pair = dist_pair_closest_pair_strip
                            
    return tuple(min_dist_pair)                                            

##################################################################################                     
"""
application:3
Question:1
"""

import random

def gen_random_clusters(num_clusters):
    """
    that creates a list of clusters where each cluster in this list 
    corresponds to one randomly generated point in the square with 
    corners (±1,±1)
    """
    idx = num_clusters
    cluster_list = []
    while idx != 0:
        cluster_list.append(Cluster(set([]), random.uniform(-1, 1), 
                                                random.uniform(-1, 1), 0, 0))
        idx -= 1
    
    return cluster_list
        
##################################################################
#calculated dataset from desktop to plot in codeskultpor
#import time

#dataset_slow = {}
#dataset_fast = {}

#for size in range(2, 201):
    #start_time = time.perf_counter()
    #slow_closest_pair(gen_random_clusters(size))
    #end_time = time.perf_counter()
    #dataset_slow[size] = end_time-start_time
    
#for size in range(2, 201):
    #start_time = time.perf_counter()
    #fast_closest_pair(gen_random_clusters(size))
    #end_time = time.perf_counter()
    #dataset_fast[size] = end_time-start_time

#print(dataset_fast)
#print(dataset_slow)

###################################################################
import simpleplot

dataset_fast = {2: 9.514391422271729e-06, 3: 1.3535842299461365e-05, 4: 4.7223176807165146e-05, 5: 4.1177961975336075e-05, 6: 4.159891977906227e-05, 7: 6.44768588244915e-05, 8: 7.67996534705162e-05, 9: 7.286388427019119e-05, 10: 0.00010584527626633644, 11: 7.126713171601295e-05, 12: 7.484806701540947e-05, 13: 0.00010124268010258675, 14: 0.00010967021808028221, 15: 0.00014380412176251411, 16: 0.00012269895523786545, 17: 0.00015787500888109207, 18: 0.0001763729378581047, 19: 0.000157209113240242, 20: 0.00016221310943365097, 21: 0.0001708017662167549, 22: 0.0001660538837313652, 23: 0.0001702108420431614, 24: 0.00018266262486577034, 25: 0.0002057282254099846, 26: 0.00021999794989824295, 27: 0.00023889308795332909, 28: 0.0002627372741699219, 29: 0.00024404097348451614, 30: 0.00025281962007284164, 31: 0.00033100880682468414, 32: 0.0003223586827516556, 33: 0.0002963081933557987, 34: 0.00031134486198425293, 35: 0.0003332211636006832, 36: 0.0003496119752526283, 37: 0.00039554620161652565, 38: 0.00032636383548378944, 39: 0.0003653261810541153, 40: 0.0003858087584376335, 41: 0.00036088330671191216, 42: 0.00031813187524676323, 43: 0.00038804300129413605, 44: 0.00038721784949302673, 45: 0.0003639012575149536, 46: 0.0004367963410913944, 47: 0.0004108077846467495, 48: 0.00040425313636660576, 49: 0.0004267408512532711, 50: 0.00038746418431401253, 51: 0.0004030149430036545, 52: 0.00047812191769480705, 53: 0.0004975581541657448, 54: 0.00048255501314997673, 55: 0.0006136479787528515, 56: 0.0005584000609815121, 57: 0.0005637058056890965, 58: 0.0005853921175003052, 59: 0.0005385596305131912, 60: 0.0006448039785027504, 61: 0.0006016888655722141, 62: 0.0006028730422258377, 63: 0.0006284061819314957, 64: 0.0006466810591518879, 65: 0.000689149834215641, 66: 0.0006540222093462944, 67: 0.0006639389321208, 68: 0.0006742752157151699, 69: 0.0007169661112129688, 70: 0.0006745890714228153, 71: 0.0006717867217957973, 72: 0.0007321899756789207, 73: 0.0007143882103264332, 74: 0.0007154759950935841, 75: 0.0006890306249260902, 76: 0.000761610921472311, 77: 0.0007351767271757126, 78: 0.0007564439438283443, 79: 0.0007938388735055923, 80: 0.0007465779781341553, 81: 0.0007721981965005398, 82: 0.0007376582361757755, 83: 0.000780831091105938, 84: 0.000854977872222662, 85: 0.0008206870406866074, 86: 0.0008051949553191662, 87: 0.0007776911370456219, 88: 0.0008294046856462955, 89: 0.0008712890557944775, 90: 0.0008492632769048214, 91: 0.0008906340226531029, 92: 0.0009251120500266552, 93: 0.0008214199915528297, 94: 0.0008628997020423412, 95: 0.0008682790212333202, 96: 0.0008305218070745468, 97: 0.0009664949029684067, 98: 0.0009789946489036083, 99: 0.0009181690402328968, 100: 0.0009460239671170712, 101: 0.0009561739861965179, 102: 0.0009741331450641155, 103: 0.0009703510440886021, 104: 0.0009981351904571056, 105: 0.0010154559276998043, 106: 0.000992010347545147, 107: 0.0010986300185322762, 108: 0.001028846949338913, 109: 0.0010761930607259274, 110: 0.0010567777790129185, 111: 0.0011054310016334057, 112: 0.0010668369941413403, 113: 0.0010424219071865082, 114: 0.0011492511257529259, 115: 0.0012003788724541664, 116: 0.0011687008664011955, 117: 0.0012075710110366344, 118: 0.001247212290763855, 119: 0.0012297360226511955, 120: 0.0012360080145299435, 121: 0.0012707910500466824, 122: 0.0012498958967626095, 123: 0.0013396362774074078, 124: 0.0013234429061412811, 125: 0.0013811341486871243, 126: 0.0013301712460815907, 127: 0.001376353669911623, 128: 0.0013237250968813896, 129: 0.0014008032158017159, 130: 0.0014120512641966343, 131: 0.0013872859999537468, 132: 0.0015053818933665752, 133: 0.0013284417800605297, 134: 0.001297137700021267, 135: 0.0014397799968719482, 136: 0.0014261389151215553, 137: 0.0013885358348488808, 138: 0.0013502282090485096, 139: 0.0014430340379476547, 140: 0.0015262030065059662, 141: 0.0014194580726325512, 142: 0.0016172430478036404, 143: 0.0014925538562238216, 144: 0.001364374067634344, 145: 0.0016346760094165802, 146: 0.001433372963219881, 147: 0.0015682931989431381, 148: 0.0015377211384475231, 149: 0.0014823349192738533, 150: 0.0014603547751903534, 151: 0.0015087262727320194, 152: 0.001495238859206438, 153: 0.0016098893247544765, 154: 0.0015765298157930374, 155: 0.0016348352655768394, 156: 0.0014522438868880272, 157: 0.001584113109856844, 158: 0.0016011199913918972, 159: 0.0015118741430342197, 160: 0.0015157987363636494, 161: 0.0016768448986113071, 162: 0.0015966640785336494, 163: 0.0016369447112083435, 164: 0.0016049430705606937, 165: 0.0016370629891753197, 166: 0.001544096041470766, 167: 0.0016219187527894974, 168: 0.001645970158278942, 169: 0.001741382759064436, 170: 0.001716582104563713, 171: 0.0016570859588682652, 172: 0.001610341016203165, 173: 0.0018545091152191162, 174: 0.0016460530459880829, 175: 0.0017188666388392448, 176: 0.0018395851366221905, 177: 0.0016933879815042019, 178: 0.0018096989952027798, 179: 0.001767762005329132, 180: 0.0017197346314787865, 181: 0.0018072589300572872, 182: 0.0017164386808872223, 183: 0.0017507122829556465, 184: 0.0017348481342196465, 185: 0.001889580860733986, 186: 0.00183846615254879, 187: 0.0018326230347156525, 188: 0.0019385828636586666, 189: 0.0018958896398544312, 190: 0.0017167897894978523, 191: 0.0018199849873781204, 192: 0.0018424629233777523, 193: 0.0019471626728773117, 194: 0.0019107190892100334, 195: 0.0019583581015467644, 196: 0.0019094021990895271, 197: 0.0018758983351290226, 198: 0.0019400008022785187, 199: 0.0020327982492744923, 200: 0.0020295060239732265}
dataset_slow = {2: 2.495432272553444e-05, 3: 1.588882878422737e-05, 4: 2.101389691233635e-05, 5: 2.754293382167816e-05, 6: 3.802496939897537e-05, 7: 4.950631409883499e-05, 8: 6.047682836651802e-05, 9: 7.562898099422455e-05, 10: 8.873920887708664e-05, 11: 0.0001078159548342228, 12: 0.00012577511370182037, 13: 0.00014481320977210999, 14: 0.00016800500452518463, 15: 0.0001901760697364807, 16: 0.00021460279822349548, 17: 0.00024216482415795326, 18: 0.0002698455937206745, 19: 0.00029794638976454735, 20: 0.0003279689699411392, 21: 0.000363876111805439, 22: 0.0003957841545343399, 23: 0.00044060777872800827, 24: 0.0004692929796874523, 25: 0.0005065207369625568, 26: 0.0005468246527016163, 27: 0.0005848361179232597, 28: 0.0006103022024035454, 29: 0.0006618266925215721, 30: 0.0007145390845835209, 31: 0.0007432540878653526, 32: 0.0007957662455737591, 33: 0.0008424539119005203, 34: 0.0008913506753742695, 35: 0.0009704749099910259, 36: 0.001030349638313055, 37: 0.0010860832408070564, 38: 0.0011419807560741901, 39: 0.0012078001163899899, 40: 0.0012629982084035873, 41: 0.001324955839663744, 42: 0.0014099813997745514, 43: 0.0014558429829776287, 44: 0.0015323520638048649, 45: 0.0016031819395720959, 46: 0.0016646552830934525, 47: 0.0017365948297083378, 48: 0.0018141129985451698, 49: 0.0019008642993867397, 50: 0.0019643898122012615, 51: 0.0020458498038351536, 52: 0.00211885292083025, 53: 0.0022121057845652103, 54: 0.0022346070036292076, 55: 0.0022963699884712696, 56: 0.0023837299086153507, 57: 0.0025425138883292675, 58: 0.002630497794598341, 59: 0.0027278242632746696, 60: 0.0028120637871325016, 61: 0.002889879047870636, 62: 0.0030034128576517105, 63: 0.0030977106653153896, 64: 0.003235260955989361, 65: 0.0032321573235094547, 66: 0.0034110452979803085, 67: 0.0034993658773601055, 68: 0.0036067827604711056, 69: 0.003717471845448017, 70: 0.0038329092785716057, 71: 0.003933589905500412, 72: 0.004057544749230146, 73: 0.004168921150267124, 74: 0.004292212892323732, 75: 0.004291926044970751, 76: 0.00436590937897563, 77: 0.0045348238199949265, 78: 0.004768377169966698, 79: 0.004891633987426758, 80: 0.0049203368835151196, 81: 0.004979725927114487, 82: 0.005250251851975918, 83: 0.005366744939237833, 84: 0.0054785218089818954, 85: 0.005613360088318586, 86: 0.005751335062086582, 87: 0.005879072938114405, 88: 0.006020721979439259, 89: 0.006072368007153273, 90: 0.006148943677544594, 91: 0.006428936962038279, 92: 0.006578659638762474, 93: 0.006716572679579258, 94: 0.00685182074084878, 95: 0.007009585853666067, 96: 0.007160861976444721, 97: 0.00730990432202816, 98: 0.007460710592567921, 99: 0.007590570952743292, 100: 0.0076688919216394424, 101: 0.007799664977937937, 102: 0.007983780931681395, 103: 0.00813654763624072, 104: 0.00836521526798606, 105: 0.008572475053369999, 106: 0.008718752767890692, 107: 0.008714376017451286, 108: 0.009032931178808212, 109: 0.009198862127959728, 110: 0.009354579728096724, 111: 0.009528154972940683, 112: 0.009662977885454893, 113: 0.009979523252695799, 114: 0.010059729218482971, 115: 0.010237852111458778, 116: 0.010401086881756783, 117: 0.010594024322926998, 118: 0.010776834096759558, 119: 0.010946372989565134, 120: 0.011149398982524872, 121: 0.011322905775159597, 122: 0.011511122342199087, 123: 0.011694726999849081, 124: 0.011904920917004347, 125: 0.012079028878360987, 126: 0.012306961230933666, 127: 0.012510502710938454, 128: 0.012678936123847961, 129: 0.012889477889984846, 130: 0.013102775905281305, 131: 0.013409907929599285, 132: 0.013745157979428768, 133: 0.013964757788926363, 134: 0.014166140928864479, 135: 0.014312832150608301, 136: 0.014610357582569122, 137: 0.014817126095294952, 138: 0.01504133315756917, 139: 0.01522019412368536, 140: 0.015467120800167322, 141: 0.015678186900913715, 142: 0.01600682782009244, 143: 0.01613188488408923, 144: 0.0163474939763546, 145: 0.016667619347572327, 146: 0.016890473198145628, 147: 0.017141432035714388, 148: 0.01722985226660967, 149: 0.01730801211670041, 150: 0.017695743590593338, 151: 0.018008175771683455, 152: 0.01823895378038287, 153: 0.01844853674992919, 154: 0.018760602455586195, 155: 0.018959551118314266, 156: 0.01912287389859557, 157: 0.01943007158115506, 158: 0.019689087755978107, 159: 0.01996541488915682, 160: 0.020089543890208006, 161: 0.020438022911548615, 162: 0.020673853810876608, 163: 0.021191160194575787, 164: 0.021372993011027575, 165: 0.021564451046288013, 166: 0.021801420021802187, 167: 0.02184081496670842, 168: 0.022369381971657276, 169: 0.02263556607067585, 170: 0.022869248874485493, 171: 0.023206232115626335, 172: 0.023401515558362007, 173: 0.023621863219887018, 174: 0.023825615644454956, 175: 0.02404675306752324, 176: 0.024450214579701424, 177: 0.02467013383284211, 178: 0.02499203383922577, 179: 0.025303318165242672, 180: 0.025518001057207584, 181: 0.0259865359403193, 182: 0.02612632093951106, 183: 0.026362427044659853, 184: 0.026213915087282658, 185: 0.026518510654568672, 186: 0.026854089926928282, 187: 0.026899287942796946, 188: 0.027321777772158384, 189: 0.02797419112175703, 190: 0.028100327122956514, 191: 0.028155933134257793, 192: 0.02839522436261177, 193: 0.028845936991274357, 194: 0.029161545913666487, 195: 0.02959233010187745, 196: 0.02973334677517414, 197: 0.02997785108163953, 198: 0.03051075479015708, 199: 0.030548884067684412, 200: 0.03096407325938344} 

simpleplot.plot_lines('Running time of slow vs fast closest pairs in Desktop', 800, 600, 
                      'Number of initial clusters', 'Running time in seconds', 
                      [dataset_slow, dataset_fast ], True, 
                      ['slow_closest_pair', 'fast_closest_pair'])










