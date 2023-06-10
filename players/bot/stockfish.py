import sys
import numpy as np
sys.path.append('../../')
from player import Player
from utils import *
class StockFish(Player):

    def __init__(self,name,player_number,depth):
        self.name = name
        self.player_number = player_number
        self.depth = depth

    def play(self, grid, macroX, macroY):
        first_turn = is_empty_grid(grid)
        bscore,bx,by,path = self._play(first_turn, grid, macroX, macroY, self.depth, self.player_number)
        print("IA playing",(bx,by),"for a score of",bscore,"(path :",path,")")
        return bx,by

    def evaluate(self,old_grid,grid,macroX,macroY,x,y,player_number):
        new_macro = get_state_of_macro_grid(grid)
        old = get_state_of_micro_grid(old_grid,macroX,macroY)
        new = get_state_of_micro_grid(grid,macroX,macroY)

        score = 0

        if new_macro == player_number:
            score = 999999
        elif (new == -1 and old == 0) or old == -1:
            score = -1
        elif new == player_number and old == 0:
            score = 50
        elif x == y and x == 1:
            score = 5
        elif x == y or abs(x-y) == 2:
            score = 2
        else:
            score = 1

        if macroX == macroY and macroX == 1:
            score *= 5
        elif macroX == macroY or abs(macroX-macroY) == 2:
            score *= 2

        return score
    
    def _play(self, first_turn, grid, macroX, macroY, depth, player_number):
        bx,by,bscore,path = None,None,None,[]
        for i in range(3):
            for j in range(3):
                if (grid[macroX,macroY,i,j] == 0) and (not (first_turn and (i == macroX) and (j == macroY))) and not is_filled_micro_grid(grid,i,j):
                    c_grid = np.copy(grid)
                    c_grid[macroX,macroY,i,j] = player_number
                    score = self.evaluate(grid,c_grid,macroX,macroY,i,j,player_number)
                    _path = []
                    if depth >= 2 and abs(score) < 1000:
                        played = self._play(False, grid, i, j, depth-1, 3-player_number)
                        score -= played[0]
                        _path = played[3]
                    if bscore == None or score > bscore:
                        bx,by,bscore,path = i,j,score,_path
                    
        return bscore,bx,by,(path.copy()+[(bx,by)])