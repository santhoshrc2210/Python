#http://www.codeskulptor.org/#user47_oaWxNL0AJg_0.py
"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """

    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score
    """
    score=[]
    for idx in hand:
        val_die=hand.count(idx)
        score.append(val_die*idx)

    return max(score)

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcomes=range(1,num_die_sides+1)
    seq_gen=gen_all_sequences(outcomes,num_free_dice)
    seq_score=0
    for seq in seq_gen:
        seq_score+=score(held_dice+seq)

    expected_value=float(seq_score)/len(seq_gen)
    return expected_value


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    #generate sequence for all indices
    dummy_lst=range(len(hand))
    answer_set = set([()])
    for dummy_idx in range(len(hand)) :
        temp_set = set([()])
        for partial_sequence in answer_set:
            for item in dummy_lst:
                new_sequence = list(partial_sequence)
                if item not in new_sequence:
                    new_sequence.append(item)
                    new_sequence.sort()
                    temp_set.add(tuple(new_sequence))
        answer_set = temp_set

    #answer_set contains all the list indices of outcome
    #use the list indices to plug in values
    answer_lst=list(answer_set)
    idx=1
    ans_set = set([()])
    dum_set = set([()])
    while idx<len(answer_lst):
        temp_tuple=answer_lst[idx]
        idx+=1
        temp_lst=[]
        for idx_1 in range(0,len(temp_tuple)):
            temp_lst.append(hand[temp_tuple[idx_1]])
        dum_set.add(tuple(temp_lst))
    ans_set=dum_set
    return ans_set


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    score_lst=[]
    possible_hands=gen_all_holds(hand)
    for each_hand in possible_hands:
        num_free_dice=len(hand)-len(each_hand)
        obt_score=expected_value(each_hand, num_die_sides, num_free_dice)
        score_lst.append(obt_score)
    #find max score and the index corresponding to that
    max_score=max(score_lst)
    idx=score_lst.index(max_score)
    possible_hands_lst=list(possible_hands)
    temp_lst=[]
    temp_lst.append(max_score)
    temp_lst.append(possible_hands_lst[idx])
    ans_tuple=tuple(temp_lst)
    return ans_tuple


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1,1,1,5,6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score


run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
