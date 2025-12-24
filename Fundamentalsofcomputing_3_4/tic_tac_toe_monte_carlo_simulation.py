#http://www.codeskulptor.org/#user47_MoKYJEzGdp_41.py
"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100       # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the machine player
SCORE_OTHER = 1.0   # Score for squares played by the gui player

# Add your functions here.
def mc_trial(board,player):
    '''
    Plays a game taking the current state of the board and the
    next player as inputs
    '''
    current_player=player

    empty_sq=board.get_empty_squares()
    numbers=range(len(empty_sq))
    random.shuffle(numbers)

    for ind_1 in numbers:
        len_win=board.get_empty_squares()
        if len(len_win)<=4:
            var_a=board.check_win()
            if var_a==None:
                conv_lst=list(empty_sq[ind_1])
                board.move(conv_lst[0],conv_lst[1],current_player)
                current_player=provided.switch_player(player)
        elif len(len_win)>4:
            conv_lst=list(empty_sq[ind_1])
            board.move(conv_lst[0],conv_lst[1],current_player)
            current_player=provided.switch_player(player)

def mc_update_scores(scores,board,player):
    '''
    inputs are a scores grid, a completed board
    and the machine player. Updates the scores board
    accordingly
    '''

    other_player=provided.switch_player(player)

    mach_player_lst=[]
    other_player_lst=[]
    board_dim=board.get_dim()

    for row in range(board_dim):
        for col in range(board_dim):
            if board.square(row,col)==player:
                co_ord=(row,col)
                mach_player_lst.append(co_ord)
            elif board.square(row,col)==other_player:
                co_ord=(row,col)
                other_player_lst.append(co_ord)

    if board.check_win()==player:
        for ind_1 in range(len(mach_player_lst)):
                temp_list=list(mach_player_lst[ind_1])
                scores[temp_list[0]][temp_list[1]]+=SCORE_CURRENT
        for jnd_1 in range(len(other_player_lst)):
                temp_list_1=list(other_player_lst[jnd_1])
                scores[temp_list_1[0]][temp_list_1[1]]+=-SCORE_OTHER
    elif board.check_win()==other_player:
        for ind_1 in range(len(mach_player_lst)):
                temp_list=list(mach_player_lst[ind_1])
                scores[temp_list[0]][temp_list[1]]+=-SCORE_CURRENT
        for jnd_1 in range(len(other_player_lst)):
                temp_list_1=list(other_player_lst[jnd_1])
                scores[temp_list_1[0]][temp_list_1[1]]+=SCORE_OTHER
    elif board.check_win()==provided.DRAW:
        pass


def get_best_move(board, scores):
    '''
    Takes a board in play and grid of scores and returns
    the empty square with the maximum score

    '''

    lst_empty_sq=board.get_empty_squares()

    if len(lst_empty_sq)==0:
        return

    final_scores=[]
    co_ord=[]
    for ind_1 in range(len(lst_empty_sq)):
        temp_list=list(lst_empty_sq[ind_1])
        final_scores.append(scores[temp_list[0]][temp_list[1]])

    for ind_2 in range(len(lst_empty_sq)):
        if max(final_scores)==final_scores[ind_2]:
            co_ord.append(lst_empty_sq[ind_2])

    fut_move = co_ord[random.randrange(len(co_ord))]
    return fut_move

def mc_move(board, player, trials):
    '''
    inputs are board in play, machine player,
    and  number of trials to run. Returns a move for the
    machine player in the form of a (row, col) tuple
    '''
    board_dim=board.get_dim()
    scores=[[0 + 0 for col in range(board_dim)]
                           for row in range(board_dim)]

    for trial_num in range(trials):
        dum_board = board.clone()
        mc_trial(dum_board, player)
        mc_update_scores(scores, dum_board, player)

    return get_best_move(board, scores)

# Test game with the console or the GUI.  Uncomment whichever
# you prefer.  Both should be commented out when you submit
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
