def get_state_of_micro_grid(grid,macroX,macroY):
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
            return 1
        if ok_2:
            return 2
    for j in range(3):
        ok_1,ok_2 = True,True
        for i in range(3):
            if grid[macroX,macroY,i,j] != 1:
                ok_1 = False
            if grid[macroX,macroY,i,j] != 2:
                ok_2 = False
        if ok_1:
            return 1
        if ok_2:
            return 2
    if grid[macroX,macroY,1,1] == 1:
        if (grid[macroX,macroY,0,2] == 1 and grid[macroX,macroY,2,0]) == 1 or (grid[macroX,macroY,0,0] == 1 and grid[macroX,macroY,2,2] == 1):
            return 1
    if grid[macroX,macroY,1,1] == 2:
        if (grid[macroX,macroY,0,2] == 2 and grid[macroX,macroY,2,0]) == 2 or (grid[macroX,macroY,0,0] == 2 and grid[macroX,macroY,2,2] == 2):
            return 2
    if filled:
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