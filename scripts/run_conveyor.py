import os
import sys

gridsize = [(3,4)]
weights = [(5,-1)]
#gridsize = [(8,8)]
#weights = [(10,-2)]

for (r,c) in gridsize:
    for (p,n) in weights:
        print("\n")
        filename = "../benchmarks/conveyor/"+"_".join([str(r),str(c),str(p),str(-1*n)])+".txt"
        command = " ".join(["python3 ../benchmarks/conveyor/create_game.py", str(r), str(c), str(p), str(n), ">", filename])
        print(command)
        os.system(command)
        for df in [2]:
            outputfilename = "../outputs/conveyor/" +  "_".join([str(r),str(c),str(p),str(-1*n), str(df)])+".txt"
            runprogram = " ".join(["timeout 2000 time", "../src/./game", "-df", str(df), "-id 1 -syn -f", filename, ">", outputfilename])
            print(runprogram)
            os.system(runprogram)
