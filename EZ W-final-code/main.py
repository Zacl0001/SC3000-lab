import json
import heapq
from math import inf, sqrt
import  time

energy_budget = 287932

def edge_distance(dist, u, v):
    key = f"{u},{v}"
    return dist[key]


def edge_energy_cost(cost, u, v):
    key = f"{u},{v}"
    return cost[key]


def path_energy_cost(path, cost):
    total = 0
    for i in range(len(path) - 1):
        total += edge_energy_cost(cost, path[i], path[i + 1])
    return total


def ucs_no_energy(graph: dict, dist, start, goal):
    start = str(start)
    goal = str(goal)

    nodes_expanded = 0

    if start not in graph:
        raise ValueError(f"Start node '{start}' not found in graph")
    if goal not in graph:
        raise ValueError(f"Goal node '{goal}' not found in graph")

    distances = {node: inf for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0

    min_heap = [(0, start)]

    while min_heap:
        current_dist, u = heapq.heappop(min_heap)

        nodes_expanded += 1

        if current_dist > distances[u]:
            continue

        if u == goal:
            break

        for v in graph.get(u, []):
            v = str(v)
            weight = edge_distance(dist, u, v)
            candidate = current_dist + weight

            if candidate < distances.get(v, inf):
                distances[v] = candidate
                previous[v] = u
                heapq.heappush(min_heap, (candidate, v))

    if distances.get(goal, inf) == inf:
        return inf, [], nodes_expanded
    
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = previous[node]
    path.reverse()

    return distances[goal], path, nodes_expanded


def heuristic(v, goal, Coord):
    # Define heuristic
    '''
    Computes Euclidean distance between node and goal.
    Straight line distance represents minimum possible distance between 2 points.
    '''
    # Good heuristic as prioritises nodes closer to goal
    x1, y1 = Coord[str(v)]
    x2, y2 = Coord[str(goal)]
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def ucs_with_energy(G, Dist, Cost, start, goal):
    # Initialise priority queue
    open_set = []
    heapq.heappush(open_set, (0, start))

    # Track costs
    totaldist = {start: 0} # Distance from start node to this node
    energy_score = {start: 0} # Total energy consumed to reach this node
    parent = {}

    # Track number of nodes expanded
    nodes_expanded = 0

    while open_set:
        dist, current = heapq.heappop(open_set) # Pop node with the lowest total distance (most promising node)
        nodes_expanded +=1

        if current == goal:
            # Reconstruct path by following parent pointers from goal back to start
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse()
            return totaldist[goal], path,  nodes_expanded
        # Explore neighbours
        for neighbour in G[current]:
            # Compute tentative distance and energy cost to the neighbour
            tentative_dist = totaldist[current] + Dist[f"{current},{neighbour}"]
            tentative_energy = energy_score[current] + Cost[f"{current},{neighbour}"]

            # Skip this path if the energy budget would be exceeded
            if tentative_energy > energy_budget:
                continue
            # Update if this path to the neighbour is shorter than any previously found
            elif neighbour not in totaldist or tentative_dist < totaldist[neighbour]:
                totaldist[neighbour] = tentative_dist
                energy_score[neighbour] = tentative_energy
                parent[neighbour] = current
                heapq.heappush(open_set, (tentative_dist, neighbour))

    # Return None if no valid path satisfies the energy constraint
    return inf, None, nodes_expanded

# Run A*
def astar(G, Coord, Dist, Cost, start, goal):
    # Initialise priority queue
    open_set = []
    heapq.heappush(open_set, (0, start))

    # Track costs
    g_score = {start: 0} # Distance from start node to this node
    energy_score = {start: 0} # Total energy consumed to reach this node
    parent = {}

    # Track number of nodes expanded
    nodes_expanded = 0

    while open_set:
        f, current = heapq.heappop(open_set) # Pop node with the lowest f_score (most promising node)

        nodes_expanded += 1

        if current == goal:
            # Reconstruct path by following parent pointers from goal back to start
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            path.append(start)
            path.reverse()
            return g_score[goal], path, nodes_expanded

        # Explore neighbour
        for neighbour in G[current]:

            # Compute tentative distance and energy cost to the neighbour
            tentative_g = g_score[current] + Dist[f"{current},{neighbour}"]
            tentative_energy = energy_score[current] + Cost[f"{current},{neighbour}"]

            # Skip this path if the energy budget would be exceeded
            if tentative_energy > energy_budget:
                continue

            # Update if this path to the neighbour is shorter than any previously found
            if neighbour not in g_score or tentative_g < g_score[neighbour]:
                g_score[neighbour] = tentative_g
                energy_score[neighbour] = tentative_energy
                parent[neighbour] = current

                # Compute A* priority: f(n) = g(n) + h(n)
                # where g(n) is the distance so far and h(n) is the heuristic estimate to the goal
                f_score = tentative_g + heuristic(neighbour, goal, Coord)

                heapq.heappush(open_set, (f_score, neighbour))

    # Return None if no valid path satisfies the energy constraint
    return inf, None, nodes_expanded

def runtime(func, runs, *args):
    total = 0

    for _ in range(runs):
        start = time.perf_counter()
        func(*args)
        total += time.perf_counter() - start

    return total / runs


def main():
    # Load files
    with open("G.json", "r") as file:
        G = json.load(file)
    with open("Coord.json", "r") as file:
        Coord = json.load(file)
    with open("Dist.json", "r") as file:
        Dist = json.load(file)
    with open("Cost.json", "r") as file:
        Cost = json.load(file)

    print("-----PART 1-----")
    start = input("Enter start node: ").strip()
    goal = input("Enter goal node: ").strip()
    runs = int(input("Enter number of runs (for runtime calc): ").strip())

    # task 1: no energy constraint
    print("\n-----TASK 1-----")

    total_distance, path, nodes = ucs_no_energy(G, Dist, start, goal)
    avg_runtime = runtime(ucs_no_energy, runs, G, Dist, start, goal)

    if path is None:
        print(f"No path found from {start} to {goal}.")
    else:
        print("Shortest path:", "->".join(path))
        print(f"Shortest distance: {total_distance}")
        print(f"Total energy cost: {path_energy_cost(path, Cost)}")
        print(f"Nodes expanded: {nodes}")
        print(f"Average runtime over {runs} runs: {avg_runtime:.6f} seconds")

    #task 2: Uninformed search algorithm
    print("\n-----TASK 2-----")
    total_distance, path, nodes = ucs_with_energy(G, Dist, Cost, start, goal)
    avg_runtime = runtime(ucs_with_energy, runs, G, Dist, Cost, start, goal)

    if path is None:
        print(f"No path found from {start} to {goal}.")
    else:
        print("Shortest path:", "->".join(path))
        print(f"Shortest distance: {total_distance}")
        print(f"Total energy cost: {path_energy_cost(path, Cost)}")
        print(f"Nodes expanded: {nodes}")
        print(f"average runtime over {runs} runs: {avg_runtime:.6f} seconds")

    #task 3: A* Search algorithm
    print("\n-----TASK 3-----")
    total_distance, path, nodes = astar(G, Coord, Dist, Cost, start, goal)
    avg_runtime = runtime(astar, runs, G, Coord, Dist, Cost, start, goal)

    if path is None:
        print(f"No path found from {start} to {goal}.")
    else:
        print("Shortest path:", "->".join(path))
        print("Shortest distance:", total_distance)
        print(f"Total energy cost: {path_energy_cost(path, Cost)}")
        print(f"Nodes expanded: {nodes}")
        print(f"Average runtime over {runs} runs: {avg_runtime:.6f} seconds")

if __name__ == "__main__": 
    main()