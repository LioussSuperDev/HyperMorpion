class Player(object):
    def __init__(self,name):
        self.name = name
        self.player_number = None
    def play(self, grid):
        return NotImplementedError()
    def set_player_number(self,n):
        self.player_number = n