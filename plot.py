#!/usr/bin/python
# -*- coding: utf-8 -*-



from __future__ import print_function
import numpy as np 
import struct
import sys
import os, fnmatch
import matplotlib.pyplot as plt
from grid import load_grid 


def plot_difference(output, grid_name, direction, verbose) : 
    l_files = fnmatch.filter(os.listdir(output), "wavefield*_01.bin")
    
    if verbose : print("Loading grid")
    grid, grid_x, grid_y = load_grid(grid_name+"/ASCII_dump_of_grid_points.txt")
    

    for filename in l_files :
        if verbose : print(filename)
        with open((output+"/"+filename), mode ='rb') as file :
            content= file.read()
        file.close
        
        if direction == "re" : 
            with open((grid_name+"/"+filename), mode ='rb') as file :
                content_ref= file.read()
            file.close
        
        size = int(len(content)/8)
        
        delta = np.zeros((int(len(grid_y)), int(len(grid_x))))
        x = np.array(grid_x)
        y = np.array(grid_y)
        for line in range(size):
            (dx, dy) = struct.unpack("ff",content[line*8:(line+1)*8])
            if direction == "re" :
                (xref, yref) = struct.unpack("ff", content_ref[line*8:(line+1)*8])
            xval,yval = grid[line]
            
            xval = np.where(x == xval)[0][0]
            yval = np.where(y == yval)[0][0]

            
            if direction =="norm" : delta[yval][xval] = (dx**2 + dy**2)**(1/2)
            elif direction == "x" : delta[yval][xval] = dx
            elif direction == "y" : delta[yval][xval] = dy
            else : 
                if ((xref**2 + yref**2)**(1/2))!=0 :
                    delta[yval][xval] = (dx**2 + dy**2)**(1/2)/ (xref**2 + yref**2)**(1/2)
                else : delta[yval][xval] = (dx**2 + dy**2)**(1/2)

        X, Y = np.meshgrid(x,y)
        delta = delta[:-1, :-1]
        
        fig, ax = plt.subplots()
        

        extrema = max(-delta.min(), delta.max(), 0.00001)
        if direction == "x" or direction == "y" :
            psm = ax.pcolormesh(X, Y, delta, vmin=-extrema, vmax=extrema, cmap="seismic")
        else :
            psm = ax.pcolormesh(X, Y, delta, vmin=0, vmax=extrema, cmap="nipy_spectral_r")

        ax.set_title(filename)
        fig.colorbar(psm, ax=ax)
        
        plt.savefig(output+"/"+filename[:-3]+"png")


def plot_points(interfaces, ax):
    f_interfaces = open(interfaces, mode ='r')
    l_interfaces = None
    element = 0
    line = f_interfaces.readline()
    while line.startswith('#'): line = f_interfaces.readline()
    n_interfaces = int(line)
    
    for i in range (n_interfaces):
        line = f_interfaces.readline()
        if line.startswith('#'):
            continue
        n_pts = line
        X, Y = np.array([]), np.array([])
        for j in range (n_pts):
            x,y = f_interfaces.readline().split()
            np.append(X,float(x))
            np.append(Y,float(y))
        X,Y = np.meshgrid(X,Y)
        plt.plot(X,Y,'-')

def plot_sources(grid_name):
    X,Y= np.array([]), np.array([])
    f_sources = open(grid_name+"/for_information_SOURCE_actually_used", mode = "r")
    for source in f_sources :
        x,y = source.split()
        np.append(X,x)
        np.append(Y,y)
    X,Y = np.meshgrid(X,Y)
    return X,Y

def plot_receivers(grid_name, ax):
    f_receivers = open(grid_name+"/for_information_STATIONS_actually_used", mode = "r")
    X,Y = np.array([]), np.array([])
    for receiver in f_receivers :
        receiver = receiver.split()
        np.append(X,receiver[2])
        np.append(Y, receiver[3])
    X,Y = np.meshgrid(X,Y)
    ax.scatter(X,Y,s=200, marker='s',color="green")

###################### Usage ######################

def usage():
    print("Usage :\n./plot.py output_name grid_name others")
    print(" with")
    print("\n     output_name  - directory where computed data is saved")
    print("                       e.g. ./OUTPUT_difference")
    
    print("\n     grid_name    - directory of reference ASCII grid file")
    print("                       e.g. ./OUTPUT_reference")
    
    print("\n     others - v  : prints a lot of details (default = false)")
    print("              - x  : plots difference along x")
    print("              - y  : plots difference along y")
    print("              - n  : plots relative norm difference")
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
    direction = "norm"
    if "v" in sys.argv[3] : verbose = True
    if "x" in sys.argv[3] : direction = "x"
    if "y" in sys.argv[3] : direction = "y"
    if "n" in sys.argv[3] : direction = "re"
    
        
    plot_difference(output, grid_name, direction ,verbose)

