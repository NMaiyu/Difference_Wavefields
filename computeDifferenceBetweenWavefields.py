#!/usr/bin/python
# -*- coding: utf-8 -*-



from __future__ import print_function
import numpy as np 
import struct
import sys



###################### Open file ############################


def compute_difference_between_wavefields(name_file1, name_file2, name_output):
    with open(name_file1, mode ='rb') as file1 :
        content1 = file1.read()

    with open(name_file2, mode ='rb') as file2 :
        content2 = file2.read()

    fileOut= open(name_output, mode ='wb')


    # Loop to compare corresponding elements


    size = len(content1)


    for line in range(int(size/8)):
        # C'est des floats donc "f" buffersize = 4 ; et on lit les couples de déplacement en sortie
        (x1, y1) = struct.unpack("ff",content1[line*8:(line+1)*8])
        (x2, y2) = struct.unpack("ff",content2[line*8:(line+1)*8])
        dx, dy = x2-x1, y2-y1
        fileOut.write(struct.pack("ff", dx, dy))
        line+=1



    file1.close()
    file2.close()
    fileOut.close()

    ###################### check ############################
    
    with open(name_output, mode ='rb') as file :
        content= file.read()
    for line in range(int(size/8)):
        print(struct.unpack("ff",content[line*8:(line+1)*8]))
    file.close()




###################### Usage ######################

def usage():
    print("Usage : ./computeDifferenceBetweenWavefields.py finelame_1 filename_2 output_name")
    print(" with")
    print("     filename_1  - reference file's path ; e.g. ./test/wavefield0001000_01.bin")
    print("     filename_2  - other file's path     ; e.g. ./test/wavefield0000005_01.bin")
    print("     output_name - created filename      ; e.g. ./test/difference.bin")
    sys.exit(1)

###################### Main ######################

if __name__ == '__main__':
    # gets arguments
    if len(sys.argv) < 4:
        usage()

    ## input parameters
    name_file1 = sys.argv[1]
    name_file2 = sys.argv[2]
    name_output = sys.argv[3]

    compute_difference_between_wavefields(name_file1, name_file2, name_output)

