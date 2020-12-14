import os
import sys

gridsize = [(4,4), (6,6), (8,8), (10,10)]
weights = [(5,-1), (10,-2), (10,-1), (18,-2)]
gridsize = [(8,8)]
weights = [(5,-1),(10,-2)]

for (r,c) in gridsize:
    for (p,n) in weights:
        
        filename = "../benchmarks/social_dist/"+"_".join([str(r),str(c),str(p),str(-1*n)])+".txt"
        #command = " ".join(["python3 ../benchmarks/create_game.py", str(r), str(c), str(p), str(n), ">", filename])
        #print(command)
        #os.system(command)
        for df in [2,3]:
            outputfilename = "../outputs/social_dist/" +  "_".join([str(r),str(c),str(p),str(-1*n), str(df)])+".txt"
            runprogram = " ".join(["timeout 2400 time", "../src/./game", "-df", str(df), "-id 1 -syn -f", filename, ">", outputfilename])
            print(runprogram)
            #os.system(runprogram)
