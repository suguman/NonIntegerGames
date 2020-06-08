from game import Location, State
from config import num_cols, num_rows, num_humans, num_robots, goal_locs, temporal_goal_locs, obstacles
# import create_game

# import tkinter
#
# from matplotlib.backends.backend_tkagg import (
#     FigureCanvasTkAgg, NavigationToolbar2Tk)
# # Implement the default Matplotlib key bindings.
# from matplotlib.backend_bases import key_press_handler
# from matplotlib.figure import Figure
#
# import numpy as np

import sys

import matplotlib.pyplot as plt
import matplotlib.lines as mlines

def draw_grid():
    ax = plt.gca()
    old_r = 0
    old_c = 0
    for r in range(num_rows+1):
        l = mlines.Line2D([0, num_cols], [r, r])
        ax.add_line(l)
    for c in range(num_cols+1):
        l = mlines.Line2D([c,c],[0,num_rows])
        ax.add_line(l)

def row_col2x_y(rc):
    x = 0.5 + rc.row
    y = 0.5 + rc.col
    return[x,y]

def draw_state(s):
    robot_points = [row_col2x_y(rc) for rc in s.robot_locs]
    x = [p[0] for p in robot_points]
    y = [p[1] for p in robot_points]
    ax = plt.gca()
    ax.scatter(x, y, marker='h', color='blue')

    human_points = [row_col2x_y(rc) for rc in s.human_locs]
    x = [p[0] for p in human_points]
    y = [p[1] for p in human_points]
    ax = plt.gca()
    ax.scatter(x, y, marker='o', color='red')


def draw_obs():
    obs_points = [row_col2x_y(rc) for rc in obstacles]
    x = [p[0] for p in obs_points]
    y = [p[1] for p in obs_points]
    ax = plt.gca()
    ax.scatter(x, y, marker='s', color='grey')

def draw_arrow(cell1,cell2,line_color):
    ax = plt.gca()
    p1 = row_col2x_y(cell1)
    p2 = row_col2x_y(cell2)
    l = mlines.Line2D(p1,p2)
    l.set_color(line_color)
    ax.add_line(l)

def load_strategy(filename):
    file = open(filename, 'r')
    lines = file.readlines()

    strategy = {}

    for l in lines:
        s = l.split("-->")
        if len(s) != 2:
            #skip non-strategy lines
            continue
        else:
            str1 = s[0]
            str2 = s[1]
            tmp = str1.split(",")
            state1 = tmp[0]
            aut1=tmp[1]
            state2=state1
            aut2=aut1
            if str2 != " Any action \n":
                tmp = str2.split(",")
                if len(tmp) != 2:
                    print("ERROR")
                    print(tmp)
                state2 = tmp[0]
                aut2=tmp[1]
            
            strategy[(int(state1),int(aut1))] = (int(state2), int(aut2))
    return strategy

def load_int_to_state_mapping(filename):
    file = open(filename, 'r')
    lines = file.readlines()

    int2locs = {}

    for l in lines:
        s = l.split(",")
        if len(s) != 5:
            #skip non-strategy lines
            continue
        else:
            int2locs[int(s[0])] = (int(s[1]),int(s[2]),int(s[3]),int(s[4]))
    return int2locs

def draw_move_human_loc():
    pass

def draw_next_k_ply(strategy, int2locs, k):
    state = 1
    aut = 0
    robot_turn = True
    for i in range(k):
        next_state,next_aut = strategy[(state, aut)]
        print(state)
        print(int2locs[state])
        if robot_turn:
            draw_arrow(Location(int2locs[state][0], int2locs[state][1]), Location(int2locs[next_state][0], int2locs[next_state][1]), 'blue')
        else:
            draw_arrow(Location(int2locs[state][2], int2locs[state][3]), Location(int2locs[next_state][2], int2locs[next_state][3]), 'red')
        robot_turn = not robot_turn
        state = next_state
        aut = next_aut

def main():
    if len(sys.argv) != 7:
        print("visualize_game robot_row robot_col human_row human_col strategy_file mapping_file")
        quit(1)

    robot_r = int(sys.argv[1])
    robot_c = int(sys.argv[2])
    human_r = int(sys.argv[3])
    human_c = int(sys.argv[4])

    strat = load_strategy(sys.argv[5])
    int2state = load_int_to_state_mapping(sys.argv[6])

    #silliness to make matplotlib work
    x=[0,0]
    y=[0,0]
    plt.plot(x,y)

    draw_grid()


    goal_points = [row_col2x_y(rc) for rc in goal_locs]
    x = [p[0] for p in goal_points]
    y = [p[1] for p in goal_points]
    ax=plt.gca()
    ax.scatter(x,y, marker='p', color='green')

    if(len(temporal_goal_locs) > 0):
        goal_points = [row_col2x_y(rc) for rc in temporal_goal_locs]
        x = [p[0] for p in goal_points]
        y = [p[1] for p in goal_points]
        ax=plt.gca()
        ax.scatter(x,y, marker='^', color='green')

    draw_obs()

    s = State([Location(robot_r, robot_c)],[Location(human_r,human_c)],True)

    draw_state(s)

    draw_next_k_ply(strat, int2state, 10)

    plt.show()

if __name__ == "__main__":
    main()