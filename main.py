#!/usr/bin/python
# -*- coding: utf-8 -*-



from __future__ import print_function
from compute_difference import compute_difference_between_wavefields

###################### Arguments ############################

###### DATA and OUTPUT ######

# simulation_1  - directory where binary outputs of reference simulation and ASCII grid are stored
#                   should be the simulation with less elements
sim_1 = "./DATA/80x60_elements"

# simulation_2  - directory where binary outputs of reference simulation and ASCII grid are stored
sim_2 = "./DATA/81x60_elements"

# output_name   - directory where results are saved
output_name = "./OUTPUT_FILES"

# interf_name   - path of interfaces file
#                 can be set on False in order not to plot interfaces
#                 This file is the DATA directory of specfem2d simulation
interf_name = "./DATA/interfaces_simple_topo_curved.dat"


###### PARAMETERS ######

image = True        # plot an image
step = 10            # x,z step of the new mesh
percentile = 0.1     # % of extreme values muted in the plot
plot_type = "re"     # type of information to plot
#                   - x  : plots difference along x
#                   - y  : plots difference along y
#                   - norm  : plots relative norm difference
#                   - re : norm of difference

###### GLOBAL ######

verbose = True      # print details
compute = True       # compute the difference (and plot image if 'image' is True)
plot_only = False    # plot previously computed difference


###################### Run ############################

if compute : prints("Computation of difference between specfem2d displacement wavefield dumps")
elif plot_only : prints("Plot difference between specfem2d displacement wavefield dumps")

print("\nsimulation_1 : "+simu_1)
print("simulation_2 : "+simu_2)
print("output file  : "+output_name)
if interf_name : print("interface    : "+interf_name)
if image : 
    if plot_type == "re" : print("images       : relative norm difference")
    elif plot_type == "x" : print("images       : difference along x")
    elif plot_type == "y" : print("images       : difference along y")
    elif plot_type == "norm" : print("images       : difference's norm")
print("step         : "+str(step))
print(" percentile   : "+str(percentile)+"\n")


if compute : compute_difference_between_wavefields(sim_1, sim_2, output_name, percentile, step, image, plot_type, interf_name, verbose)
elif plot_only : plot_difference(output_name, percentile, plot_type ,interf_name,verbose)

print("done")
