import heapq
import math
import json

# STEP 1: Load files
with open("G.json", "r") as f:
    G = json.load(f)

with open("Coord.json", "r") as f:
    Coord = json.load(f)

with open("Dist.json", "r") as f:
    Dist = json.load(f)

with open("Cost.json", "r") as f:
    Cost = json.load(f)

# STEP 2: Define heuristic
# Computes Euclidean distance between node and goal
# Straight line distance represents minimum possible distance between 2 points
# Good heuristic as prioritises nodes closer to goal

def heuristic(v, goal, Coord):
    x1, y1 = Coord[str(v)]
    x2, y2 = Coord[str(goal)]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# STEP 3: Run A*
def astar(G, Coord, Cost, start, goal):
    # Initialise priority queue
    open_set = []
    heapq.heappush(open_set, (0, start))

    # Track costs
    g_score = {start: 0} # Distance from start node to this node
    energy_score = {start: 0} # Total energy consumed to reach this node
    parent = {}

    while open_set:
        f, current = heapq.heappop(open_set) # Pop node with the lowest f_score (most promising node)

        if current == goal:
            # Reconstruct path by following parent pointers from goal back to start
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse()
            return path

        # Explore neighbors
        for neighbor in G[current]:

            # Compute tentative distance and energy cost to the neighbor
            tentative_g = g_score[current] + Dist[f"{current},{neighbor}"]
            tentative_energy = energy_score[current] + Cost[f"{current},{neighbor}"]

            # Skip this path if the energy budget would be exceeded
            if tentative_energy > energy_budget:
                continue

            # Update if this path to the neighbor is shorter than any previously found
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                energy_score[neighbor] = tentative_energy
                parent[neighbor] = current

                # Compute A* priority: f(n) = g(n) + h(n)
                # where g(n) is the distance so far and h(n) is the heuristic estimate to the goal
                f_score = tentative_g + heuristic(neighbor, goal, Coord)

                heapq.heappush(open_set, (f_score, neighbor))

    # Return None if no valid path satisfies the energy constraint
    return None

# Compute total distance and total energy cost of the final path
def compute_metrics(path, Dist, Cost):
    total_dist = 0
    total_energy = 0

    for i in range(len(path)-1):
        v = path[i]
        w = path[i+1]

        total_dist += Dist[f"{v},{w}"]
        total_energy += Cost[f"{v},{w}"]

    return total_dist, total_energy

start = "1"
goal = "50"
energy_budget = 287932
path = astar(G, Coord, Cost, start, goal)

if path is None:
    print("No path found")
else:
    distance, energy = compute_metrics(path, Dist, Cost)

    print("Shortest path:", "->".join(path))
    print("Shortest distance:", distance)
    print("Total energy cost:", energy)