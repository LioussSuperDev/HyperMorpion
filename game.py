import numpy as np
import sys
from players.human.human_player import HumanPlayer
from players.bot.stockfish import StockFish
from players.bot.random import RandomPlayer
from utils import *

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
    
    def get_macro_grid_for_print(self):
        returned = np.empty((3,3), dtype=str)
        for i in range(self._grid.shape[0]):
            for j in range(self._grid.shape[1]):
                char = self.get_state_of_micro_grid(i,j)
                if char == 0:
                    returned[i,j] = " "
                elif char == 1:
                    returned[i,j] = "X"
                elif char == 2:
                    returned[i,j] = "O"
        return returned

    def print_board(self):
        cg = self.int_to_string_array()
        mg = self.get_macro_grid_for_print()
        print("╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗")
        print("║ {} │ {} │ {} ║ {} │ {} │ {} ║ {} │ {} │ {} ║".format(cg[0,0,0,0],cg[0,0,0,1],cg[0,0,0,2],cg[0,1,0,0],cg[0,1,0,1],cg[0,1,0,2],cg[0,2,0,0],cg[0,2,0,1],cg[0,2,0,2]))
        print("╟───┼───┼───╫───┼───┼───╫───┼───┼───╢")
        print("║ {} │ {} │ {} ║ {} │ {} │ {} ║ {} │ {} │ {} ║".format(cg[0,0,1,0],cg[0,0,1,1],cg[0,0,1,2],cg[0,1,1,0],cg[0,1,1,1],cg[0,1,1,2],cg[0,2,1,0],cg[0,2,1,1],cg[0,2,1,2]))
        print("╟───┼───┼───╫───┼───┼───╫───┼───┼───╢")
        print("║ {} │ {} │ {} ║ {} │ {} │ {} ║ {} │ {} │ {} ║".format(cg[0,0,2,0],cg[0,0,2,1],cg[0,0,2,2],cg[0,1,2,0],cg[0,1,2,1],cg[0,1,2,2],cg[0,2,2,0],cg[0,2,2,1],cg[0,2,2,2]))
        print("╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣   ╔═══╦═══╦═══╗")
        print("║ {} │ {} │ {} ║ {} │ {} │ {} ║ {} │ {} │ {} ║   ║ {} ║ {} ║ {} ║".format(cg[1,0,0,0],cg[1,0,0,1],cg[1,0,0,2],cg[1,1,0,0],cg[1,1,0,1],cg[1,1,0,2],cg[1,2,0,0],cg[1,2,0,1],cg[1,2,0,2],mg[0,0],mg[0,1],mg[0,2]))
        print("╟───┼───┼───╫───┼───┼───╫───┼───┼───╢   ╠═══╬═══╬═══╢")
        print("║ {} │ {} │ {} ║ {} │ {} │ {} ║ {} │ {} │ {} ║   ║ {} ║ {} ║ {} ║".format(cg[1,0,1,0],cg[1,0,1,1],cg[1,0,1,2],cg[1,1,1,0],cg[1,1,1,1],cg[1,1,1,2],cg[1,2,1,0],cg[1,2,1,1],cg[1,2,1,2],mg[1,0],mg[1,1],mg[1,2]))
        print("╟───┼───┼───╫───┼───┼───╫───┼───┼───╢   ╠═══╬═══╬═══╢")
        print("║ {} │ {} │ {} ║ {} │ {} │ {} ║ {} │ {} │ {} ║   ║ {} ║ {} ║ {} ║".format(cg[1,0,2,0],cg[1,0,2,1],cg[1,0,2,2],cg[1,1,2,0],cg[1,1,2,1],cg[1,1,2,2],cg[1,2,2,0],cg[1,2,2,1],cg[1,2,2,2],mg[2,0],mg[2,1],mg[2,2]))
        print("╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣   ╚═══╩═══╩═══╝")
        print("║ {} │ {} │ {} ║ {} │ {} │ {} ║ {} │ {} │ {} ║".format(cg[2,0,0,0],cg[2,0,0,1],cg[2,0,0,2],cg[2,1,0,0],cg[2,1,0,1],cg[2,1,0,2],cg[2,2,0,0],cg[2,2,0,1],cg[2,2,0,2]))
        print("╟───┼───┼───╫───┼───┼───╫───┼───┼───╢")
        print("║ {} │ {} │ {} ║ {} │ {} │ {} ║ {} │ {} │ {} ║".format(cg[2,0,1,0],cg[2,0,1,1],cg[2,0,1,2],cg[2,1,1,0],cg[2,1,1,1],cg[2,1,1,2],cg[2,2,1,0],cg[2,2,1,1],cg[2,2,1,2]))
        print("╟───┼───┼───╫───┼───┼───╫───┼───┼───╢")
        print("║ {} │ {} │ {} ║ {} │ {} │ {} ║ {} │ {} │ {} ║".format(cg[2,0,2,0],cg[2,0,2,1],cg[2,0,2,2],cg[2,1,2,0],cg[2,1,2,1],cg[2,1,2,2],cg[2,2,2,0],cg[2,2,2,1],cg[2,2,2,2]))
        print("╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝")
    
    def play(self):
        continues = 0
        grid_filled = False
        while continues == 0 and not grid_filled:
            for i,p in enumerate(self.players):
                self.print_board()
                x,y = self.next_macro_x,self.next_macro_y
                self.next_macro_x,self.next_macro_y = p.play(self._grid,x,y)
                self._grid[x,y,self.next_macro_x,self.next_macro_y] = (i+1)
                continues = self.get_state_of_macro_grid()
                print("continues",continues)
                grid_filled = is_filled_micro_grid(self._grid,self.next_macro_x,self.next_macro_y)
                if continues != 0 or grid_filled:
                    break
        self.print_board()
        if continues == -1 or (continues == 0 and grid_filled):
            print("Jeu nul.")
        else:
            print("Joueur",continues,"gagnant !")


p1,p2 = StockFish("H1",5),StockFish("H1",5)
game = HyperMorpion(p1,p2)
game.play()