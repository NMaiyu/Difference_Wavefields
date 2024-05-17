#!/bin/bash
#
# script runs solver and visualization
# using this example setup
#

echo "running example: `date`"
echo "Test maillages"
currentdir=`pwd`

# sets up directory structure in current example directoy
echo
echo "setting up example..."
echo 
echo simulation_1 : coarse_heterogeneous
echo simulation_2 : simple_heterogeneous
echo interface    : interface_topo_flat.dat
echo images       : relative norm difference
echo step         : 10
echo 

mkdir -p OUTPUT_FILES_Y

# cleans output files
rm -rf OUTPUT_FILES_Y/*

cd $currentdir

echo
python3 ../../compute_difference.py OUTPUT_coarse_heterogeneous OUTPUT_simple_heterogeneous OUTPUT_FILES_Y 10 interface_topo_flat.dat ivy


echo
echo "see results in directory: OUTPUT_FILES/"
echo
echo "done"
echo `date`

