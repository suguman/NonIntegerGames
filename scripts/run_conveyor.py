import os
import sys

gridsize = [(3,5), (3,6), (3,8), (3,10), (4,5), (4,6), (4,8), (4,10)]
weights = [(10,-1), (10,-2), (10,-3), (10,-4), (10,-5)]
#gridsize = [(8,8)]
#weights = [(10,-2)]

for (r,c) in gridsize:
    for (p,n) in weights:
        print("\n")
        filename = "../benchmarks/conveyor/"+"_".join([str(r),str(c),str(p),str(-1*n)])+".txt"
        command = " ".join(["python3 ../benchmarks/conveyor/create_game.py", str(r), str(c), str(p), str(n), ">", filename])
        print(command)
        os.system(command)
        for df in [2,3]:
            outputfilename = "../outputs/conveyor/" +  "_".join([str(r),str(c),str(p),str(-1*n), str(df)])+".txt"
            runprogram = " ".join(["timeout 2000 time", "../src/./game", "-df", str(df), "-id 1 -syn -f", filename, ">", outputfilename])
            print(runprogram)
            os.system(runprogram)
