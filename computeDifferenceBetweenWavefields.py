###################### Open file ############################

name_file1 = "wavefield0001000_01.bin"
name_file2 = "wavefield0000005_01.bin"
name_output = "test.bin" #Name of the difference file


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



###################### Tests ###############

with open(name_output, mode ='rb') as file :
    content= file.read()
for line in range(int(size/8)):
    print(struct.unpack("ff",content[line*8:(line+1)*8]))
    
file.close()
