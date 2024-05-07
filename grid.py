#!/usr/bin/python
# -*- coding: utf-8 -*-



from __future__ import print_function
import numpy as np 
from PIL import Image
import struct
import sys
import os, fnmatch

###################### Load grid ############################

def load_grid(filename):
    """
    brief  : loads a grid
    param  : filename - STR name of the grid's ASCII dump
    return : grid     - LIST of coordinates of grid points (TUPLES)
             grid_x   - LIST of xs contained in the grid
             grid_y   - LIST of ys contained in the grid
    """
    
    file = open(filename, mode ='r')
    size = int(file.readline().strip())
    grid = []
    grid_x=[]
    grid_y=[]
    
    for i in range(size):
        x,y = file.readline().split()
        x,y = float(x), float(y)
        grid.append((x,y))
        if x not in grid_x : grid_x.append(x)
        if y not in grid_y : grid_y.append(y)
    file.close()
    return grid, grid_x, grid_y


###################### Grid correspondance ############################


def grid_correspondance(grid_1, grid_2, grid_2x, grid_2y):
    """
    brief   : Computes the list used to get corresponding data in the 2 simulations 
    param   : grid_1         - LIST of coordinates of grid points (TUPLES) of the reference simulation
              grid_2         - LIST of coordinates of grid points (TUPLES) of the other simulation
              grid_2x        - LIST of xs in the other simulation's grid
              grid_2y        - LIST of ys in the other simulation's grid
    return  : line1_to_line2 - LIST of LIST of 2nd simulation indexes and interpolation weights
                               corresponding to 1st simulation index
                               line1_to_line2[n] = [ (line_2, weight) ]
  """
    line1_to_line2 = []
    for line_1 in range (len(grid_1)):
    
        (x,y) = grid_1[line_1]
        
        if (x in grid_2x): 
            if (y in grid_2y):
                # (x,y) is also in grid_2
                line1_to_line2.append([(grid_2.index((x,y)), 1)])
                continue
            
            else :
                xs = [x]
                ind_y = grid_2y.append(y).sort().index(y)
                ys = [grid_2y[ind_y-1],grid_2y[ind_y+1]]
            
        elif (y in grid_2y):
            ys = [y]
            ind_x = grid_2x.append(x).sort().index(x)
            xs = [grid_2x[ind_x -1], grid_2x[ind_x +1]]
            
        else :
            ind_x = grid_2x.append(x).sort().index(x)
            xs = [grid_2x[ind_x -1], grid_2x[ind_x +1]]
            ind_y = grid_2y.append(y).sort().index(y)
            ys = [grid_2y[ind_y-1],grid_2y[ind_y+1]]
        
        
        # Create the list of corresponding indexes and weights 
        line_2 = []
        for x_2 in xs:
            for y_2 in ys:
                line_2.append( ((grid_2.index((x_2,y_2))), ( 1/ ((x-x_2)**2 + (y-y_2)**2) **(1/2)) ))
        
        grid_line_2.append(line_2)

    return line1_to_line2
