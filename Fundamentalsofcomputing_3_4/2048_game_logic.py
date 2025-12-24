#http://www.codeskulptor.org/#user47_ziJ4sk6prE_63.py
"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
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

def traverse_grid(start_cell, direction, num_steps,grid):
        """
        Function that iterates through the cells in a grid
        in a linear direction

        Both start_cell is a tuple(row, col) denoting the
        starting cell

        direction is a tuple that contains difference between
        consecutive cells in the traversal
        """
        list1=[]
        for step in range(num_steps):
            row = start_cell[0] + step * direction[0]
            col = start_cell[1] + step * direction[1]
            list1.append(grid[row][col])
        return list1


def merged_grid(start_cell, direction, num_steps,line,grid):
    """
    Function that takes as input the merged list

    and puts back the values in order
    """

    for step in range(num_steps):
        row = start_cell[0] + step * direction[0]
        col = start_cell[1] + step * direction[1]
        grid[row][col]=line[step]

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._height=grid_height
        self._width=grid_width

        #calculating initial tiles for UP

        initial_tiles_up=[]
        ind_up=0
        while ind_up<self._width:
            initial_tiles_up.append((0,ind_up))
            ind_up+=1

       #calculating initial tiles for DOWN

        initial_tiles_dn=[]
        ind_dn=0
        while ind_dn<self._width:
            initial_tiles_dn.append((self._height-1,ind_dn))
            ind_dn+=1

        #calculating initial tiles for LEFT

        initial_tiles_lt=[]
        ind_lt=0
        while ind_lt<self._height:
            initial_tiles_lt.append((ind_lt,0))
            ind_lt+=1

        #calculating initial tiles for RIGHT

        initial_tiles_rt=[]
        ind_rt=0
        while ind_rt<self._height:
            initial_tiles_rt.append((ind_rt,self._width-1))
            ind_rt+=1

        self._initial_tiles={UP: initial_tiles_up,
                            DOWN: initial_tiles_dn,
                            LEFT: initial_tiles_lt,
                            RIGHT: initial_tiles_rt}
        self._tile=0
        self._grid = [[0 + 0 for col in range(self._width)]
                 for row in range(self._height)]

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 + 0 for col in range(self._width)]
                 for row in range(self._height)]

        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        grid_readable=""
        if(self._tile==1):
            grid_readable="\nwith "+str(self._tile)+" additional tile"
        elif(self._tile>1):
            grid_readable="\nwith "+str(self._tile)+" additional tile(s)"
        return '[%s]' % '\n'.join(str(row) for row in self._grid)+grid_readable

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        self._direction=direction
        #intializing to empty lists
        merged_list=[]
        temp_list=[]
        grid_change=False

        if self._direction==UP:
            for ind_grid in range(self._width):
                initial_tiles_up=self._initial_tiles[UP]
                temp_list=traverse_grid((initial_tiles_up[ind_grid]),(OFFSETS[UP]),self._height,self._grid)
                merged_list=merge(temp_list)
                if temp_list!=merged_list:
                    grid_change=True
                merged_grid((initial_tiles_up[ind_grid]),(OFFSETS[UP]),self._height,merged_list,self._grid)

        elif self._direction==DOWN:
            for ind_grid in range(self._width):
                initial_tiles_dn=self._initial_tiles[DOWN]
                temp_list=traverse_grid((initial_tiles_dn[ind_grid]),(OFFSETS[DOWN]),self._height,self._grid)
                merged_list=merge(temp_list)
                if temp_list!=merged_list:
                    grid_change=True
                merged_grid((initial_tiles_dn[ind_grid]),(OFFSETS[DOWN]),self._height,merged_list,self._grid)

        elif self._direction==LEFT:
            for ind_grid in range(self._height):
                initial_tiles_lt=self._initial_tiles[LEFT]
                temp_list=traverse_grid((initial_tiles_lt[ind_grid]),(OFFSETS[LEFT]),self._width,self._grid)
                merged_list=merge(temp_list)
                if temp_list!=merged_list:
                    grid_change=True
                merged_grid((initial_tiles_lt[ind_grid]),(OFFSETS[LEFT]),self._width,merged_list,self._grid)

        elif self._direction==RIGHT:
            for ind_grid in range(self._height):
                initial_tiles_rt=self._initial_tiles[RIGHT]
                temp_list=traverse_grid((initial_tiles_rt[ind_grid]),(OFFSETS[RIGHT]),self._width,self._grid)
                merged_list=merge(temp_list)
                if temp_list!=merged_list:
                    grid_change=True
                merged_grid((initial_tiles_rt[ind_grid]),(OFFSETS[RIGHT]),self._width,merged_list,self._grid)

        if (grid_change):
            self.new_tile()

    def check_empty_tile(self):
        """
        Check for Empty Tiles and return the
        positions
        """
        empty_tile_list=[]
        for row in range(self._width):
            for col in range(self._height):
                if(self._grid[col][row]==0):
                    empty_tile_list.append([col,row])

        return empty_tile_list

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        num=random.randint(1,10)
        if num==1:
            value=4
        else:
            value=2
        if(len(self.check_empty_tile())>0):
            [row,col]=random.choice(self.check_empty_tile())
            self._grid[row][col]=value
            self._tile+=1


    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col]=value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        val_grid_element=self._grid[row][col]
        return val_grid_element

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
