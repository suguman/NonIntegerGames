## ============================================================================
# Name        : create_game.py
# Author      : Andrew Wells
# Version     :
# Copyright   : Your copyright notice
# Description : Robotics benchmark
## ============================================================================

#We also encode some temporal goals in the states

import sys


class Location:
    row = 0
    col = 0

    def __init__(self, r, c):
        self.row = r
        self.col = c

    def __str__(self):
        return str(self.row) +", "+str(self.col)
        #return f'<{self.row},{self.col}>'


clineinputs = sys.argv

num_rows = int(clineinputs[1])
num_cols = int(clineinputs[2])
num_humans = 1
num_robots = 1
num_locs = num_rows*num_cols


if(num_rows < 6 or num_cols < 6):
    print("We need at least a 6x6 grid")
    exit()

pos_reward = int(clineinputs[3])
neg_reward = int(clineinputs[4])

temporal_goal_locs = [Location(1,num_cols-2), Location(num_rows-2,1)]

goal_locs = [Location(0,num_cols-1), Location(num_rows-1,0)]

center = num_rows/2
obstacles = [Location(center,center), Location(center, center+1), Location(center+1, center), Location(center+1, center+1)]

class State:
    human_locs = []
    robot_locs = []
    robot_turn = False
    neighbors = []
    rewards = []
    temporal_goals_visited = []

    def __init__(self, human_locs, robot_locs, temporal_goals_visited, robot_turn):
        self.human_locs = human_locs
        self.robot_locs = robot_locs
        self.temporal_goals_visited = temporal_goals_visited
        self.robot_turn = robot_turn
        self.neighbors = []
        self.rewards = []

    def __str__(self):
        s = ""
        for l in self.human_locs:
            s = s + str(l) + ", "
        for l in self.robot_locs:
            s = s + str(l) + ", "
        for x in self.temporal_goals_visited:
            s = s + str(x) + ", "
        if self.robot_turn:
            s = s + "1"
        else:
            s = s + "0"
        return s

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.robot_turn != other.robot_turn:
            return False
        for i in len(self.human_locs):
            if self.human_locs[i] != other.human_locs[i]:
                return False
        for i in len(self.robot_locs):
            if self.robot_locs[i] != other.robot_locs[i]:
                return False
        for i in len(self.temporal_goals_visited):
            if self.temporal_goals_visited[i] != other.temporal_goals_visited[i]:
                return False
        return True

    def __hash__(self): #TODO: give a perfect hash function
        return hash((self.human_locs[0], self.robot_locs[0], self.robot_turn, self.temporal_goals_visited[0], self.temporal_goals_visited[1]))


#Map location to integer
def loc2i(loc):
    return (loc.row+1) * num_rows + loc.col+1

#Map state to integer
def s2i(state):
    exponent = 1
    sum = loc2i(state.robot_locs[0]) * exponent
    exponent = exponent * num_locs
    for i in range(num_humans):
        sum = sum + loc2i(state.human_locs[i]) * exponent
        exponent = exponent * num_locs
    for i in range(len(temporal_goal_locs)):
        if state.temporal_goals_visited[i]:
            sum = sum + 1 * exponent
        exponent = exponent * 2
    if state.robot_turn:
        sum = sum + 1 * exponent
    return sum

def print_states(states, state_map):
    for s in states:
        # print(s)
        if s.robot_turn:
            print(str(state_map[s2i(s)]) + " 1")
        else:
            print(str(state_map[s2i(s)]) + " 0")

def print_transitions(states, state_map):
    for s in states:
        for i in range(len(s.neighbors)):
            print(str(state_map[s2i(s)]) + " " + str(state_map[s2i(s.neighbors[i])]) + " " + str(s.rewards[i]))

def get_neighbor_cells(loc):
    neighbors = []
    if loc.row > 0:
        neighbors.append(Location(loc.row-1, loc.col))
    if loc.col > 0:
        neighbors.append(Location(loc.row, loc.col-1))
    if loc.row < num_rows - 1:
            neighbors.append(Location(loc.row + 1, loc.col))
    if loc.col < num_cols - 1:
        neighbors.append(Location(loc.row, loc.col + 1))

    return [x for x in neighbors if x not in obstacles]

def loc_free_in_s(loc, s):
    for l in s.human_locs:
        if loc.row == l.row and loc.col == l.col:
            return False
    return True

def get_reward(loc, s):
    r = 0
    for l in goal_locs:
        if loc.row == l.row and loc.col == l.col:
            r = pos_reward
    for i in range(len(temporal_goal_locs)):
        if s.temporal_goals_visited[i]:
            continue
        if loc.row == temporal_goal_locs[i].row and loc.col == temporal_goal_locs[i].col:
            r = r + 2*pos_reward
            s.temporal_goals_visited[i] = True
    return r

def manhattan_dist(l1, l2):
    return abs(l1.row-l2.row)+abs(l1.col-l2.col)

def gen_rewards(human_moves):
    r = []
    for m in human_moves:
        r.append(2+(int)(neg_reward / (1+manhattan_dist(m.robot_locs[0], m.human_locs[0]))))
    return r

def gen_human_moves(s): #TODO: generalize to n humans
    moves = []
    curr_loc = s.human_locs[0]
    neighs = get_neighbor_cells(curr_loc)
    for n in neighs:
        newState = State([n], s.robot_locs.copy(), s.temporal_goals_visited.copy(), True)
        moves.append(newState)
    return moves

def gen_moves(s):
    moves = []
    rewards = []
    if (not s.robot_turn):  # Human turn
        moves = gen_human_moves(s)
        rewards = gen_rewards(moves)
    else: # Robot turn
        curr_loc = s.robot_locs[0]
        neighs = get_neighbor_cells(curr_loc)
        for n in neighs:
            if loc_free_in_s(n,s):
                newState = State(s.human_locs.copy(), [n], s.temporal_goals_visited.copy(), False)
                moves.append(newState)
                rewards.append(get_reward(n,newState))
    s.neighbors = moves
    s.rewards = rewards
    return moves


def build_game(init):
    initial_state = init

    horizon = []
    horizon.append(init)

    visited_set = {}
    # vs = {}

    game_states = []

    while(len(horizon) > 0):
        s = horizon.pop()
        game_states.append(s)
        visited_set[s2i(s)] = s
        # vs[s] = s2i(s)

        # print("======We are finishing state: " + str(s))

        gen_moves(s)
        for st in s.neighbors:
            if not (s2i(st) in visited_set):
                horizon.append(st)

            # else:
            #     print("We already visited state: "+str(st))
            #     print(visited_set[s2i(st)])
            #     if not st in vs:
            #         print("Error, the visited set is wrong")

    return game_states

human_loc = Location(num_rows-1, num_cols-1)
robot_loc = Location(0, 0)
initial_state = State([human_loc], [robot_loc], [False] * len(temporal_goal_locs) , False)

states = build_game(initial_state)

state_map = {}
for i in range(len(states)):
    state_map[s2i(states[i])] = i

print("# states")
print_states(states, state_map)
print("# initial state")
print(state_map[s2i(initial_state)])
print("# transitions")
print_transitions(states, state_map)

#print(clineinputs)
#print(num_rows, num_cols, pos_reward, neg_reward)
