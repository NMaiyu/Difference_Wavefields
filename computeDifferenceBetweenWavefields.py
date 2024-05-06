#!/usr/bin/python
# -*- coding: utf-8 -*-



from __future__ import print_function
import numpy as np 
from PIL import Image
import struct
import sys
import os, fnmatch

# import argparse # To deal with arguments :
# https://docs.python.org/2/library/argparse.html


###################### Transpose ############################


def transpose(grid_1, grid_2,grid_2x, grid_2y, line, content2):
    """
    brief  : gives the displacement in the 2nd simulation at the studied point 
    param  : grid_1   - LIST of coordinates of grid points (TUPLES) of the reference simulation
             grid_2   - LIST of coordinates of grid points (TUPLES) of the other simulation
             grid_2x  - LIST of xs in the other simulation's grid
             grid_2y  - LIST of ys in the other simulation's grid
             line     - INT no of the studied line, in the reference simulation output
             content2 - STR content of the bin output of the other simulation
    return : dx2, dy2 - TUPLE displacement at the studied point in the other simulation
    """

    # search the 4 closest points to the reference point
    (x,y) = grid_1[line]

    if (x in grid_2x): 
        if (y in grid_2y) : 
            # If the point is in both grids, no need to interpolate
            line_2 = grid_2.index((x,y))
            return struct.unpack("ff",content2[line*8:(line+1)*8])
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
    displacement = []
    weight = []
    for x_2 in xs:
        for y_2 in ys:
            line_2 = grid_2.index((x_2,y_2))
            displacement.append( struct.unpack("ff",content2[line_2*8:(line_2+1)*8]))
            weight.append( 1/ ((x-x_2)**2 + (y-y_2)**2) **(1/2))
    (dx2, dy2) = (sum( weight[i] * displacement[i][0] /sum(weight) for i in range (4)) , sum( weight[i] * displacement[i][1] /sum(weight) for i in range (4)))

    return (dx2, dy2)


###################### Grid ############################

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

###################### Main function ############################

def compute_difference_between_wavefields(sim_1, sim_2, name_output, image, verbose):
    """
    brief  : computes the difference between two wavefields
    param  : sim_1       - STR name of the directory with reference simulation data
             sim_2       - STR name of the directory with other simulation data
             name_output - STR name of the directory where outputs are saved
             image       - BOOL wether or not an image is generated 
    """
    
    
    l_files1 = fnmatch.filter(os.listdir(sim_1), "wavefield*_01.bin")
    l_files2 = fnmatch.filter(os.listdir(sim_2), "wavefield*_01.bin")
    
    
    if verbose : print("Loading reference simulation grid ...")
    grid_1=load_grid(sim_1+"/"+"ASCII_dump_of_grid_points.txt")[0]
    if verbose : print("Loading other simulation grid ... \n")
    grid_2, grid_2x, grid_2y=load_grid(sim_2+"/"+"ASCII_dump_of_grid_points.txt")
    
    
    # Compares files if at the same time
    for i in range(min(len(l_files1), len(l_files2))): 
        if verbose : 
            print("Comparing file "+str(i+1)+"/"+str(min(len(l_files1), len(l_files2)))+"...")
            print("     this can take time depending of data's size")
        if l_files1[i] in l_files2:
        
                with open(sim_1+"/"+l_files1[i], mode ='rb') as file1 :
                    content1 = file1.read()
                with open(sim_2+"/"+l_files1[i], mode ='rb') as file2 :
                    content2 = file2.read()
                
                size = len(content1)
                fileOut= open((name_output+"/"+l_files1[i]), mode ='wb')
                
                if image : l_differences=[]
                for line in range(int(size/8)):
                    # dx, dy are floats -> "f" and buffersize = 4
                    (dx1, dy1) = struct.unpack("ff",content1[line*8:(line+1)*8])
                    (dx2, dy2) = transpose(grid_1, grid_2,grid_2x, grid_2y, line, content2)
                    

                    dx, dy = dx2-dx1, dy2-dy1
                    fileOut.write(struct.pack("ff", dx, dy))
                    line+=1
                    if image : l_differences.append((dx**2 + dy**2)**(1/2))

                file1.close()
                file2.close()
                
                if verbose : print("     creating image")
                if image: write_image(sim_1,  l_differences)
                
                fileOut.close()
    if verbose : print("Difference between wavefields is computed !")

"""
    ###################### check ############################
    
    with open((name_output+"/"+l_files1[0]), mode ='rb') as file :
        content= file.read()
    for line in range(int(size/8)):
        print(struct.unpack("ff",content[line*8:(line+1)*8]))
    file.close()
"""

###################### Create Image ######################

def write_image(sim_1, l_difference):
    print("IMAGE CREATION NOT IMPLEMENTED YET...")
    return None   
    

###################### Usage ######################

def usage():
    print("Usage : ./computeDifferenceBetweenWavefields.py simulation_1 grid_1 filename_2 grid_2 output_name image verbose")
    print(" with")
    print("\n     simulation_1  - path of directory where binary outputs of reference simulation and ASCII grid are stored")
    print("                       should be the simulation with less elements")
    print("                       e.g. ./simu1/OUTPUT")
    
    print("\n     simulation_2  - path of directory where binary outputs of reference simulation and ASCII grid are stored")
    print("                       e.g. ./simu2/OUTPUT")
    
    print("\n     output_name - created filename")
    print("                       e.g. ./test/difference.bin")
    print("     image       - true/false - if true, creation of a bitmap")
    print("     verbose     - if true, prints lots of details")
    print("The simulation directories should contain binary outputs of simulation and ASCII grid output")
    sys.exit(1)
    
###################### Main ######################

if __name__ == '__main__':
    # gets arguments
    if len(sys.argv) < 6:
        usage()

    ## input parameters
    sim_1 = sys.argv[1]
    sim_2 = sys.argv[2]
    name_output = sys.argv[3]
    image = sys.argv[4]
    verbose = sys.argv[5]
    
    compute_difference_between_wavefields(sim_1, sim_2, name_output, image, verbose)

