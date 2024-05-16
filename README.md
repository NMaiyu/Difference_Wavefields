# Difference_Wavefields  
  
Computes and shows the difference (Ux, Uy or norm) between binary wavefield dumps created with [specfem2d](https://specfem2d.readthedocs.io/en/latest/)  
  
  
## Execution
  
  
### running an example  
  
  
### computeDifferenceBetweenWavefields.py  
This script creates binary files storing the difference along x and y axis in a speficied directory.   
If wanted, it is possible to also plot these (by adding 'i' in the "precisions" argument).   
  
#### Notes :   
The new directory where information will be stored should be created beforehand.   
The first directory should contain the output of the simulation with less elements.   
  
#### Syntax : 

>`python3 compute_difference.py simulation_1 simulation_2 output_name interf_name others`  
e.g.    `python3 ./compute_difference.py OUTPUT_coarse_heterogeneous OUTPUT_simple_heterogeneous OUTPUT_difference iv`  
  
>simulation_1  - `path of directory where binary outputs of reference simulation and ASCII grid are stored`  
                 should be the simulation with less elements  
                 e.g. ./simu1/OUTPUT  
  
>simulation_2  - `path of directory where binary outputs of reference simulation and ASCII grid are stored`  
                 e.g. ./simu2/OUTPUT  
  
>output_name - `directory where results are saved`  
                 e.g. ./test/difference.bin  
  
>interf_name  - `path of interfaces file (not mandatory)`  
                 This file is initially in DATA  
                 e.g. ./OUTPUT_reference/interfaces_simple_topo_curved.dat  
  
>others   
          - s : same grid is used in both simulation  
          - i : creation of an image (default = false)  
          - v : prints lots of details (default = false)  
          - x  : plots difference along x  
          - y  : plots difference along y  
          - n  : plots relative norm difference  
          Default : plots norm of difference  
  
  
### plot.py  
This script creates png plots of previously computed differences.   
The same arguments as in computeDifferenceBetweenWavefields are used here.   
It is possible to specify the direction (along x, y, or the norm/relative norm) of considered differences (by adding "x", "y", "n" in 'other')   
  
#### Syntax : 

>`python3 ./plot.py outputDirName DirName1 interface others`  
e.g.     `python3 ./plot.py  OUTPUT_difference OUTPUT_coarse_heterogeneous interfaces_topo.dat`  

>outputDirName  `- directory where computed data is saved`  
               e.g. ./OUTPUT_difference  
  
>DirName1    `- directory of reference simulation`  
               e.g. ./OUTPUT_reference  
  
>interface  - `path of interfaces file (not mandatory)`  
               This file is initially in DATA  
               e.g. ./OUTPUT_reference/interfaces_simple_topo_curved.dat  
  
>others   
          - v  : prints a lot of details (default = false)  
          - x  : plots difference along x  
          - y  : plots difference along y  
          - n  : plots relative norm difference  
          Default : plots norm of difference  
          Only one plot difference is applied at once  
  
  
## Structure

EXAMPLES  
  Directory storing tests. 

  
compute_differences.py  
  Script that compute differences between specfem binary wavefield dumps. 

plot.py
  Script that creates png plots of differences. 
  Can be used through compute_differencs.py,  
  but can also be used on compute_differencs.py binary results

grid.py
  Used in the two scripts abovet to load grids and compute correspondances

  
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
