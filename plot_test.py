#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import numpy as np 
import struct
import sys
import os, fnmatch
import matplotlib.pyplot as plt
from grid_test import load_grid 


def plot_difference(output_name, simu_name, direction,interfaces, verbose) : 
    l_files = fnmatch.filter(os.listdir(output_name), "wavefield*_01.bin")
    
    if verbose : print("Loading grid")
    grid = load_grid(output_name+"/ASCII_dump_of_grid_points.txt")
    

    for filename in l_files :
        if verbose : print("Creating image for "+filename+" ...")
        with open((output_name+"/"+filename), mode ='rb') as file :
            content= file.read()
        file.close
        
        if direction == "re" : 
            with open((output_name+"/reference_projection_"+filename), mode ='rb') as file :
                content_ref= file.read()
            file.close
        
        size = int(len(content)/8)
        
        x = np.array(sorted(set([point[0] for point in grid])))
        y = np.array(sorted(set([point[1] for point in grid])))
        delta = np.zeros((len(y),len(x)))
        for line in range(size):
            (dx, dy) = struct.unpack("ff",content[line*8:(line+1)*8])
            if direction == "re" :
                (xref, yref) = struct.unpack("ff", content_ref[line*8:(line+1)*8])
            xval,yval = grid[line]
            xval = np.where(x==xval)[0][0]
            yval=np.where(y==yval)[0][0]

            
            if direction =="norm" : delta[yval][xval] = (dx**2 + dy**2)**(1/2)
            elif direction == "x" : delta[yval][xval] = dx
            elif direction == "y" : delta[yval][xval] = dy
            else : 
                if ((xref**2 + yref**2)**(1/2))!=0 :
                    delta[yval][xval] = (dx**2 + dy**2)**(1/2)/ (xref**2 + yref**2)**(1/2)
                else : delta[yval][xval] = -1


        delta = delta[:-1, :-1]
        fig, ax = plt.subplots()
        
        X, Y = np.meshgrid(x,y)
        extrema =max(np.percentile(delta, 90), 0.00001, -np.percentile(delta, 0.1))

        if direction == "x" or direction == "y" :
            psm = ax.pcolormesh(X, Y, delta, vmin=-extrema, vmax=extrema, cmap="seismic")
        else :
            psm = ax.pcolormesh(X, Y, delta, vmin=0, vmax=extrema, cmap="nipy_spectral_r")

        ax.set_xlim(X.min(),X.max())
        ax.set_ylim(Y.min(),Y.max())
        
        if interfaces : 
            plot_points(interfaces, ax)
        plot_receivers(simu_name,ax)
        plot_sources(simu_name,ax)

        ax.set_title(filename)
        if direction !="re" : label = "Difference in "+direction
        else : label = "Norm relative difference"
        fig.colorbar(psm, ax=ax, label=label)
        plt.figure(fig,figsize=(8,6), dpi=200)
        plt.savefig(output_name+"/"+filename[:-3]+"png", dpi=200)


def plot_points(interfaces, ax):
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

def plot_sources(simu_name,ax):
    X,Y= np.array([]), np.array([])
    f_sources = open(simu_name+"/for_information_SOURCE_actually_used", mode = "r")
    for source in f_sources :
        x,y = source.split()
        X=np.append(X,float(x))
        Y=np.append(Y,float(y))
    ax.scatter(X,Y, marker='x',color='orange')

def plot_receivers(simu_name, ax):
    f_receivers = open(simu_name+"/for_information_STATIONS_actually_used", mode = "r")
    X,Y = np.array([]), np.array([])
    for receiver in f_receivers :
        receiver = receiver.split()
        X=np.append(X,float(receiver[2]))
        Y=np.append(Y, float(receiver[3]))
    ax.scatter(X,Y,s=5,marker="s",color="green")

###################### Usage ######################

def usage():
    print("Usage :\n./plot.py output_name simu_name interf_name others")
    print(" with")
    print("\n     output_name  - directory where computed data is saved")
    print("                       if the reference simulation directory is used here")
    print("                       its wavefield bump will be plotted")
    print("                       e.g. ./OUTPUT_difference")
    
    print("\n     simu_name    - directory of reference simulation")
    print("                       e.g. ./OUTPUT_reference")
    
    print("\n     interf_name  - path of interfaces file (not mandatory)")
    print("                       This file is initially in DATA")
    print("                       e.g. ./OUTPUT_reference/interfaces_simple_topo_curved.dat")
    
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
    output_name = sys.argv[1]
    simu_name = sys.argv[2]
    verbose = False
    direction = "norm"
    interfaces = False
    others=0
    if ".dat" in sys.argv[3] : 
        interfaces = sys.argv[3]
        others=1
        
    if len(sys.argv)>(3+others):
        if "v" in sys.argv[3+others] : verbose = True
        if "x" in sys.argv[3+others] : direction = "x"
        if "y" in sys.argv[3+others] : direction = "y"
        if "n" in sys.argv[3+others] : direction = "re"
    
        
    plot_difference(output_name, simu_name, direction ,interfaces,verbose)

