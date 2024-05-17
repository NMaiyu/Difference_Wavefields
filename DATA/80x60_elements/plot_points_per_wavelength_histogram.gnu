 set term wxt
 #set term gif
 #set output "points_per_wavelength_histogram_S_in_solid.gif"

 set boxwidth   0.123908736    
 set xlabel "Range of min number of points per S wavelength in solid"
 set ylabel "Percentage of elements (%)"
 set loadpath "./OUTPUT_FILES/"
 plot "points_per_wavelength_histogram_S_in_solid.txt" with boxes
 pause -1 "hit any key..."
