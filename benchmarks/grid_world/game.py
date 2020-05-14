class Location:
    row = 0
    col = 0

    def __init__(self, r, c):
        self.row = r
        self.col = c

    def __str__(self):
        return f'<{self.row},{self.col}>'

class State:
    human_locs = []
    robot_locs = []
    robot_turn = False
    neighbors = []
    rewards = []

    def __init__(self, human_locs, robot_locs, robot_turn):
        self.human_locs = human_locs
        self.robot_locs = robot_locs
        self.robot_turn = robot_turn
        self.neighbors = []
        self.rewards = []

    def __str__(self):
        s = ""
        for l in self.human_locs:
            s = s + str(l) + ", "
        for l in self.robot_locs:
            s = s + str(l) + ", "
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
        return True

    def __hash__(self): #TODO: give a perfect hash function
        return hash((self.human_locs[0], self.robot_locs[0], self.robot_turn))