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
echo simulation_1 : simple_topo_normal
echo simulation_2 : simple_topo_without_fluid
echo interface    : interfaces_simple_topo_curved.dat
echo images       : relative norm difference
echo step         : 10
echo 

mkdir -p OUTPUT_FILES

# cleans output files
rm -rf OUTPUT_FILES/*

cd $currentdir

echo
python3 ../../compute_difference.py OUTPUT_simple_topo_normal OUTPUT_simple_topo_without_fluid OUTPUT_FILES 10 interfaces_simple_topo_curved.dat iv

echo
echo "see results in directory: OUTPUT_FILES/"
echo
echo "done"
echo `date`

