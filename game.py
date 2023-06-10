import numpy as np
import sys
from players.human.human_player import HumanPlayer
from players.bot.stockfish import StockFish
from utils import *
import os

sys.stdout.reconfigure(encoding='utf-8')

class HyperMorpion(object):

    def __init__(self, player1, player2):
        self._grid = np.zeros((3,3,3,3))
        self._grid_winners = np.zeros((3,3))
        self.players = [player1,player2]
        self.next_macro_x,self.next_macro_y = 1,1
        player1.set_player_number(1)
        player2.set_player_number(2)

    def get_state_of_micro_grid(self,macroX,macroY):
        if self._grid_winners[macroX,macroY] != 0:
            return self._grid_winners[macroX,macroY]
        self._grid_winners[macroX,macroY] = get_state_of_micro_grid(self._grid,macroX,macroY)
        return self._grid_winners[macroX,macroY]
    
    def get_state_of_macro_grid(self):
        return get_state_of_macro_grid(self._grid)
    
    def int_to_string_array(self):
        returned = np.empty((3,3,3,3), dtype=str)
        for i in range(self._grid.shape[0]):
            for j in range(self._grid.shape[1]):
                for k in range(self._grid.shape[2]):
                    for l in range(self._grid.shape[3]):
                        char = self._grid[i,j,k,l]
                        if char == 0:
                            returned[i,j,k,l] = " "
                        elif char == 1:
                            returned[i,j,k,l] = "X"
                        elif char == 2:
                            returned[i,j,k,l] = "O"
        return returned
    
    def print_board(self):
        cg = self.int_to_string_array()
        print("╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗")
        print("║ {} │ {} │ {} ║ {} │ {} │ {} ║ {} │ {} │ {} ║".format(cg[0,0,0,0],cg[0,0,0,1],cg[0,0,0,2],cg[0,1,0,0],cg[0,1,0,1],cg[0,1,0,2],cg[0,2,0,0],cg[0,2,0,1],cg[0,2,0,2]))
        print("╟───┼───┼───╫───┼───┼───╫───┼───┼───║")
        print("║ {} │ {} │ {} ║ {} │ {} │ {} ║ {} │ {} │ {} ║".format(cg[0,0,1,0],cg[0,0,1,1],cg[0,0,1,2],cg[0,1,1,0],cg[0,1,1,1],cg[0,1,1,2],cg[0,2,1,0],cg[0,2,1,1],cg[0,2,1,2]))
        print("╟───┼───┼───╫───┼───┼───╫───┼───┼───║")
        print("║ {} │ {} │ {} ║ {} │ {} │ {} ║ {} │ {} │ {} ║".format(cg[0,0,2,0],cg[0,0,2,1],cg[0,0,2,2],cg[0,1,2,0],cg[0,1,2,1],cg[0,1,2,2],cg[0,2,2,0],cg[0,2,2,1],cg[0,2,2,2]))
        print("║═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══║")
        print("║ {} │ {} │ {} ║ {} │ {} │ {} ║ {} │ {} │ {} ║".format(cg[1,0,0,0],cg[1,0,0,1],cg[1,0,0,2],cg[1,1,0,0],cg[1,1,0,1],cg[1,1,0,2],cg[1,2,0,0],cg[1,2,0,1],cg[1,2,0,2]))
        print("╟───┼───┼───╫───┼───┼───╫───┼───┼───║")
        print("║ {} │ {} │ {} ║ {} │ {} │ {} ║ {} │ {} │ {} ║".format(cg[1,0,1,0],cg[1,0,1,1],cg[1,0,1,2],cg[1,1,1,0],cg[1,1,1,1],cg[1,1,1,2],cg[1,2,1,0],cg[1,2,1,1],cg[1,2,1,2]))
        print("╟───┼───┼───╫───┼───┼───╫───┼───┼───║")
        print("║ {} │ {} │ {} ║ {} │ {} │ {} ║ {} │ {} │ {} ║".format(cg[1,0,2,0],cg[1,0,2,1],cg[1,0,2,2],cg[1,1,2,0],cg[1,1,2,1],cg[1,1,2,2],cg[1,2,2,0],cg[1,2,2,1],cg[1,2,2,2]))
        print("║═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══║")
        print("║ {} │ {} │ {} ║ {} │ {} │ {} ║ {} │ {} │ {} ║".format(cg[2,0,0,0],cg[2,0,0,1],cg[2,0,0,2],cg[2,1,0,0],cg[2,1,0,1],cg[2,1,0,2],cg[2,2,0,0],cg[2,2,0,1],cg[2,2,0,2]))
        print("╟───┼───┼───╫───┼───┼───╫───┼───┼───║")
        print("║ {} │ {} │ {} ║ {} │ {} │ {} ║ {} │ {} │ {} ║".format(cg[2,0,1,0],cg[2,0,1,1],cg[2,0,1,2],cg[2,1,1,0],cg[2,1,1,1],cg[2,1,1,2],cg[2,2,1,0],cg[2,2,1,1],cg[2,2,1,2]))
        print("╟───┼───┼───╫───┼───┼───╫───┼───┼───║")
        print("║ {} │ {} │ {} ║ {} │ {} │ {} ║ {} │ {} │ {} ║".format(cg[2,0,2,0],cg[2,0,2,1],cg[2,0,2,2],cg[2,1,2,0],cg[2,1,2,1],cg[2,1,2,2],cg[2,2,2,0],cg[2,2,2,1],cg[2,2,2,2]))
        print("╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝")
    
    def play(self):
        continues = 0
        continues2 = 0
        while continues == 0 and continues2 == 0:
            for i,p in enumerate(self.players):
                #os.system('cls' if os.name == 'nt' else 'clear')
                self.print_board()
                x,y = self.next_macro_x,self.next_macro_y
                self.next_macro_x,self.next_macro_y = p.play(self._grid,x,y)
                self._grid[x,y,self.next_macro_x,self.next_macro_y] = (i+1)
                continues = self.get_state_of_macro_grid()
                continues2 = is_filled_micro_grid(self._grid,self.next_macro_x,self.next_macro_y)
                if continues != 0 or continues2:
                    break
        self.print_board()
        if continues == -1 or (continues == 0 and continues2):
            print("Jeu nul.")
        else:
            print("Joueur",continues,"gagnant !")


p1,p2 = StockFish("H1",5),StockFish("SF",5)
#p1,p2 = HumanPlayer("H1"),StockFish("SF",10)
game = HyperMorpion(p1,p2)
game.play()