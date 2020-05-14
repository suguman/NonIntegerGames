from game import Location

num_rows = 10
num_cols = 10
num_humans = 1
num_robots = 1
num_locs = num_rows*num_cols

pos_reward = 15
neg_reward = -1

goal_locs = [Location(0,num_cols-1), Location(num_rows-1,0)]
temporal_goal_locs = [Location(1,num_cols-2), Location(num_rows-2,1)]


center = num_rows/2
obstacles = [Location(center,center), Location(center, center+1), Location(center+1, center), Location(center+1, center+1)]