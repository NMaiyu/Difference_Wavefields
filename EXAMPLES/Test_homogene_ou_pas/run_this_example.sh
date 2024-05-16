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
echo simulation_1 : simple_flat
echo simulation_2 : simple_heterogeneous
echo interface    : interface_topo_flat.dat
echo images       : relative norm difference
echo

mkdir -p OUTPUT_FILES

# cleans output files
rm -rf OUTPUT_FILES/*

cd $currentdir

echo
python3 ../../compute_difference_test.py OUTPUT_simple_flat  OUTPUT_simple_heterogeneous OUTPUT_FILES interface_topo_flat.dat iv


echo
echo "see results in directory: OUTPUT_FILES/"
echo
echo "done"
echo `date`

