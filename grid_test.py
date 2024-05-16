#!/usr/bin/python
# -*- coding: utf-8 -*-



from __future__ import print_function
import numpy as np 
import struct
import sys
import os, fnmatch

###################### Load grid ############################

def load_grid(filename):
    """
    brief  : loads a grid
    param  : filename - STR name of the grid's ASCII dump
    return : grid     - LIST of coordinates of grid points (TUPLES)
    """
    
    file = open(filename, mode ='r')
    size = int(file.readline().strip())
    grid = []
    
    for i in range(size):
        x,y = file.readline().split()
        x,y = int((float(x))), int((float(y)))
        grid.append((x,y))
    file.close()
    return grid

###################### Create grid ############################

def create_grid_file(grid_x, grid_y, filename):
    file = open(filename, mode ='w')
    file.writelines(["       "+str((len(grid_x)-1)*(len(grid_y)-1))+"\n"])
    for i in range(len(grid_x)-1):
        for j in range(len(grid_y)-1):
            file.writelines(["   "+str(grid_x[i]) + "        "+str(grid_y[j])+"        \n"])
    file.close

    
