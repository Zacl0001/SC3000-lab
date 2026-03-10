gamma = 0.9

def move_up(x,y):
    if y == 4:
        return y
    y += 1
    if (x == 1 or x == 3) and y == 2:
        y -= 1
    return y

def move_down(x,y):
    if y == 0:
        return y
    y -= 1
    if (x == 1 or x == 3) and y == 2:
        y += 1
    return y

def move_left(x,y):
    if x == 0:
        return x
    x -= 1
    if (x == 1 or x == 3) and y == 2:
        x += 1
    return x

def move_right(x,y):
    if x == 4:
        return x
    x += 1
    if (x == 1 or x == 3) and y == 2:
        x -= 1
    return x  

q_table = [[[0 for _ in range(4)] for _ in range(5)] for _ in range(5)]
v_table = [[0 for _ in range(5)] for _ in range(5)]
reward_table = [[-1 for _ in range(5)] for _ in range(5)]
reward_table[4][4] = 9
#a_0: up, a_1: left, a_2: down, a_3: right
#(1,2) and (3,2) are not accessible

for i in range(1,100):
    for x in range(5):
        for y in range(5):
            if (x == 1 or x == 3) and y == 2:
                continue
            elif x == 4 and y == 4:
                v_table[x][y] = 0
                continue
            y_up = move_up(x,y)
            y_down = move_down(x,y)
            x_left = move_left(x,y)
            x_right = move_right(x,y)
            q_table[x][y][0] = 0.8*(reward_table[x][y_up]+gamma*v_table[x][y_up])+0.1*(reward_table[x_left][y]+gamma*v_table[x_left][y])+0.1*(reward_table[x_right][y]+gamma*v_table[x_right][y])
            q_table[x][y][1] = 0.8*(reward_table[x_left][y]+gamma*v_table[x_left][y])+0.1*(reward_table[x][y_down]+gamma*v_table[x][y_down])+0.1*(reward_table[x][y_up]+gamma*v_table[x][y_up])
            q_table[x][y][2] = 0.8*(reward_table[x][y_down]+gamma*v_table[x][y_down])+0.1*(reward_table[x_left][y]+gamma*v_table[x_left][y])+0.1*(reward_table[x_right][y]+gamma*v_table[x_right][y])
            q_table[x][y][3] = 0.8*(reward_table[x_right][y]+gamma*v_table[x_right][y])+0.1*(reward_table[x][y_down]+gamma*v_table[x][y_down])+0.1*(reward_table[x][y_up]+gamma*v_table[x][y_up])
            v_table[x][y] = max(q_table[x][y])
    print()
    print(f"Value table (iteration {i}):")
    for x in range(5):
        for y in range(5):
            if (x == 1 or x == 3) and y == 2:
                continue
            print(f"v({x},{y}): {v_table[x][y]}; ", end="")
        print()
