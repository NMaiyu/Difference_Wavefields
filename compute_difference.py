#!/usr/bin/python
# -*- coding: utf-8 -*-



from __future__ import print_function
import numpy as np 
import struct
import sys
import os, fnmatch
from grid import load_grid, create_grid_file
from plot import plot_difference
from scipy.interpolate import griddata


###################### Main function ############################

def compute_difference_between_wavefields(sim_1, sim_2, name_output, percentile, step, image, direction, interfaces, verbose):
    """
    brief  : computes the difference between two wavefields
    param  : sim_1       - STR name of the directory with reference simulation data
             sim_2       - STR name of the directory with other simulation data
             name_output - STR name of the directory where outputs are saved
             image       - BOOL wether or not an image is generated 
    """
    
    
    l_files1 = fnmatch.filter(os.listdir(sim_1), "wavefield*_01.bin")
    l_files2 = fnmatch.filter(os.listdir(sim_2), "wavefield*_01.bin")
    
    ###### Load grid ######
    if verbose : print("\nLoading reference simulation grid ...")
    grid_1=load_grid(sim_1+"/"+"ASCII_dump_of_grid_points.txt")
    if verbose : print("Loading other simulation grid ... \n")
    grid_2 =load_grid(sim_2+"/"+"ASCII_dump_of_grid_points.txt")
    
    
    ###### Create new grid ######
    size = len(grid_1)
    xmax = max(grid_1[i][0] for i in range(size))+step
    zmax = max(grid_1[i][1] for i in range(size))+step

    grid_x, grid_y = np.mgrid[0:xmax:step, 0:zmax:step]
    create_grid_file(grid_x[:,0], grid_y[0,:], name_output+"/"+"ASCII_dump_of_grid_points.txt")
    
    ###### Copy information files ######
    os.system('cp '+sim_1+"/for_information_STATIONS_actually_used " +name_output+"/for_information_STATIONS_actually_used")
    os.system('cp '+sim_1+"/for_information_SOURCE_actually_used " +name_output+"/for_information_SOURCE_actually_used")   
    
    ###### Compare files ######
    for i in range(min(len(l_files1), len(l_files2))): 
    
        ## The difference is computed if there is data at the same time in both simulations
        if verbose : 
            print("Comparing file "+str(i+1)+"/"+str(min(len(l_files1), len(l_files2)))+"...")
        if l_files1[i] in l_files2: 
        
            ### Open files ###
            with open(sim_1+"/"+l_files1[i], mode ='rb') as file1 :
                content1 = file1.read()
                d1 = np.array([struct.unpack("ff",content1[l*8:(l+1)*8]) for l in range(size)])
                file1.close
            with open(sim_2+"/"+l_files1[i], mode ='rb') as file2 :
                content2 = file2.read()
                d2 = np.array([struct.unpack("ff",content2[l*8:(l+1)*8]) for l in range(len(grid_2))])
                file2.close()

            ### Create output files ###
            fileOut= open(name_output+"/"+l_files1[i], mode ='wb')
            if direction=="re" : 
                file1_projection = open(name_output+"/reference_projection_"+l_files1[i],mode="wb")

            ### Interpolate wavefield dumps ### 
            d2_x = griddata(grid_2, [point[0] for point in d2], (grid_x, grid_y), method = 'linear')
            d2_y = griddata(grid_2, [point[1] for point in d2], (grid_x, grid_y), method = 'linear')
            
            d1_x = griddata(grid_1, [point[0] for point in d1], (grid_x, grid_y), method = 'linear')
            d1_y = griddata(grid_1, [point[1] for point in d1], (grid_x, grid_y), method = 'linear')
            
            dx = d2_x - d1_x
            dy = d2_y - d1_y
                
            dx = np.reshape(dx, (1,len(grid_x[:,0])*len(grid_y[0,:])))[0]
            dy = np.reshape(dy, (1,len(grid_x[:,0])*len(grid_y[0,:])))[0]
            if direction=="re": 
                d1_x = np.reshape(d1_x, (1,len(grid_x[:,0])*len(grid_y[0,:])))[0]
                d1_y = np.reshape(d1_y, (1,len(grid_x[:,0])*len(grid_y[0,:])))[0]
            
            ### Write output files ###
            for i in range(len(dx)):
                if np.isnan(dx[i]) : dx[i]=0
                if np.isnan(dy[i]) : dy[i]=0
                fileOut.write(struct.pack("ff", dx[i], dy[i]))
                if direction=="re":
                    if np.isnan(d1_x[i]) : d1_x[i]=0
                    if np.isnan(d1_y[i]) : d1_y[i]=0
                    file1_projection.write(struct.pack("ff",d1_x[i], d1_y[i]))
                            
            if direction == "re" : file1_projection.close()
            fileOut.close()
    if verbose : print("\nCreating images of " + direction + " differences" )
    if image : plot_difference(name_output, percentile, direction, interfaces, verbose)

###################### Usage ######################

def usage():
    print("Usage :\n./compute_difference.py simulation_1 simulation_2 output_name step interf_name (others) (percentile)")
    print(" with")
    print("\n     simulation_1  - path of directory where binary outputs of reference simulation and ASCII grid are stored")
    print("                       should be the simulation with less elements")
    print("                       e.g. ./simu1/OUTPUT")
    
    print("\n     simulation_2  - path of directory where binary outputs of reference simulation and ASCII grid are stored")
    print("                       e.g. ./simu2/OUTPUT")
    
    print("\n     output_name   - directory where results are saved")
    print("                       e.g. ./test/difference.bin")
    
    print("\n     step          - x,z step of the new mesh")
    print("                       e.g. 10")

    print("\n     interf_name   - path of interfaces file (not mandatory)")
    print("                       This file is initially in DATA")
    print("                       e.g. ./OUTPUT_reference/interfaces_simple_topo_curved.dat")

    print("\n     (others)   - i : creation of an image (default = false)")
    print("              - v : prints lots of details (default = false)")
    print("              - x  : plots difference along x")
    print("              - y  : plots difference along y")
    print("              - n  : plots difference's norm")
    print("              Default : plots relative norm difference")
    print("The simulation directories should contain binary outputs of simulation and ASCII grid output")
    print("              - p  : set a percentile")

    print("\n     (percentile) - % of extreme values muted in the plot")
    print("                    Doesnt work if p parameter is not used in 'others'")
    print("                    Default = 0.1")
    sys.exit(1)
    
###################### Main ######################

if __name__ == '__main__':
    ## get arguments
    if len(sys.argv) < 5:
        usage()
    
    ## input parameters
    sim_1 = sys.argv[1]
    sim_2 = sys.argv[2]
    name_output = sys.argv[3]
    step = int(sys.argv[4])
    image, verbose = False, False
    direction = "re"
    percentile =0.1
    oth=0
    interfaces = False
    
    if len(sys.argv)>5 :
        if ".dat" in sys.argv[5] : 
            interfaces = sys.argv[5]
            oth=1
    
    if len(sys.argv)>(5+oth) :
        if "i" in sys.argv[5+oth] : image = True
        if "v" in sys.argv[5+oth] : verbose = True
        if "x" in sys.argv[5+oth] : direction = "x"
        if "y" in sys.argv[5+oth] : direction = "y"
        if "n" in sys.argv[5+oth] : direction = "norm"
        if "p" in sys.argv[5+oth] : percentile = float(sys.argv[6+oth])
        
    compute_difference_between_wavefields(sim_1, sim_2, name_output,percentile, step, image, direction, interfaces, verbose)

