#!/bin/bash
#
# script runs solver and visualization
# using this example setup
#

echo "running example: `date`"
currentdir=`pwd`

# sets up directory structure in current example directoy
echo
echo "setting up example..."
echo 
echo simulation_1 : 80x60_elements
echo simulation_2 : 81x60_elements
echo interface    : interfaces_simple_topo_curved.dat
echo images       : relative norm difference
echo 

mkdir -p OUTPUT_FILES

# cleans output files
rm -rf OUTPUT_FILES/*

cd $currentdir

echo
python3 ../../compute_difference_test.py 80x60_elements 81x60_elements OUTPUT_FILES interfaces_simple_topo_curved.dat ivn

echo
echo "see results in directory: OUTPUT_FILES/"
echo
echo "done"
echo `date`

