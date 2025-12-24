#https://py2.codeskulptor.org/#user48_4uLhH6hNEH_2.py
"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    list2=list(list1)  
    for idx in list1:
        reps=list2.count(idx)
        while reps>1:
            print list2
            list2.remove(idx)
            reps-=1
    return list2 

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    list_and=[]
    list_2=list(list2)
    for ele in list1:
        if ele in list_2:
            list_2.remove(ele)
            list_and.append(ele)
    return list_and

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """   
    list_or=list(list1)               
    list_or.extend(list2)
    #list_and=intersect(list1,list2)
    #for i in list_and:
        #list_or.remove(i)
        
    #sorting the list in ascending order
    list_dummy=list(list_or)
    list_4=[]
    idx=0
    while idx<len(list_or):
        min_ele=min(list_dummy)
        list_4.append(min_ele)
        list_dummy.remove(min_ele)
        idx+=1
    return list_4 


def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1)<=2:
        l_th=len(list1)
        return merge(list1[0:l_th/2],list1[l_th/2:])
    else:
        l_th=len(list1)
        a_idx=merge_sort(list1[0:l_th/2])
        b_idx=merge_sort(list1[l_th/2:])
        return merge(a_idx,b_idx)

# Function to generate all strings for the word wrangler game
def lst_to_str(list1):
    """
    convert a list to a string
    """
    f_str=''
    for ele in list1:
        f_str+=ele
    return f_str
def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if word=='':
        return ['']
    
    else:
        #step1
        first=word[0]
        rest=word[1:]
        #step2 generate strings out of rest
        rest_strings=gen_all_strings(rest)
        #step3
        comb=[]        
        for rest_str in rest_strings:
            temp_comb=list(rest_str)
            for idx in range(len(rest_str)+1):
                temp_comb.insert(idx,first)
                temp_comb=lst_to_str(temp_comb)
                comb.append(temp_comb)
                temp_comb=list(rest_str)
        return rest_strings+comb
                  
# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    online_file = urllib2.urlopen(url)
    return [word[:-1] for word in online_file]

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()

    
    
