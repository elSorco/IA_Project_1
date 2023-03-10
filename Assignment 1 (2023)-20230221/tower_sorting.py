#!/usr/bin/env python
"""
Name of the author(s):
- Auguste Burlats <auguste.burlats@uclouvain.be>
"""
import time
import sys
from copy import deepcopy
from search import *


#################
# Problem class #
#################
class TowerSorting(Problem):

    # --------------------                  actions                                   -------------------------- #

    def actions(self, state):
        for i in range(state.number):
            for j in range(state.number):
                if(i != j):  
                    if(len(state.grid[j]) == 0 or len(state.grid[j])<state.size):
                        yield(i,j)
    


    # --------------------                  result                                    -------------------------- #
    

    def result(self, state, action):
        towerA,towerB = action 
        new_grid = deepcopy(state.grid)
        new_grid[towerB].append(new_grid[towerA].pop())
        return State(state.number, state.size, new_grid, f"Tower {towerA} to Tower {towerB}")
    

    
    # ----------------------------       goal_test  -------------------------------------------------------------#
    
    def goal_test(self, state):
        for i in range(state.number):
            if(len(state.grid[i])!=0 and (len(state.grid[i]) != state.size or len(set(state.grid[i])) != 1) ):
                return False
        return True
      

###############
# State class #
###############
class State:

    def __init__(self, number, size, grid, move="Init"):
        self.number = number
        self.size = size
        self.grid = grid
        self.move = move

    def __str__(self):
        s = self.move + "\n"
        for i in reversed(range(self.size)):
            for tower in self.grid:
                if len(tower) > i:
                    s += "".join(tower[i]) + " "
                else:
                    s += ". "
            s += "\n"
        return s


    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(str(self.grid))


######################
# Auxiliary function #
######################

def read_instance_file(filepath):
    with open(filepath) as fd:
        lines = fd.read().splitlines()

    number_tower, size_tower = tuple([int(i) for i in lines[0].split(" ")])
    initial_grid = [[] for i in range(number_tower)]
    for row in lines[1:size_tower+1]:
        elems = row.split(" ")
        for index in range(number_tower):
            if elems[index] != '.':
                initial_grid[index].append(elems[index])

    for tower in initial_grid:
        tower.reverse()

    return number_tower, size_tower, initial_grid


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: ./sort_tower.py <path_to_instance_file>")
    filepath = sys.argv[1]

    number, size, initial_grid = read_instance_file(filepath)

    init_state = State(number, size, initial_grid, "Init")
    problem = TowerSorting(init_state)
    # Example of search
    start_timer = time.perf_counter()
    #node, nb_explored, remaining_nodes = depth_first_tree_search(problem)
    node, nb_explored, remaining_nodes = breadth_first_graph_search(problem)
    end_timer = time.perf_counter()

    # Example of print
    path = node.path()

    for n in path:
        # assuming that the __str__ function of state outputs the correct format
        print(n.state)

    print("* Execution time:\t", str(end_timer - start_timer))
    print("* Path cost to goal:\t", node.depth, "moves")
    print("* #Nodes explored:\t", nb_explored)
    print("* Queue size at goal:\t",  remaining_nodes)


