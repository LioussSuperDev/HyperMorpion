class Player(object):
    def __init__(self,name,player_number):
        self.name = name
        self.player_number = player_number
    def play(self, grid):
        return NotImplementedError()