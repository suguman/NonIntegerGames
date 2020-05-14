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


def main():
    if len(sys.argv) != 5:
        print("visualize_game robot_row robot_col human_row human_col")
        quit(1)

    robot_r = int(sys.argv[1])
    robot_c = int(sys.argv[2])
    human_r = int(sys.argv[3])
    human_c = int(sys.argv[4])

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

    plt.show()

if __name__ == "__main__":
    main()