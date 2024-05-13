# Difference_Wavefields

Computes and shows the difference (Ux, Uy or norm) between binary wavefield dumps created with [![specfem2d](https://specfem2d.readthedocs.io/en/latest/)]
It has been tested on "simple_topography_and_also_a_simple_fluid_layer", with and without the fluid layer. 

### computeDifferenceBetweenWavefields.py
This script creates binary files storing the difference along x and y axis in a speficied directory. 
If wanted, it is possible to also plot these (by adding 'i' in the "precisions" argument). 

Notes : 
The new directory where information will be stored should be created beforehand. 
The first directory should contain the output of the simulation with less elements. 

Syntax : python3 ./computeDifferenceBetweenWavefields.py DirName1 DirName2 outputDirName precisions
e.g.    `python3 ./computeDifferenceBetweenWavefields.py OUTPUT_coarse_heterogeneous OUTPUT_simple_heterogeneous OUTPUT_difference i`

### plot.py
This script creates png plots of previously computed differences. 
The same arguments as in computeDifferenceBetweenWavefields are used here. 
It is possible to specify the direction (along x, y, or the norm) of considered differences (by adding "x", "y" in 'other') 

Syntax : python3 ./plot.py outputDirName DirName1 others
e.g.     `python3 ./plot.py  OUTPUT_difference OUTPUT_coarse_heterogeneous`

## Notes
1. Requires following simulation parameters:
-   `output_grid_ASCII = .true.`
-   `output_wavefield_dumps = .true.`
-   `use_binary_for_wavefield_dumps = .true.`
2. Differences can not be computed for different timesteps
3. Uses following modules:
-   numpy 
-   struct
-   matplotlib.pyplot
4. Boundaries between materials, source and receiver are not plotted
