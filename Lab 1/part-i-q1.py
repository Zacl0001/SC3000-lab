import heapq
import json
from math import inf
from pathlib import Path


def load_json(file_path: Path):
    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def edge_distance(dist, u, v):
    key = f"{u},{v}"
    return dist[key]


def dijkstra_shortest_path(graph: dict, dist, start, goal):
    start = str(start)
    goal = str(goal)

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
        return inf, []

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = previous[node]
    path.reverse()

    return distances[goal], path


def main():
    graph = load_json(Path("G.json"))
    dist = load_json(Path("Dist.json"))

    start = input("Enter start node: ").strip()
    goal = input("Enter goal node: ").strip()

    total_distance, path = dijkstra_shortest_path(graph, dist, start, goal)

    if not path:
        print(f"No path found from {start} to {goal}.")
        return

    print(f"Shortest distance: {total_distance}")
    print("Path:", " -> ".join(path))


if __name__ == "__main__":
    main()
