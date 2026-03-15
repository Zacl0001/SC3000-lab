import random
import statistics

# seed can be changed to alter the initial arbitrary policy, and also the behaviour of epsilon-greedy

GAMMA = 0.9

def get_action(x, y, pi): 
    '''input the coordinates of a state  
    output action based on policy pi (note that this is an epsilon-soft policy)'''
    policy_action = pi[x][y]
    prob_float = random.random()
    # epsilon = 0.1
    if policy_action == "U": 
        if 0 <= prob_float < 0.925: return "U"
        elif 0.925 <= prob_float < 0.950: return "D"
        elif 0.950 <= prob_float < 0.975: return "L"
        else: return "R" 
    elif policy_action == "D": 
        if 0 <= prob_float < 0.925: return "D"
        elif 0.925 <= prob_float < 0.950: return "U"
        elif 0.950 <= prob_float < 0.975: return "L"
        else: return "R" 
    elif policy_action == "L": 
        if 0 <= prob_float < 0.925: return "L"
        elif 0.925 <= prob_float < 0.950: return "R"
        elif 0.950 <= prob_float < 0.975: return "U"
        else: return "D" 
    else: 
        if 0 <= prob_float < 0.925: return "R"
        elif 0.925 <= prob_float < 0.950: return "L"
        elif 0.950 <= prob_float < 0.975: return "U"
        else: return "D" 

def get_next_state(x, y, action: str, stochastic: bool): 
    '''
    input the coordinates of the current state and the action to take  
    input whether stochastic transition is involved for getting the next state
    output the coordinates of the next state
    (note that stochastic transition causes the intended action to execute not as planned)
    '''
    def reach_roadblock(x, y): # x is row, y is col
        if (x == 2 and y == 1) or (x == 2 and y == 3): 
            return True 
        return False 
    
    def move_left(x, y): 
        if y == 0: 
            return x, y
        new_y = y - 1
        if reach_roadblock(x, new_y): 
            return x, y
        return x, new_y

    def move_right(x, y): 
        if y == 4: 
            return x, y
        new_y = y + 1
        if reach_roadblock(x, new_y): 
            return x, y
        return x, new_y

    def move_up(x, y): 
        if x == 4: 
            return x, y
        new_x = x + 1
        if reach_roadblock(new_x, y): 
            return x, y
        return new_x, y

    def move_down(x, y): 
        if x == 0: 
            return x, y
        new_x = x - 1
        if reach_roadblock(new_x, y): 
            return x, y
        return new_x, y

    prob_float = random.random()
    if action == "U": 
        if stochastic == False or 0 <= prob_float < 0.8: return move_up(x, y)
        elif 0.8 <= prob_float < 0.9: return move_left(x, y)
        else: return move_right(x, y)
    elif action == "D": 
        if stochastic == False or 0 <= prob_float < 0.8: return move_down(x, y)
        elif 0.8 <= prob_float < 0.9: return move_left(x, y)
        else: return move_right(x, y)
    elif action == "L": 
        if stochastic == False or 0 <= prob_float < 0.8: return move_left(x, y)
        elif 0.8 <= prob_float < 0.9: return move_up(x, y)
        else: return move_down(x, y)
    else: 
        if stochastic == False or 0 <= prob_float < 0.8: return move_right(x, y)
        elif 0.8 <= prob_float < 0.9: return move_up(x, y)
        else: return move_down(x, y)

def print_q_table(q_table): 
    for i in range(5): 
        for j in range(5):
            if (i == 2 and j == 1) or (i == 2 and j == 3) or (i == 4 and j == 4): 
                continue
            print(f"Q(({i},{j}),U) = {q_table[i][j]["U"]:.3f}, Q(({i},{j}),D) = {q_table[i][j]["D"]:.3f}, Q(({i},{j}),L) = {q_table[i][j]["L"]:.3f}, Q(({i},{j}),R) = {q_table[i][j]["R"]:.3f}")

def print_policy(pi): 
    for i in range(4, -1, -1): 
        for j in range(5): 
            print(pi[i][j], end="   ")
        print()

def generate_episode(pi, reward_table): 
    x,y = 0,0
    episode = [(0,0)]

    while x != 4 or y != 4: 
        action = get_action(x, y, pi)
        x,y = get_next_state(x, y, action, True)
        reward = reward_table[x][y]
        episode.extend([action, reward, (x,y)])

    return episode

#   0     1    2    3      4    5   6     7    8     9    10   11    12
# [(0,0), "U", -1, (1,0), "R", -1, (1,1), "L", -1, (1,0), "R", -1, (1,1)]
#   S0    A0   R1    S1   A1   R2   S2    A2   R3    S3   A3   R4   S4
# len(episode) = 3n+1 = n(state, action, next_reward) + final_state = 13

def calculate_rewards(episode, sample_returns, q_table): 
    length = len(episode)
    final_index = length-2 # initialise final_index to be the final reward
    i = 2

    while i <= final_index:
        # We use the coordinates, rewards and actions for each state for the new q value calculation
        x,y = episode[i-2]
        action = episode[i-1]
        reward = episode[i]   
        # alpha = 0.1
        x_next,y_next = get_next_state(x, y, action, False)
        qmax = max(q_table[x_next][y_next]["U"], q_table[x_next][y_next]["D"], q_table[x_next][y_next]["L"], q_table[x_next][y_next]["R"])
        q_table[x][y][action] = q_table[x][y][action] + 0.1 * (reward + GAMMA * qmax - q_table[x][y][action])
        i += 3
    


def update_policy(pi, q_table): 
    '''update the whole policy based on q_table while being greedy'''
    for i in range(5): 
        for j in range(5): 
            if (
                (i == 2 and j == 1) or 
                (i == 2 and j == 3) or 
                (i == 4 and j == 4)
            ):
                continue
            pi[i][j] = max(q_table[i][j], key=q_table[i][j].get)

def initialise_policy(pi, my_seed): 
    for i in range(5):
        for j in range(5): 
            choice = random.randint(1, 4)
            if choice == 1: 
                pi[i][j] = "U"
            elif choice == 2: 
                pi[i][j] = "D"
            elif choice == 3: 
                pi[i][j] = "L"
            else: 
                pi[i][j] = "R"
    pi[2][1] = "X"
    pi[2][3] = "X"
    pi[4][4] = "X"
    
    print(f"Initial policy (seed = {my_seed}): ")
    print_policy(pi)
    print("\n\n")

    input("Proceed? ")

def main():
    # configuration: ask for user input on no. of episodes and seed 
    no_of_episodes = int(input("Enter the number of episodes: "))
    my_seed = int(input("Enter the seed: "))
    random.seed(my_seed)

    # initialisation
    # for q_table, sample_returns, pi, disregard (2,1), (2,3), (4,4)
    q_table = [[{"U":0, "D":0, "L":0, "R":0} for _ in range(5)] for _ in range(5)]
    sample_returns = [[{"U":[], "D":[], "L":[], "R":[]} for _ in range(5)] for _ in range(5)]
    pi = [[None for _ in range(5)] for _ in range(5)]
    reward_table = ((-1, -1, -1, -1, -1), (-1, -1, -1, -1, -1), (-1, None, -1, None, -1), (-1, -1, -1, -1, -1), (-1, -1, -1, -1, 9))

    # initialise an arbitrary policy
    initialise_policy(pi, my_seed)

    for num in range(no_of_episodes): 
        # generate an episode using pi
        episode = generate_episode(pi, reward_table)
        # calculate mean rewards for each state-action pair in the episode 
        calculate_rewards(episode, sample_returns, q_table)
        # update policy
        update_policy(pi, q_table)

        # print results
        print_q_table(q_table)
        print(f"Policy after {num+1} episodes (seed = {my_seed}): ")
        print_policy(pi)
        print("\n\n")
    
if __name__ == "__main__": 
    main()