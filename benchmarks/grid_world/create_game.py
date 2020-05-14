from game import Location, State
from config import *

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
    if state.robot_turn:
        sum = sum + 1 * exponent #Even or odd to encode whose turn it is
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
    return neighbors

def loc_free_in_s(loc, s):
    for l in s.human_locs:
        if loc.row == l.row and loc.col == l.col:
            return False
    return True

def get_reward(loc):
    for l in goal_locs:
        if loc.row == l.row and loc.col == l.col:
            return pos_reward
    return 0

def gen_human_moves(s): #TODO: generalize to n humans
    moves = []
    curr_loc = s.human_locs[0]
    neighs = get_neighbor_cells(curr_loc)
    for n in neighs:
        newState = State([n], s.robot_locs.copy(), True)
        moves.append(newState)
    return moves

def gen_moves(s):
    moves = []
    rewards = []
    if (not s.robot_turn):  # Human turn
        moves = gen_human_moves(s)
        rewards = [neg_reward] * len(moves)
    else: # Robot turn
        curr_loc = s.robot_locs[0]
        neighs = get_neighbor_cells(curr_loc)
        for n in neighs:
            if loc_free_in_s(n,s):
                newState = State(s.human_locs.copy(), [n], False)
                moves.append(newState)
                rewards.append(get_reward(n))
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
initial_state = State([human_loc], [robot_loc], False)

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