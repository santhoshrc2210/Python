#https://py2.codeskulptor.org/#user48_qMByWEBhas_6.py
#passed owltest and mostly works but has some bugs need to work on it some more
"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods
    def position_zero_tile(self,target_row,target_col):
        '''
        move zero at target_row,target_col to position at target tile
        '''
        target_tile_pos=self.current_position(target_row, target_col)
        #move zero to this position
        no_u_mv=target_row-target_tile_pos[0]
        no_s_mv=target_col-target_tile_pos[1]
        move_string=''
        move_string+='u'*no_u_mv
        if no_s_mv>0:
        #move left           
            move_string+='l'*no_s_mv
        elif no_s_mv<=0:
            no_r=-1*no_s_mv
            #move right            
            move_string+='r'*no_r
        return move_string                
        
    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """  
        cond1=False
        cond2=False
        cond3=False
        #Tile zero is positioned at i,j
        if self._grid[target_row][target_col]==0:
            cond1=True
        
        #All tiles in rows i+1 or below are positioned at their solved location
        list_cond_2=[]
        solved_board=[]
        if target_row+1<self._height:    
            for row in range( target_row+1, self._height):
                for col in range(self._width):
                    list_cond_2.append(self._grid[row][col])
                    solved_board.append(col + self._width * row)
            if list_cond_2==solved_board:
                cond2=True
        elif target_row+1==self._height:
            cond2=True
        
        #All tiles in row i to the right of position (i,j) 
        #are positioned at their solved location.
        list_cond_3=[]
        solved_board_1=[]
        if target_col+1<self._width:
            for col in range(target_col+1,self._width):
                list_cond_3.append(self._grid[target_row][col])
                solved_board_1.append(col + self._width * target_row)
            if list_cond_3==solved_board_1:
                cond3=True
        elif target_col+1==self._width:
            cond3=True
        
        #end of function
        if cond1 and cond2 and cond3:
            return True
        else:
            return False

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, target_col)
        target_tile_pos=self.current_position(target_row, target_col)
        no_u_mv=target_row-target_tile_pos[0]
        no_s_mv=target_col-target_tile_pos[1]
        #move the zero which is at target_row,target_col to position of target tile
        move_string=self.position_zero_tile(target_row,target_col) 
        #case1:target tile has same x cordinates as i
        
        if no_u_mv==1 and no_s_mv==0:
            move_string+='ld'
        elif no_u_mv>1 and no_s_mv==0:
            move_string+='lddru'*(no_u_mv-1)
            move_string+='ld'
        
        #case2:target tile is i to the left of zero tile
        elif no_u_mv==0 and no_s_mv==1:
            move_string='l'
        elif no_u_mv==0 and no_s_mv>1:
            #moving the target tile one position right with every iteration
            move_string+='urrdl'*(no_s_mv-1)
        elif no_u_mv>0 and no_s_mv>=1:
            #moving the target tile one position down            
            move_string+='druld'*no_u_mv
            #keep moving to the right till y co-ordinates match
            #moving the target tile one position right with every iteration
            move_string+='urrdl'*(no_s_mv-1)                                  
        
        #case3:target tile is to right of the zero tile
        elif no_u_mv>0 and no_s_mv<0:
            no_r_mv=-1*no_s_mv
            #first move the target tile left such that it has same y co-ordinates
            if no_u_mv>1:
                move_string+='dllur'*(no_r_mv-1)
            elif no_u_mv==1:
                move_string='ulldr'*(no_r_mv-1)
    
            #second move the target tile down to target location
            move_string+='dlurd'*(no_u_mv-1)
            move_string+='ullddruld'
                
                
        self.update_puzzle(move_string)
        assert self.lower_row_invariant(target_row, target_col-1)
        return move_string 

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0)
        move_string=''
        target_tile_pos=self.current_position(target_row, 0)        
        if target_tile_pos[0]==target_row-1 and target_tile_pos[1]==0:
            move_string='ur'
            #move zero tile to the end of i-1th row
            move_string+='r'*(self._width-2)
            self.update_puzzle(move_string)
            assert self.lower_row_invariant(target_row-1, self._width-1)
            return move_string
        #step1
        #Reposition the target tile to position (i−1,1) and the zero tile to position (i−1,0)
        #using a process similar to that of solve_interior_tile
        #zero tile is at (i,0)
        no_u_mv=target_row-target_tile_pos[0]
        no_s_mv=target_tile_pos[1]
        #move the zero which is at target_row,target_col to position of target tile
        #case1:target tile has is in col 0 and not in target_row-1        
        if no_u_mv>1 and no_s_mv==0:
            move_string=self.position_zero_tile(target_row,0)        
            move_string+='rddlu'*(no_u_mv-2)
            move_string+='rdl'
        #case2: target tile is in col>=1 in any row
        elif no_u_mv==1 and no_s_mv==1:
            move_string='ur'
        elif no_u_mv>1 and no_s_mv==1:
            move_string=self.position_zero_tile(target_row,0)        
            move_string+='l'
            move_string+='druld'*(no_u_mv-1)            
        elif no_u_mv>=1 and no_s_mv>1:
            #move target tile left 
            move_string=self.position_zero_tile(target_row,0)        
            move_string+='dlurd'*(no_u_mv-1)
            move_string+='ulldr'*(no_s_mv-2)
            move_string+='ulld'
        
        #step2 Then apply the move string for a 3×2 puzzle as described in problem #9 of 
        #the homework to bring the target tile into position (i,0),
        move_string+='ruldrdlurdluurddlur'
        
        #step3 Finally, conclude by moving tile zero to the right end of row i−1
        #zero tile is at (row-1,1)       
        move_string+='r'*(self._width-2)
        self.update_puzzle(move_string)
        
        assert self.lower_row_invariant(target_row-1, self._width-1)
        return move_string
        

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        list_cond=[]
        solved_board=[]
        cond_1=False
        cond_2=False
        if self._grid[0][target_col]==0:
                cond_1=True
        #for (1,j) to end of board it is solved
        for row in range(1, self._height):
            for col in range(self._width):
                list_cond.append(self._grid[row][col])
                solved_board.append(col + self._width * row)
        #remove elements from row 1,col 0-(j-1)
        no_iter=target_col-1
        while no_iter>=0:
            list_cond.pop(0)
            solved_board.pop(0)
            no_iter-=1
        if list_cond==solved_board:
            cond_2=True 
        if cond_1 and cond_2:
            return True
        else:
            return False
        return False

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        #check wether tile zero is at (1,j)
        if self.lower_row_invariant(1, target_col):
            return True             
        return False

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        #need to work on this
        target_tile_pos=self.current_position(0, target_col)
        no_d_mv=target_tile_pos[0]
        no_l_mv=target_col-target_tile_pos[1] 
        move_string=''
        if no_l_mv==1 and no_d_mv==0:
            move_string='ld'
        elif no_l_mv==1 and no_d_mv==1:
            move_string='ld'
            move_string+='uldurdlurrdluldrruld'
        elif no_l_mv>1 and no_d_mv==0:
            move_string='l'*no_l_mv
            move_string+='drrul'*(no_l_mv-2)
            move_string+='dr'            
            move_string+='uldurdlurrdluldrruld'    
        elif no_l_mv>1 and no_d_mv>0:
            move_string+='d'*no_d_mv
            move_string+='l'*no_l_mv
            #moving target value right
            move_string+='urrdl'*(no_l_mv-2)
            #moving target value up
            move_string+='urd'
            move_string+='ruld'
         
        self.update_puzzle(move_string)
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        target_row=1
        assert self.row1_invariant(target_col)
        target_tile_pos=self.current_position(target_row, target_col)
        no_u_mv=target_row-target_tile_pos[0]
        no_s_mv=target_col-target_tile_pos[1]
        #move the zero which is at target_row,target_col to position of target tile
        move_string=self.position_zero_tile(target_row,target_col) 
        #case1:target tile has same x cordinates as i
        
        if no_u_mv==1 and no_s_mv==0:
            move_string+='ld'       
        #case2:target tile is i to the left of zero tile
        elif no_u_mv==0 and no_s_mv==1:
            move_string+=''
        elif no_u_mv==0 and no_s_mv>1:
            #moving the target tile one position right with every iteration
            move_string+='urrdl'*(no_s_mv-1)
        elif no_u_mv>0 and no_s_mv>=1:
            #moving the target tile one position down            
            move_string+='druld'*no_u_mv
            #keep moving to the right till y co-ordinates match
            #moving the target tile one position right with every iteration
            move_string+='urrdl'*(no_s_mv-1)                                  
        
        #case3:target tile is to right of the zero tile
        elif no_u_mv>0 and no_s_mv<0:
            #first move the target tile left such that it has same y co-ordinates
            pass    
            #second move the target tile down to target location
        #dont understand this move
        move_string+='ur'                                                       
        self.update_puzzle(move_string)
        return move_string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        #put zero in 0,0 and there are two situations which are solvable
        assert self.row1_invariant(1)        
        #move zero
        #move_string='ld'
        move_string=''
        puzzle_copy=self.clone()
        move_str='lu'
        puzzle_copy.update_puzzle(move_str)
        one_pos=puzzle_copy.get_number(0,1)
        two_pos=puzzle_copy.get_number(1,0)
        solved_two_pos=self._width
        three_pos=puzzle_copy.get_number(1,1)
        solved_three_pos=1 + self._width
        if one_pos==1 and two_pos==solved_two_pos and three_pos==solved_three_pos:
            move_string='lu'
        elif one_pos==solved_two_pos and two_pos==solved_three_pos and three_pos==1:
            move_string='lurdlu'            
        elif one_pos==solved_three_pos and two_pos==1 and three_pos==solved_two_pos:             
            move_string='ludrul'
           
        self.update_puzzle(move_string)
        return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        if self.lower_row_invariant(0, 0):
            return ""
        #find the pos zero needs to be moved to for a partially solved board
        move_string = ""
        width = self.get_width()
        height = self.get_height()
        
        if self.get_number(height - 1, width - 1) != 0:
            for row in range(height):
                for col in range(width):
                    if self.get_number(row, col) == 0:
                        zero_row = row
                        zero_col = col
                        break
            move_string += "d" * (height - 1 - zero_row)
            move_string += "r" * (width - 1 - zero_col)
            
        self.update_puzzle(move_string)
        #figure out when a solve function should be used and where to start
        for row in range(height-1,1,-1):
            for col in range(width-1,-1,-1):
                #when to use solve_interior_tile
                if col!=0:
                    move_string+=self.solve_interior_tile(row,col)
                #when to use solve_col0_tile
                elif col==0 :
                    move_string+=self.solve_col0_tile(row)
        
        for col in range(width-1,1,-1):          
            move_string+=self.solve_row1_tile(col)
            move_string+=self.solve_row0_tile(col)
                
        move_string += self.solve_2x2()                
        return move_string
    
# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4)) 














                              
