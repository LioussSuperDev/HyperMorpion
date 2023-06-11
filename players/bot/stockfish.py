import sys
import numpy as np
sys.path.append('../../')
from player import Player
from utils import *
class StockFish(Player):

    def __init__(self,name,depth):
        self.name = name
        self.depth = depth

    def play(self, grid, macroX, macroY):
        first_turn = is_empty_grid(grid)
        bscore,bx,by,path = self._play(first_turn, grid, macroX, macroY, self.depth, self.player_number)
        print("IA playing",(bx,by),"for a score of",bscore,"(path :",path,")")
        return bx,by

    def evaluate(self,old_grid,grid,macroX,macroY,x,y,player_number,defense_score=0.25):
        new_macro = get_state_of_macro_grid(grid)
        old = get_state_of_micro_grid(old_grid,macroX,macroY)
        new = get_state_of_micro_grid(grid,macroX,macroY)

        if new_macro == player_number:
            return 999999
        elif new_macro == -1:
            return -50
        elif (new == -1 and old == 0) or old == -1:
            return -1
        
        maold = get_number_of_possible_lines_macro(old_grid,macroX,macroY,player_number)
        maold2 = get_number_of_possible_lines_macro(old_grid,macroX,macroY,3-player_number)
        manew2 = get_number_of_possible_lines_macro(grid,macroX,macroY,3-player_number)
        maold,maold2,manew2 = maold[0]*maold[1],maold2[0]*maold[1],manew2[0]*maold[1]

        if old == 0 and new == player_number:
            return 50*((1-defense_score)*maold+defense_score*(maold2-manew2))
        
        miold = get_number_of_possible_lines_micro(old_grid,macroX,macroY,x,y,player_number)
        miold2 = get_number_of_possible_lines_micro(old_grid,macroX,macroY,x,y,3-player_number)
        minew2 = get_number_of_possible_lines_micro(grid,macroX,macroY,x,y,3-player_number)
        miold,miold2,minew2 = miold[0]*miold[1],miold2[0]*miold2[1],minew2[0]*minew2[1]

        return (1-defense_score)*miold*maold+defense_score*(miold2*maold2-minew2*manew2)

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
                        if played[0] != None:
                            score -= played[0]
                            _path = played[3]
                    if bscore == None or score > bscore:
                        bx,by,bscore,path = i,j,score,_path
        if bx == None:
            for i in range(3):
                for j in range(3):
                    if (grid[macroX,macroY,i,j] == 0):
                        bx,by,bscore,path = i,j,None,[]
        return bscore,bx,by,(path.copy()+[(bx,by)])