import os
import sys

benchmark = [(5,5), (5,10), (5,15), (6,6), (6,12), (6,18), (10,10), (10,15), (10,20), (10,30)]

for (i,j) in benchmark:
    filename = "../benchmarks/"+str(i)+"_"+str(j)+".txt"
    command = " ".join(["python3 ../benchmarks/create_game.py", str(i), str(i), str(j), str(-1), ">", filename])
    print(command)
    os.system(command)
