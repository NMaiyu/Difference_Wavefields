#!/usr/bin/python
# -*- coding: utf-8 -*-



from __future__ import print_function
import numpy as np 
import struct
import sys
import os, fnmatch
import math
# import argparse # To deal with arguments :
# https://docs.python.org/2/library/argparse.html




###################### Compare files ############################

def compare_files(content1, content2, fileOut, size):
    for line in range(int(size/8)):
        # x, y are floats -> "f" and buffersize = 4 
        (x1, y1) = struct.unpack("ff",content1[line*8:(line+1)*8])
        (x2, y2) = struct.unpack("ff",content2[line*8:(line+1)*8])
        dx, dy = x2-x1, y2-y1
        fileOut.write(struct.pack("ff", dx, dy))
        line+=1
    return None



###################### Main function ############################

def compute_difference_between_wavefields(sim_1, mesh_1, sim_2, mesh_2, name_output, image):
    
    l_files1 = fnmatch.filter(os.listdir(sim_1), "wavefield*_01.bin")
    l_files2 = fnmatch.filter(os.listdir(sim_2), "wavefield*_01.bin")

    
    # Compares files if from the same time
    for i in range(min(len(l_files1), len(l_files2))): 
        if l_files1[i] in l_files2:
        
                with open(sim_1+"/"+l_files1[i], mode ='rb') as file1 :
                    content1 = file1.read()

                with open(sim_2+"/"+l_files1[i], mode ='rb') as file2 :
                    content2 = file2.read()
                
                size = len(content1)
                fileOut= open((name_output+"/"+l_files1[i]), mode ='wb')
                
                compare_files(content1, content2, fileOut, size)



                file1.close()
                file2.close()
                
                if (image==True): write_image(fileOut, size)
                
                fileOut.close()

"""
    ###################### check ############################
    
    with open((name_output+"/"+l_files1[0]), mode ='rb') as file :
        content= file.read()
    for line in range(int(size/8)):
        print(struct.unpack("ff",content[line*8:(line+1)*8]))
    file.close()
"""

###################### Create Image ######################

def write_image(fileOut, size):
    print("Create bmp   -   not written yet")
    return None
    

###################### Usage ######################

def usage():
    print("Usage : ./computeDifferenceBetweenWavefields.py simulation_1 mesh_1 filename_2 mesh_2 output_name image")
    print(" with")
    print("\n     simulation_1  - path of directory where binary outputs of reference simulation are stored")
    print("                       e.g. ./simu1/OUTPUT")
    print("     mesh_1        - mesh file's path")
    print("                       e.g. ./simu1/DATA/interface_simple_topo_flat.dat")
    
    print("\n     simulation_2  - path of directory where binary outputs of reference simulation are stored")
    print("                       e.g. ./simu2/OUTPUT")
    print("     mesh_2        - mesh file's path")
    print("                       e.g. ./simu2/DATA/interface_simple_topo_flat.dat")
    
    print("\n     output_name - created filename")
    print("                       e.g. ./test/difference.bin")
    print("     image       - true/false - if true, creation of a bitmap")
    sys.exit(1)
    
###################### Main ######################

if __name__ == '__main__':
    # gets arguments
    if len(sys.argv) < 7:
        usage()

    ## input parameters
    sim_1 = sys.argv[1]
    mesh_1 = sys.argv[2]
    sim_2 = sys.argv[3]
    mesh_2 = sys.argv[4]
    name_output = sys.argv[5]
    image = sys.argv[6]
    
    compute_difference_between_wavefields(sim_1, mesh_1, sim_2, mesh_2, name_output, image)

