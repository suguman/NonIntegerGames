
from config_file import placement_requirements, grasp_requirements, place_limits, num_objects, num_place_locs, initial_state_list

class State:
    obj_locs = []
    human_turn = False
    neighbors = []

    def __init__(self):
        self.obj_locs=[]
        self.human_turn = False
        self.neighbors=[]

    def to_int(self):
        r = 0
        power = 1
        for i in range(len(self.obj_locs)):
            r = r + self.obj_locs[i] * power
            power = power*num_place_locs
        i = 0
        if self.human_turn:
            i = 1
        r = r + i * power
        return r

# Ensure all placement requirement locations are occupied
# And the destination placement is unoccupied
def isLegalPlacement(loc_index, state):
    loc_list = placement_requirements[loc_index]
    for loc in loc_list:
        loc_occupied = False
        for i in state.obj_locs:
            if i == loc:
                loc_occupied = True
                continue
        if loc_occupied:
            continue
        else:
            return False

    place_counts = [0]*num_place_locs
    for l in state.obj_locs:
        place_counts[l] = place_counts[l]+1

    if place_counts[loc_index] >= place_limits[loc_index]:
        return False
    return True

#Ensure no objects obstruct the grasp
def isLegalGrasp(loc_index, state):
    loc_list = grasp_requirements[loc_index]
    for loc in loc_list:
        for i in state.obj_locs:
            if i == loc:
                return False
    return True

def get_state_neighbors(state):
    neighbs = []
    graspable_objs = []
    for obj_i in range(len(state.obj_locs)):
        if isLegalGrasp(state.obj_locs[obj_i], state):
            graspable_objs.append(obj_i)
    legal_places = []
    for loc in range(num_place_locs):
        if isLegalPlacement(loc, state):
            legal_places.append(loc)    
    for obj_i in graspable_objs:
        for loc in legal_places:
            s_prime = State()
            s_prime.obj_locs = state.obj_locs.copy()
            s_prime.human_turn = not state.human_turn
            s_prime.obj_locs[obj_i] = loc
            neighbs.append(s_prime)
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
        i = -1
    print(str(counter)+" "+str(i))

print("# transitions")
for s in game_states:
    i = 1
    if s.human_turn:
        i = -1
    for n in s.neighbors:
        print(str(state_to_int_map[s.to_int()])+" "+str(state_to_int_map[n.to_int()])+" "+str(i))