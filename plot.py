#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import numpy as np 
import struct
import sys
import os, fnmatch
import matplotlib.pyplot as plt
from grid import load_grid 


def plot_difference(output_name,percentile, direction, interfaces, verbose) : 
    """
    brief  :  plots the difference in norm, along x/y, or the relative difference and saves it as png
    param  : output_name - directory where data is stored
             percentile  - percentile - % of extreme values muted in the plot
             direction   - plotted data's type : difference along x, y, its norm (n), or the relative difference (re)
             interfaces  - None or path of the .dat file containing interfaces' information
    """
    
    ###### Load grid ######
    l_files = fnmatch.filter(os.listdir(output_name), "wavefield*_01.bin")
    if verbose : print("Loading grid")
    grid = load_grid(output_name+"/ASCII_dump_of_grid_points.txt")
    x = np.array(sorted(set([point[0] for point in grid])))
    y = np.array(sorted(set([point[1] for point in grid])))
    
    ###### Create image for each binary file ######
    for filename in l_files :
        if verbose : print("Creating image for "+filename+" ...")
        
        ### Load files ###
        with open((output_name+"/"+filename), mode ='rb') as file :
            content= file.read()
            size = int(len(content)/8)
            file.close()
        if direction == "re" : 
            with open((output_name+"/reference_projection_"+filename), mode ='rb') as file :
                content_ref= file.read()
                file.close()
        
        ### Read data for each point ###
        delta = np.zeros((len(y),len(x)))
        for line in range(size):
            
            # Get difference
            (dx, dy) = struct.unpack("ff",content[line*8:(line+1)*8])
            
            if direction == "re" :
                # Get displacement of reference simulation  
                (xref, yref) = struct.unpack("ff", content_ref[line*8:(line+1)*8])
            
            # Get point coordinates and index
            xval,yval = grid[line]
            xval = np.where(x==xval)[0][0]
            yval=np.where(y==yval)[0][0]

            
            # Set information to plot
            if direction =="norm" : delta[yval][xval] = (dx**2 + dy**2)**(1/2)
            elif direction == "x" : delta[yval][xval] = dx
            elif direction == "y" : delta[yval][xval] = dy
            else : 
                if ((xref**2 + yref**2)**(1/2))!=0 :
                    delta[yval][xval] = (dx**2 + dy**2)**(1/2)/ (xref**2 + yref**2)**(1/2)
                else : delta[yval][xval] = -1
            
        ### Plot ###
        fig, ax = plt.subplots()
        delta = delta[:-1, :-1]
        perc = 1
        X, Y = np.meshgrid(x,y)
        extrema =max(np.percentile(delta, 100 - perc), 0.00001, -np.percentile(delta, perc))
        
        # Create colormesh
        if direction == "x" or direction == "y" :
            psm = ax.pcolormesh(X, Y, delta, vmin=-extrema, vmax=extrema, cmap="seismic")
        else :
            psm = ax.pcolormesh(X, Y, delta, vmin=0, vmax=extrema, cmap="nipy_spectral_r")
        ax.set_xlim(X.min(),X.max())
        ax.set_ylim(Y.min(),Y.max())
        
        # Draw interfaces and plot sources/Receivers
        if interfaces : 
            plot_points(interfaces, ax)
        plot_receivers(output_name,ax)
        plot_sources(output_name,ax)
        
        ### Save image ###
        ax.set_title(filename)
        if direction !="re" : label = "Difference in "+direction
        else : label = "Norm relative difference"
        fig.colorbar(psm, ax=ax, label=label)
        plt.figure(fig,figsize=(8,6), dpi=200)
        plt.savefig(output_name+"/"+filename[:-3]+"png", dpi=200)

###################### Plot topo, sources, receivers ######################

def plot_points(interfaces, ax):
    """
    brief  : plot interfaces on ax
    """
    f_interfaces = open(interfaces, mode ='r')
    l_interfaces = None
    element = 0
    line = f_interfaces.readline()
    while line.startswith('#'): line = f_interfaces.readline()
    n_interfaces = int(line)
    
    for i in range (n_interfaces):
        line = f_interfaces.readline()
        while line.startswith('#'): line = f_interfaces.readline()
        n_pts = int(line)
        X, Y = np.array([]), np.array([])
        for j in range (n_pts):
            x,y = f_interfaces.readline().split()
            X=np.append(X,float(x))
            Y=np.append(Y,float(y))
        ax.plot(X,Y,'-',color='black')

def plot_sources(output_name,ax):
    """
    brief  : plot sources as orange crosses
    """
    X,Y= np.array([]), np.array([])
    f_sources = open(output_name+"/for_information_SOURCE_actually_used", mode = "r")
    for source in f_sources :
        x,y = source.split()
        X=np.append(X,float(x))
        Y=np.append(Y,float(y))
    ax.scatter(X,Y, marker='x',color='orange')

def plot_receivers(output_name, ax):
    """
    brief  : plot receivers as green squares
    """
    f_receivers = open(output_name+"/for_information_STATIONS_actually_used", mode = "r")
    X,Y = np.array([]), np.array([])
    for receiver in f_receivers :
        receiver = receiver.split()
        X=np.append(X,float(receiver[2]))
        Y=np.append(Y, float(receiver[3]))
    ax.scatter(X,Y,s=5,marker="s",color="green")

###################### Usage ######################

def usage():
    print("Usage :\n./plot.py output_name interf_name (others) (percentile)")
    print(" with")
    print("\n     output_name  - directory where computed data is saved")
    print("                       if the reference simulation directory is used here")
    print("                       its wavefield bump will be plotted")
    print("                       e.g. ./OUTPUT_difference")
        
    print("\n     interf_name  - path of interfaces file (not mandatory)")
    print("                       This file is initially in DATA")
    print("                       e.g. ./OUTPUT_reference/interfaces_simple_topo_curved.dat")
    
    print("\n     others - v  : prints a lot of details (default = false)")
    print("              - x  : plots difference along x")
    print("              - y  : plots difference along y")
    print("              - n  : plots norm difference")
    print("              -      Default : plots relative norm difference")    
    print("                     Only one plot difference is applied at once")
    print("              - p  : set a percentile")

    print("\n     percentile - % of extreme values muted in the plot")
    print("                    Doesnt work if p parameter is not used in 'others'")
    print("                    Default = 0.1")
    sys.exit(1)
    
###################### Main ######################

if __name__ == '__main__':
    # gets arguments
    if len(sys.argv) < 2:
        usage()
    
    ## read parameters
    output_name = sys.argv[1]
    verbose = False
    direction = "re"
    interfaces = False
    others=0
    percentile = 0.1
    if ".dat" in sys.argv[2] : 
        interfaces = sys.argv[2]
        others=1
        
    if len(sys.argv)>(2+others):
        if "v" in sys.argv[2+others] : verbose = True
        if "x" in sys.argv[2+others] : direction = "x"
        if "y" in sys.argv[2+others] : direction = "y"
        if "n" in sys.argv[2+others] : direction = "norm"
        if "p" in sys.argv[2+others] : percentile = sys.argv[2+others]
    
        
    plot_difference(output_name, percentile, direction ,interfaces,verbose)

