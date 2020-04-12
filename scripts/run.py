import os
import sys

benchmark = [(5,5), (5,10), (5,15), (6,6), (6,12), (6,18), (10,10), (10,15), (10,20), (10,30), (10,35)]

for (i,j) in benchmark:
    filename = "../benchmarks/"+str(i)+"_"+str(j)+".txt"
    outputfilename = "../outputs/"+str(i)+"_"+str(j)+".txt"
    commandline = " ".join(["../src/./game", "-f", filename, "-df", str(3), "-id" , str(1), "-syn", ">", outputfilename])
    print(commandline)
    os.system(commandline)
