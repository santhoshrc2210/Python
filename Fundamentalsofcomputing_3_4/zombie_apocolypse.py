"""
Student portion of Zombie Apocalypse mini-project
"""
#http://www.codeskulptor.org/#user47_hyc2NxJWBx_7.py
import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None,
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)
        else:
            self._human_list = []

    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []


    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row,col))

    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)

    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie_cord in self._zombie_list:
            yield zombie_cord

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row,col))

    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)

    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human_cord in self._human_list:
            yield human_cord

    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        visited = [[EMPTY for dummy_col in range(self._grid_width)]
                       for dummy_row in range(self._grid_height)]
        distance_field = [[self._grid_width * self._grid_height for dummy_col in range(self._grid_width)]
                       for dummy_row in range(self._grid_height)]
        boundary = poc_queue.Queue()


        if entity_type == ZOMBIE:
            for item in self.zombies():
                boundary.enqueue(item)
        if entity_type == HUMAN:
            for item in self.humans():
                boundary.enqueue(item)
        for cell in boundary:
            visited[cell[0]][cell[1]] = FULL
            distance_field[cell[0]][cell[1]] = 0
        while len(boundary) != 0:
            current_cell = boundary.dequeue()
            neighbors = self.four_neighbors (current_cell[0], current_cell[1])
            for neighbor in neighbors:
                if self.is_empty(neighbor[0], neighbor[1]):
                    if visited[neighbor[0]][neighbor[1]]==EMPTY:
                        visited[neighbor[0]][neighbor[1]]=FULL
                        boundary.enqueue(neighbor)
                        distance_field[neighbor[0]][neighbor[1]] =distance_field[current_cell[0]][current_cell[1]] + 1

        return distance_field


    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        h_list=self._human_list
        idx_h_lst=0
        for human in h_list:
            neighbors=self.eight_neighbors(human[0],human[1])
            distance_list=[]
            for neighbor in neighbors:
                if self.is_empty(neighbor[0],neighbor[1]):
                    distance_list.append(zombie_distance_field[neighbor[0]][neighbor[1]])
                else:
                    distance_list.append(0)
            max_dist=max(distance_list)
            idx=distance_list.index(max_dist)
            self._human_list[idx_h_lst]= neighbors[idx]
            idx_h_lst+=1

    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        z_list=self._zombie_list
        #print z_list
        idx_z_lst=0
        for zombie in z_list:
            neighbors=self.four_neighbors(zombie[0],zombie[1])
            distance_list=[]
            if zombie in self._human_list:
                continue
            else:
                for neighbor in neighbors:
                    if self.is_empty(neighbor[0],neighbor[1]):
                        distance_list.append(human_distance_field[neighbor[0]][neighbor[1]])
                    else:
                        distance_list.append(self._grid_width * self._grid_height)
                #print neighbors
                #print distance_list
                min_dist=min(distance_list)
                idx=distance_list.index(min_dist)
                self._zombie_list[idx_z_lst]= neighbors[idx]
                #print self._zombie_list
                idx_z_lst+=1

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40))
#obj = Apocalypse(3, 3, [], [(1, 1)], [(1, 1)])
#dist = [[2, 1, 2], [1, 0, 1], [2, 1, 2]]
#obj.move_zombies(dist)
