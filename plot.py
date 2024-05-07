#!/usr/bin/python
# -*- coding: utf-8 -*-



from __future__ import print_function
import numpy as np 
import struct
import sys
import os, fnmatch
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.ticker import MaxNLocator
from grid import load_grid 


def plot_difference(output, grid_name, direction, verbose) : 
    l_files = fnmatch.filter(os.listdir(output), "wavefield*_01.bin")
    
    if verbose : print("Loading grid")
    grid, grid_x, grid_y = load_grid(grid_name)
    

    for filename in l_files :
        if verbose : print(filename)
        with open((output+"/"+filename), mode ='rb') as file :
            content= file.read()
        file.close
        
        size = int(len(content)/8)
        
        delta = np.zeros((int(len(grid_y)), int(len(grid_x))))
        x = np.array(grid_x)
        y = np.array(grid_y)
        for line in range(size):
            (dx, dy) = struct.unpack("ff",content[line*8:(line+1)*8])
            xval,yval = grid[line]
            
            xval = np.where(x == xval)[0][0]
            yval = np.where(y == yval)[0][0]

            
            if direction =="xy" : delta[yval][xval] = (dx**2 + dy**2)**(1/2)
            elif direction == "x" : delta[yval][xval]=dx
            else : delta[yval][xval] = dy

        X, Y = np.meshgrid(x,y)
        delta = delta[:-1, :-1]
        
        fig, ax = plt.subplots()
        
        psm = ax.pcolormesh(X, Y, delta, vmin=0, vmax=max(delta.max(), 0.00001))
        ax.set_title(filename)
        fig.colorbar(psm, ax=ax)
        plt.savefig(output+"/"+filename[:-3]+"png")


###################### Usage ######################

def usage():
    print("Usage :\n./plot.py output_name grid_name others")
    print(" with")
    print("\n     output_name  - directory where computed data is saved")
    print("                       e.g. ./OUTPUT_difference")
    
    print("\n     grid_name    - name of reference ASCII grid file")
    print("                       e.g. ./OUTPUT_reference")
    
    print("\n     others - v  : prints a lot of details (default = false)")
    print("              - x  : plots difference along x")
    print("              - y  : plots difference along y")
    print("              Default : plots norm of difference")
    print("              Only one plot difference is applied at once")
    sys.exit(1)
    
###################### Main ######################

if __name__ == '__main__':
    # gets arguments
    if len(sys.argv) < 3:
        usage()
    
    ## input parameters
    output = sys.argv[1]
    grid_name = sys.argv[2]
    verbose = False
    direction = "xy"
    if "v" in sys.argv[3] : verbose = True
    if "x" in sys.argv[3] : direction = "x"
    if "y" in sys.argv[3] : direction = "y"
        
    plot_difference(output, grid_name, direction ,verbose)

