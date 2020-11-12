width = 3
length = 11 # We use the last row to denote objects the human can place next turn

speed = 1

insertion_frequency = 1.0/2


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


initial_state_list = [Location(0,0), Location(0,3)]