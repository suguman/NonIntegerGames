
from config_file import length, width, speed, insertion_frequency, initial_state_list, Location, positive_reward, negative_reward, human_reward

import copy


class State:
    obj_locs = []
    human_turn = False
    human_loc = Location(int(length/2), width-1)
    robot_loc = Location(1,0)
    neighbors = []

    def __init__(self):
        self.obj_locs=[]
        self.human_turn = False
        self.neighbors=[]

    def to_int(self):
        r = 0
        power = 1
        for i in range(len(self.obj_locs)):
            r = r + self.obj_locs[i].to_int() * power
            power = power*length*width
        r = r + self.robot_loc.to_int() * power
        power = power * length*width

        r = r + self.human_loc.to_int() * power
        power = power * length*width
        i = 0
        if self.human_turn:
            i = 1
        r = r + i * power
        return r


#We allow repeats in the ELSE region (region 1) only
def nChooseKHelper(l, n, remaining_k):
    if remaining_k == 0:
        return l
    else:
        all_lists = []
        for i in range(n):
            if( i == 1 or (not i in l)):
                new_list = l.copy()
                new_list.append(i)
                all_lists.append(nChooseKHelper(new_list, n, remaining_k-1))
        if remaining_k > 1:
            r = []
            for a in all_lists:
                for b in a:
                    r.append(b)
            return r
        else:
            return all_lists

def getNChooseKChoices(n, k):
    return nChooseKHelper([], n, k)

#Does not change the turn
def gen_states_for_new_spawns(state):
    objs_to_spawn = []
    for i in range(len(state.obj_locs)):
        if state.obj_locs[i].row == length-1:
            objs_to_spawn.append(i)
    
    spawns = getNChooseKChoices(width-1, len(objs_to_spawn))

    neighbs = []
    for s in spawns:
        s_prime = State()
        s_prime.obj_locs = copy.deepcopy(state.obj_locs)
        count = 0
        for i in range(len(state.obj_locs)):
            if state.obj_locs[i].row == length-1:
                s_prime.obj_locs[i] = Location(0,s[count])
                count += 1
        s_prime.human_turn = state.human_turn
        s_prime.robot_loc = state.robot_loc#.copy()
        s_prime.human_loc = state.human_loc#.copy()
        neighbs.append(s_prime)

    if len(neighbs) == 0:
        neighbs.append(state)

    return neighbs


def gen_state_for_new_human_loc(state, new_loc):

    intermediate_neighbs = gen_states_for_new_spawns(state)
    neighbs = []
    for s in intermediate_neighbs:
        picked_object = False
        for i in range(len(s.obj_locs)):
            if s.obj_locs[i] == new_loc:
                s_prime = State()
                s_prime.obj_locs = copy.deepcopy(s.obj_locs)
                s_prime.obj_locs[i] = Location(s.obj_locs[i].row, length-1)
                s_prime.human_turn = not s.human_turn
                s_prime.robot_loc = s.robot_loc#.copy()
                s_prime.human_loc = new_loc#.copy()
                neighbs.append(s_prime)
                picked_object = True

        if not picked_object:
            s_prime = State()
            s_prime.obj_locs = copy.deepcopy(s.obj_locs)
            s_prime.human_turn = not s.human_turn
            s_prime.robot_loc = s.robot_loc#.copy()
            s_prime.human_loc = new_loc#.copy()
            neighbs.append(s_prime)
    return neighbs

def gen_state_for_new_robot_loc(state, new_loc):
    neighbs = []
    picked_object = False

    new_obj_locs = copy.deepcopy(state.obj_locs)
    for i in range(len(state.obj_locs)):
        if state.obj_locs[i].row < length-1:
            new_obj_locs[i].row = state.obj_locs[i].row+1

    for i in range(len(state.obj_locs)):
        if state.obj_locs[i] == new_loc:
            s_prime = State()
            s_prime.obj_locs = copy.deepcopy(new_obj_locs)
            s_prime.obj_locs[i] = Location(state.obj_locs[i].row, length-1)
            s_prime.human_turn = not state.human_turn
            s_prime.robot_loc = state.robot_loc#.copy()
            s_prime.human_loc = new_loc#.copy()
            neighbs.append(s_prime)
            picked_object = True

    if not picked_object:
        s_prime = State()
        s_prime.obj_locs = copy.deepcopy(new_obj_locs)
        s_prime.human_turn = not state.human_turn
        s_prime.robot_loc = new_loc#.copy()
        s_prime.human_loc = state.human_loc#.copy()
        neighbs.append(s_prime)
    return neighbs

#We test to see if they human arm or the robot arm overlap
#We model them as line segments extending from opposite sides of the conveyor belt
def is_valid_loc(human_loc, robot_loc):
    if human_loc.row == robot_loc.row:
        if human_loc.col <= robot_loc.col:
            return False
    return True

def get_state_neighbors(state):
    neighbs = []

    if state.human_turn:
        hl = state.human_loc
        if hl.row > 0:
            new_loc = Location(hl.row-1, hl.col)
            if is_valid_loc(new_loc, state.robot_loc):
                neighbs = neighbs + gen_state_for_new_human_loc(state, new_loc)
        if hl.col > 1: #The human never goes to the top slot
            new_loc = Location(hl.row, hl.col-1)
            if is_valid_loc(new_loc, state.robot_loc):
                neighbs = neighbs + gen_state_for_new_human_loc(state, new_loc)
        if hl.row < length-1:
            new_loc = Location(hl.row+1, hl.col)
            if is_valid_loc(new_loc, state.robot_loc):
                neighbs = neighbs + gen_state_for_new_human_loc(state, new_loc)
        if hl.col < width-1:
            new_loc = Location(hl.row, hl.col+1)
            if is_valid_loc(new_loc, state.robot_loc):
                neighbs = neighbs + gen_state_for_new_human_loc(state, new_loc)
        state.neighbors = neighbs
        return neighbs
    else:
        rl = state.robot_loc
        if rl.row > 0:
            new_loc = Location(rl.row-1, rl.col)
            if is_valid_loc(state.human_loc, new_loc):
                neighbs = neighbs + gen_state_for_new_robot_loc(state, new_loc)
        if rl.col > 0:
            new_loc = Location(rl.row, rl.col-1)
            if is_valid_loc(state.human_loc, new_loc):
                neighbs = neighbs + gen_state_for_new_robot_loc(state, new_loc)
        if rl.row < length-1:
            new_loc = Location(rl.row+1, rl.col)
            if is_valid_loc(state.human_loc, new_loc):
                neighbs = neighbs + gen_state_for_new_robot_loc(state, new_loc)
        if rl.col < width-1:
            new_loc = Location(rl.row, rl.col+1)
            if is_valid_loc(state.human_loc, new_loc):
                neighbs = neighbs + gen_state_for_new_robot_loc(state, new_loc)
        state.neighbors = neighbs
        return neighbs


def build_game(init_state):
    init_state_str = init_state.to_int()

    state_count=1
    visited_states = {init_state_str:state_count}

    curr_frontier = []
    all_states = []

    curr_frontier.append(init_state)

    while(len(curr_frontier) > 0):
        #remove state from frontier and add to visited states
        s = curr_frontier[-1]
        curr_frontier.pop()
        my_tpl = {s.to_int() : state_count}
        state_count+=1
        visited_states.update(my_tpl)
        all_states.append(s)
        #check all neighbors and add new ones to frontier
        neighbors = get_state_neighbors(s)
        for n in neighbors:
            if n.to_int() in visited_states:
                pass
            else:
                curr_frontier.append(n)
    return all_states


initial_state = State()
for obj_loc in initial_state_list:
    initial_state.obj_locs.append(obj_loc)
    initial_state.human_turn=True

game_states = build_game(initial_state)
state_to_int_map = {}
counter = 0
print("# states")
for s in game_states:
    state_to_int_map[s.to_int()] = counter
    counter += 1
    i = 1
    if s.human_turn:
        i = 0
    print(str(counter)+" "+str(i))

print("# transitions")
for s in game_states:
    # i = 1
    # if s.human_turn:
    #     i = -1

    for n in s.neighbors:
        reward = 0
        #We compare current block locs to next hand locs because the blocks update when hands move
        for l in s.obj_locs:
            if n.robot_loc == l:
                reward = reward + positive_reward
            elif n.human_loc == l:
                reward = reward + human_reward
            elif l.row >= length-2:
                reward = reward + negative_reward #we add because it's negative
            else:
                pass
        print(str(state_to_int_map[s.to_int()])+" "+str(state_to_int_map[n.to_int()])+" "+str(reward))