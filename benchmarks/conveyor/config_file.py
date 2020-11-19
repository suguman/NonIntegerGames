width = 3
length = 5 # We use the last row to denote objects the human can place next turn
#Really we should only use one location for this

speed = 1

insertion_frequency = 1.0/2

positive_reward = 100 #when the robot grasps an object
negative_reward = -1 #When an object falls off the end
human_reward = 0 #Reward when a human grabs an object (currently not optional for the human)


class Location:
    row = 0
    col = 0

    def __init__(self, r, c):
        self.row = r
        self.col = c

    def __str__(self):
        return f'<{self.row},{self.col}>'

    def to_int(self):
        return self.row * width + self.col

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col


initial_state_list = [Location(0,0), Location(0,3)]