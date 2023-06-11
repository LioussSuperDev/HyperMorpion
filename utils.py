def get_state_of_micro_grid(grid,macroX,macroY,grid_winners=None):
    if grid_winners != None and grid_winners[macroX,macroY] != 0:
        return grid_winners[macroX,macroY]
    filled = True
    for i in range(3):
        ok_1,ok_2 = True,True
        for j in range(3):
            if grid[macroX,macroY,i,j] != 1:
                ok_1 = False
            if grid[macroX,macroY,i,j] != 2:
                ok_2 = False
            if grid[macroX,macroY,i,j] == 0:
                filled = False
        if ok_1:
            if grid_winners != None:
                grid_winners[macroX,macroY] = 1
            return 1
        if ok_2:
            if grid_winners != None:
                grid_winners[macroX,macroY] = 2
            return 2
    for j in range(3):
        ok_1,ok_2 = True,True
        for i in range(3):
            if grid[macroX,macroY,i,j] != 1:
                ok_1 = False
            if grid[macroX,macroY,i,j] != 2:
                ok_2 = False
        if ok_1:
            if grid_winners != None:
                grid_winners[macroX,macroY] = 1
            return 1
        if ok_2:
            if grid_winners != None:
                grid_winners[macroX,macroY] = 2
            return 2
    if grid[macroX,macroY,1,1] == 1:
        if (grid[macroX,macroY,0,2] == 1 and grid[macroX,macroY,2,0]) == 1 or (grid[macroX,macroY,0,0] == 1 and grid[macroX,macroY,2,2] == 1):
            if grid_winners != None:
                grid_winners[macroX,macroY] = 1
            return 1
    if grid[macroX,macroY,1,1] == 2:
        if (grid[macroX,macroY,0,2] == 2 and grid[macroX,macroY,2,0]) == 2 or (grid[macroX,macroY,0,0] == 2 and grid[macroX,macroY,2,2] == 2):
            if grid_winners != None:
                grid_winners[macroX,macroY] = 2
            return 2
    if filled:
        if grid_winners != None:
            grid_winners[macroX,macroY] = -1
        return -1
    return 0

def get_state_of_macro_grid(grid):
    filled = True
    for i in range(3):
        ok_1,ok_2 = True,True
        for j in range(3):
            if get_state_of_micro_grid(grid,i,j) != 1:
                ok_1 = False
            if get_state_of_micro_grid(grid,i,j) != 2:
                ok_2 = False
            if get_state_of_micro_grid(grid,i,j) == 0:
                filled = False
        if ok_1:
            return 1
        if ok_2:
            return 2
    for j in range(3):
        ok_1,ok_2 = True,True
        for i in range(3):
            if get_state_of_micro_grid(grid,i,j) != 1:
                ok_1 = False
            if get_state_of_micro_grid(grid,i,j) != 2:
                ok_2 = False
        if ok_1:
            return 1
        if ok_2:
            return 2
    if get_state_of_micro_grid(grid,1,1) == 1:
        if (get_state_of_micro_grid(grid,0,2) == 1 and get_state_of_micro_grid(grid,2,0) == 1) or (get_state_of_micro_grid(grid,0,0) == 1 and get_state_of_micro_grid(grid,2,2) == 1):
            return 1
    if get_state_of_micro_grid(grid,1,1) == 2:
        if (get_state_of_micro_grid(grid,0,2) == 2 and get_state_of_micro_grid(grid,2,0) == 2) or (get_state_of_micro_grid(grid,0,0) == 2 and get_state_of_micro_grid(grid,2,2) == 2):
            return 2
    if filled:
        return -1
    return 0

def is_empty_grid(grid):
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    if grid[i,j,k,l] != 0:
                        return False
    return True

def is_filled_micro_grid(grid, macroX, macroY):
    for i in range(3):
        for j in range(3):
            if grid[macroX, macroY, i, j] == 0:
                return False
    return True

def get_number_of_possible_lines_micro(grid, macroX, macroY, x, y, player_number):
    horiz,vert,diag1,diag2=1,1,1,1
    nhoriz,nvert,ndiag1,ndiag2=0,0,0,0
    for i in range(3):
        if not (grid[macroX,macroY,x,i] == 0 or grid[macroX,macroY,x,i] == player_number):
            horiz = 0
        if not (grid[macroX,macroY,i,y] == 0 or grid[macroX,macroY,i,y] == player_number):
            vert = 0
        if grid[macroX,macroY,x,i] == player_number:
            nhoriz+=1
        if grid[macroX,macroY,i,y] == player_number:
            nvert+=1
    if not (x == y and x == 1):
        return horiz+vert,nhoriz+nvert
    for i in range(3):
        if not (grid[macroX,macroY,i,i] == 0 or grid[macroX,macroY,i,i] == player_number):
            diag1 = 0
        if not (grid[macroX,macroY,2-i,i] == 0 or grid[macroX,macroY,2-i,i] == player_number):
            diag2 = 0
        if grid[macroX,macroY,i,i] == player_number:
            nhoriz+=1
        if grid[macroX,macroY,2-i,i] == player_number:
            nvert+=1
    return horiz+vert+diag1+diag2,nhoriz+nvert+ndiag1+ndiag2

def get_number_of_possible_lines_macro(grid, x, y, player_number):
    horiz,vert,diag1,diag2=1,1,1,1
    nhoriz,nvert,ndiag1,ndiag2=0,0,0,0
    for i in range(3):
        xi = get_state_of_micro_grid(grid,x,i)
        iy = get_state_of_micro_grid(grid,i,y)
        if not (xi == 0 or xi == player_number):
            horiz = 0
        if not (iy == 0 or iy == player_number):
            vert = 0
        if xi == player_number:
            nhoriz+=1
        if iy == player_number:
            nvert+=1
    if not (x == y and x == 1):
        return horiz+vert,nhoriz,nvert
    for i in range(3):
        ii = get_state_of_micro_grid(grid,i,i)
        i2i = get_state_of_micro_grid(grid,2-i,i)
        if not (ii == 0 or ii == player_number):
            diag1 = 0
        if not (i2i == 0 or i2i == player_number):
            diag2 = 0
        if ii == player_number:
            ndiag1+=1
        if i2i == player_number:
            ndiag2+=1
    return horiz+vert+diag1+diag2,nhoriz+nvert+ndiag1+ndiag2