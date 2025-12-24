"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    num_zeros= len(line)
    result_list=[]
    result_list2=[]
    #creating a list with 0's same length as input list
    for ind_1 in range(num_zeros):
        result_list.append(0)
        result_list2.append(0)
    #creating a list with non-zero inputs of the input list
    jnd_1=0
    for ind_1 in range(len(line)):
        if line[ind_1]!=0:
            result_list[jnd_1]=line[ind_1]
            jnd_1+=1
    #print result_list
    #merging two tiles to create sum
    for ind_3 in range(len(line)-1):
        if result_list[ind_3]==result_list[ind_3+1]:
            result_list[ind_3]*=2
            result_list[ind_3+1]=0
    #print result_list
    #repeating step 1 for result_list
    knd_1=0
    for ind_4 in range(len(result_list)):
        if result_list[ind_4]!=0:
            result_list2[knd_1]=result_list[ind_4]
            knd_1+=1
    return result_list2
