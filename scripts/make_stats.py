import os
import sys


class entry:
    num_rows = 0
    num_cols = 0
    pos_reward = 0
    neg_reward = 0
    discount_factor = 0
    creation_time = 0
    solution_time = 0

    def __init__(self, n_rows, n_cols, p_rew, n_rew, disc_f, cr_time, sol_time):
        self.num_rows = n_rows
        self.num_cols = n_cols
        self.pos_reward = p_rew
        self.neg_reward = "-"+n_rew #because the filename doesn't have a '-'
        self.discount_factor = disc_f
        self.creation_time = cr_time
        self.solution_time = sol_time

    def __lt__(self, other):
        if self.num_rows < other.num_rows:
            return True
        elif self.num_rows > other.num_rows:
            return False
        else:
            if self.num_cols < other.num_cols:
                return True
            elif self.num_cols > other.num_cols:
                return False
            else:
                if self.pos_reward < other.pos_reward:
                    return True
                elif self.pos_reward > other.pos_reward:
                    return False
                else:
                    if self.neg_reward < other.neg_reward:
                        return True
                    elif self.neg_reward > other.neg_reward:
                        return False
                    else:
                        if self.discount_factor < other.discount_factor:
                            return True
                        elif self.discount_factor > other.discount_factor:
                            return False
                        else:
                            return False
#End class

folder_name = sys.argv[1]

files = os.listdir(folder_name)

entries = []

for file_name in files:
    file = open(folder_name+"/"+file_name, 'r')

    creation_time = -1
    solution_time = -1
    for line in file:
        if line.find("Game creation") != -1:
            creation_time = line[line.find(":")+1 : line.find("s")-1]
            creation_time = float(creation_time)
        elif line.find("Game play") != -1:
            solution_time = line[line.find(":")+1 : line.find("s")-1]
            solution_time = float(solution_time)

    params = file_name.split("_")


#TODO, don't assume discount factor is only one digit
    entries.append(entry(params[0], params[1], params[2], params[3], params[4][:-4], creation_time, solution_time))

tmp = folder_name.split("/")
scene_name = tmp[len(tmp)-1]
if len(scene_name) < 1: #If the argument includes a final '/'
    scene_name = tmp[len(tmp)-2]


#Do entries of a given size
#Sort by positive, then negative, then discount factor


entries.sort()

last_sz = ""
last_rew_s = ""

for e in entries:

    sz = str(e.num_rows) +"x"+str(e.num_cols)

    if sz != last_sz:
        if last_sz != "":
            print("\\end{tabular}")
            print("\\end{table*}")
        print("")
        print("")
        print("")
        print("\\begin{table*}[h]")
        print("\\caption{Analysis of "+sz+" "+scene_name+"}")
        print("\\label{table:"+scene_name+"_"+sz+"}")
        print("\\centering")
        print("\\begin{tabular}{|c|c|c|c|}")
        print("\\hline")

        print("\\multicolumn{2}{|c|}{Rewards} &")
        print("  \\multirow{2}{*}{\\begin{tabular}[c]{@{}c@{}}Discount\\\\ factor\\end{tabular}} &")
        print("  \\multirow{2}{*}{\\begin{tabular}[c]{@{}}Total\\\\ time(s)\\end{tabular}} \\\\")

        # print(" Total time \\\\ \\hline")

        # print("  \\multicolumn{3}{c|}{Time taken (in sec.)} \\\\ \cline{1-2} \\cline{4-6} ")
        print("Positive & Negative & & \\\\ \\hline")
        # print("  Negative &")
        # print("   &  & \\\\ \\hline")
        # #print("  \\begin{tabular}[c]{@{}c@{}}Game creation\\\\ (GC)\\end{tabular} &")
        # #print("  \\begin{tabular}[c]{@{}c@{}}Game solving\\\\ (GS)\\end{tabular} &")
        # print("  \\begin{tabular}[c]{@{}c@{}}Total time\\\\ (GC+GS)\\end{tabular} \\\\ \hline")
        last_sz = sz


    if e.creation_time < 0:
        if e.pos_reward+e.neg_reward != last_rew_s:
            print("\\multirow{2}{*}{"+str(e.pos_reward)+"} & \multirow{2}{*}{"+str(e.neg_reward)+"} & "+str(e.discount_factor)+" & --- "+"    \\\\ \\cline{3-4}")
            last_rew_s = e.pos_reward+e.neg_reward
        else:
            print("                   &                     & "+str(e.discount_factor)+" & --- "+"    \\\\ \\hline")
    else:
        if e.pos_reward+e.neg_reward != last_rew_s:
            print("\\multirow{2}{*}{"+str(e.pos_reward)+"} & \multirow{2}{*}{"+str(e.neg_reward)+"} & "+str(e.discount_factor)+" & {:10.3f} ".format(e.creation_time+e.solution_time)+"    \\\\ \\cline{3-4}")
            last_rew_s = e.pos_reward+e.neg_reward
        else:
            print("                   &                     & "+str(e.discount_factor)+" & {:10.3f} ".format(e.creation_time+e.solution_time)+"    \\\\ \\hline")
    
    # if e.creation_time < 0:
    #     if e.pos_reward+e.neg_reward != last_rew_s:
    #         print("\\multirow{2}{*}{"+str(e.pos_reward)+"} & \multirow{2}{*}{"+str(e.neg_reward)+"} & "+str(e.discount_factor)+" & --- & --- & --- "+"    \\\\ \\cline{3-6}")
    #         last_rew_s = e.pos_reward+e.neg_reward
    #     else:
    #         print("                   &                     & "+str(e.discount_factor)+" & --- & --- & --- "+"    \\\\ \\hline")
    # else:
    #     if e.pos_reward+e.neg_reward != last_rew_s:
    #         print("\\multirow{2}{*}{"+str(e.pos_reward)+"} & \multirow{2}{*}{"+str(e.neg_reward)+"} & "+str(e.discount_factor)+" & {:10.3f} & {:10.3f} & {:10.3f} ".format(e.creation_time, e.solution_time, e.creation_time+e.solution_time)+"    \\\\ \\cline{3-6}")
    #         last_rew_s = e.pos_reward+e.neg_reward
    #     else:
    #         print("                   &                     & "+str(e.discount_factor)+" & {:10.3f} & {:10.3f} & {:10.3f} ".format(e.creation_time, e.solution_time, e.creation_time+e.solution_time)+"    \\\\ \\hline")

print("\\end{tabular}")
print("\\end{table*}")
