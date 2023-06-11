import sys
import numpy as np
sys.path.append('../../')
from player import Player
from utils import *
import random

class RandomPlayer(Player):

    def __init__(self,name):
        self.name = name

    def play(self, grid, macroX, macroY):
        avaible = []
        for i in range(3):
            for j in range(3):
                if grid[macroX,macroY,i,j] == 0:
                    avaible.append((i,j))
        bx,by = random.choice(avaible)
        print("IA playing",(bx,by))
        return bx,by