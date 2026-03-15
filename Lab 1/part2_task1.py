import numpy as np

#grid setup
grid_size = 5
gamma = 0.9 #discount factor
theta = 1e-4 #stopping threshold
goal = (4,4)
roadblocks = [(2,1),(2,3)]

actions = {
    "U":(1,0),
    "D":(-1,0),
    "L":(0,-1),
    "R":(0,1)
}

#stochastic Movement
perpendicular = {
    "U":["L","R"],
    "D":["L","R"],
    "L":["U","D"],
    "R":["U","D"]
}

#helper functions
#ensure movement is inside grid/ not a roadblock
def valid_state(y,x):
    if y<0 or y>=grid_size or x<0 or x>=grid_size:
        return False
    if (y,x) in roadblocks:
        return False
    return True


def move(state, action):
    if state == goal:
        return state

    y, x = state
    action_y, action_x = actions[action]
    new_y, new_x = y + action_y, x + action_x

    if valid_state(new_y, new_x):
        return (new_y, new_x)
    return state


def terminal(state):
    return state == goal or state in roadblocks


def expected_value(V, state, action):
    total = 0
    probs = [(0.8, action),
             (0.1, perpendicular[action][0]),
             (0.1, perpendicular[action][1])]

    for p, act in probs:
        new_state = move(state, act)
        reward = 10 if new_state == goal else -1
        y, x = new_state
        total += p * (reward + gamma * V[y, x])
    return total


def get_best_action(V, state):
    best_value = -1e9
    best_action = None
    for a in actions:
        val = expected_value(V, state, a)
        if val > best_value:
            best_value = val
            best_action = a
    return best_action, best_value


def print_grid(V):
    for y in reversed(range(grid_size)):  # top to bottom
        row = []
        for x in range(grid_size):
            if (y, x) == goal:
                row.append(f"{'GOAL': >5}")
            elif (y, x) in roadblocks:
                row.append(f"{'####':>5}")
            else:
                row.append(f"{V[y, x]:5.2f}")  # index by (y,x)
        print("\t".join(row))
    print("-" * 40)

def print_policy(policy):
    for y in reversed(range(grid_size)):
        row = [policy[y, x] for x in range(grid_size)]
        print("\t".join(row))
    print("-" * 40)

#-----------------
#value iteration
#-----------------
print("\nValue Iteration\n")
V = np.zeros((grid_size,grid_size))
policy = np.empty((grid_size, grid_size), dtype=str)
for y, x in roadblocks:
    policy[y, x] = "#"
policy[goal] = "G"

iteration = 1
while True:
    delta = 0
    for y in range(grid_size):
        for x in range(grid_size):
            state = (y, x)
            if terminal (state):
                continue

            best_action, best_value = get_best_action(V,state)
            delta = max(delta,abs(V[y, x] - best_value)) #tracks largest change
            V[y, x] = best_value
            policy[y, x] = best_action

    print(f"Value Iteration Round {iteration}:")
    print_grid(V)
    if delta < theta: #value stops changing then stop
        break
    iteration +=1

#print final policy
print("Optimal Policy from Value Iteration:")
print_policy(policy)

#-----------------
#policy iteration
#-----------------
print("\nPolicy Iteration\n")
#step up initial policy
policy_pi = np.full((grid_size, grid_size), "U", dtype=str)
for y, x in roadblocks:
    policy_pi[y, x] = "#"
policy_pi[goal] = "G"

V_pi = np.zeros((grid_size, grid_size))
stable = False
iteration = 1

while not stable:
    #policy evaluation
    while True:
        delta = 0
        for y in range(grid_size):
            for x in range(grid_size):
                state = (y,x)
                if terminal(state):
                    continue

                v = V_pi[y, x]
                V_pi[y, x] = expected_value(V_pi, state, policy_pi[y, x])
                delta = max(delta, abs(v - V_pi[y, x]))
        if delta < theta:
            break

    # policy improvement
    stable = True
    for y in range(grid_size):
        for x in range(grid_size):
            state = (y,x)
            if terminal(state):
                continue
            old_action = policy_pi[y, x]
            best_action, _ = get_best_action(V_pi, state) #no need for best value
            policy_pi[y, x] = best_action
            if old_action != best_action:
                stable = False

    print(f"Policy Iteration Round {iteration}:")
    print_grid(V_pi)
    iteration += 1

#print final policy
print("Optimal Policy from Policy Iteration:")
print_policy(policy_pi)