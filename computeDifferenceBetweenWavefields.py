#!/usr/bin/python
# -*- coding: utf-8 -*-



from __future__ import print_function
import numpy as np 
import struct
import sys
import os, fnmatch
from grid import grid_correspondance, load_grid


###################### Main function ############################

def compute_difference_between_wavefields(sim_1, sim_2, name_output, same_grid, image, verbose):
    """
    brief  : computes the difference between two wavefields
    param  : sim_1       - STR name of the directory with reference simulation data
             sim_2       - STR name of the directory with other simulation data
             name_output - STR name of the directory where outputs are saved
             image       - BOOL wether or not an image is generated 
    """
    
    
    l_files1 = fnmatch.filter(os.listdir(sim_1), "wavefield*_01.bin")
    l_files2 = fnmatch.filter(os.listdir(sim_2), "wavefield*_01.bin")
    
    ###### Loads grid ######
    if verbose : print("\nLoading reference simulation grid ...")
    grid_1=load_grid(sim_1+"/"+"ASCII_dump_of_grid_points.txt")[0]
    if verbose : print("Loading other simulation grid ... \n")
    grid_2, grid_2x, grid_2y=load_grid(sim_2+"/"+"ASCII_dump_of_grid_points.txt")
    
    ###### Grid correspondance ######
    if not same_grid : 
        if verbose : print("Computing correspondance between the two grids")
        line1_to_line2 = grid_correspondance(grid_1, grid_2, grid_2x, grid_2y)
    size = len(grid_1)
    
    ###### Compares files ######
    for i in range(min(len(l_files1), len(l_files2))): 
        if verbose : 
            print("Comparing file "+str(i+1)+"/"+str(min(len(l_files1), len(l_files2)))+"...")
        
        if l_files1[i] in l_files2: 
            #if data exists at the same time in both simulations
            
            ### Opens files ###
            with open(sim_1+"/"+l_files1[i], mode ='rb') as file1 :
                content1 = file1.read()
            with open(sim_2+"/"+l_files1[i], mode ='rb') as file2 :
                content2 = file2.read()
            fileOut= open((name_output+"/"+l_files1[i]), mode ='wb')
            
            
            if image : l_differences=[]
            for line1 in range(size):
                
                
                # dx, dy are floats -> "f" and buffersize = 4
                (dx1, dy1) = struct.unpack("ff",content1[line1*8:(line1+1)*8])
                
                if same_grid : 
                    (dx2, dy2) = struct.unpack("ff",content2[line1*8:(line1+1)*8])
                else : 
                    line2 = line1_to_line2[line1]
                    (dx2, dy2) = (0,0)
                    for (l, w) in line2 : 
                         (dx2i, dy2i) = struct.unpack("ff",content2[l*8:(l+1)*8])
                         dx2 += dx2i
                         dy2 += dy2i

                dx, dy = dx2-dx1, dy2-dy1
                fileOut.write(struct.pack("ff", dx, dy))
                if image : l_differences.append((dx**2 + dy**2)**(1/2))

            file1.close()
            file2.close()
            
            if image: 
                write_image(sim_1,  l_differences)
                if verbose : print("     creating image")
                
            fileOut.close()
    if verbose : print("Difference between wavefields is computed !")


###################### Create Image ######################

def write_image(sim_1, l_difference):
    print("IMAGE CREATION NOT IMPLEMENTED YET...")
    return None   
    

###################### Usage ######################

def usage():
    print("Usage :\n./computeDifferenceBetweenWavefields.py simulation_1 simulation_2 output_name others")
    print(" with")
    print("\n     simulation_1  - path of directory where binary outputs of reference simulation and ASCII grid are stored")
    print("                       should be the simulation with less elements")
    print("                       e.g. ./simu1/OUTPUT")
    
    print("\n     simulation_2  - path of directory where binary outputs of reference simulation and ASCII grid are stored")
    print("                       e.g. ./simu2/OUTPUT")
    
    print("\n     output_name - created filename")
    print("                       e.g. ./test/difference.bin")
    print("     others   - s : same grid is used in both simulation")
    print("              - i : creation of a bitmap (default = false)")
    print("              - v : prints lots of details (default ) false)")
    print("The simulation directories should contain binary outputs of simulation and ASCII grid output")
    sys.exit(1)
    
###################### Main ######################

if __name__ == '__main__':
    # gets arguments
    if len(sys.argv) < 5:
        usage()
    
    ## input parameters
    sim_1 = sys.argv[1]
    sim_2 = sys.argv[2]
    name_output = sys.argv[3]
    same_grid, image, verbose = False, False, False
    if "s" in sys.argv[4] : same_grid = True
    if "i" in sys.argv[4] : image = True
    if "v" in sys.argv[4] : verbose = True
        
    compute_difference_between_wavefields(sim_1, sim_2, name_output, same_grid, image, verbose)

