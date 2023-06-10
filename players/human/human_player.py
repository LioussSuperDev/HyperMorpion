import sys
# setting path
sys.path.append('../../')
from player import Player

class HumanPlayer(Player):

    def play(self, grid, macroX, macroY):

        valid = False
        while not valid:

            coord = input("Choisissez une coordonnée pour jouer : ("+str(macroX)+", "+str(macroY)+")")

            if coord == "exit":
                exit(0)

            X,Y = int(coord[0]),int(coord[1])

            if X < 0 or Y < 0 or X > 2 or Y > 2:
                print("Position "+coord+" invalide !")
                continue
            

            if grid[macroX,macroY,X,Y] != 0:
                print("Cette case est déjà prise !")
                continue
            
            return X,Y