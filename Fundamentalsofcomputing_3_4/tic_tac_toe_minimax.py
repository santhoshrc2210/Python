"""
Mini-max Tic-Tac-Toe Player
"""
#scoring part need to work on
#https://py2.codeskulptor.org/#user48_MJXxItTKOi_15.py
import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}
        
def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    current_player=player
    #check if game over:base case
    if board.check_win()==provided.PLAYERX:
        return SCORES[provided.PLAYERX],(-1, -1)
    elif board.check_win()==provided.PLAYERO:
        return SCORES[provided.PLAYERO],(-1, -1)
    elif board.check_win()==provided.DRAW:
        return SCORES[provided.DRAW],(-1, -1)
    else:
        list_posmvs=board.get_empty_squares()
        best_score=-1
        best_mv=(-1,-1)
        #make a move
        for posmv in list_posmvs:
            board_cpy=board.clone()
            board_cpy.move(posmv[0],posmv[1],current_player)
            res=mm_move(board_cpy,provided.switch_player(current_player))
            score =res[0] * SCORES[player]
            #scoring and returning best move
            if score==1:
                return res[0],posmv
            if score>=best_score:
                best_score=score
                best_mv=posmv
        return best_score*SCORES[player],best_mv        
                
            
            
def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(move_wrapper, 1, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
