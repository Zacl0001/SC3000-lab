from heapq import heappop, heappush, heapify
import json

with open('G.json', 'r') as file:
    G_node = json.load(file)

with open('Coord.json', 'r') as file:
    coords = json.load(file)

with open('Dist.json', 'r') as file:
    distpair = json.load(file)

with open('Cost.json', 'r') as file:
    cost = json.load(file)

def dfs(maxenergy, start, end):
    totaldist = {start: 0}
    energy = {start: 0}
    parent = {}
    nextqueue = []
    heappush(nextqueue, (0, start))
    while len(nextqueue) != 0:
        accdist, cur = heappop(nextqueue)
        if cur == end:
            path = []
            node = end
            path.append(node)
            while node in parent:
                node = parent[node]
                path.append(node)
            path.reverse()
            return path, totaldist[end], energy[end]
        for node in G_node[cur]:
            pair = cur + "," + node
            if cost[pair] + energy[cur] > maxenergy:
                continue
            elif node not in totaldist or distpair[pair] + accdist < totaldist[node]:
                totaldist[node] = distpair[pair] + accdist
                energy[node] = cost[pair] + energy[cur]
                parent[node] = cur
                heappush(nextqueue, (totaldist[node], node)) 
    return None, -1, -1    
        


energy = 287932
S, T = '1', '50'
path, min_dist, total_energy = dfs(energy, S, T)
if path is None:
    print("No path available")
else:
    print("Shortest path: ", end="")
    print("->".join(path))
    print(f"Shortest distance: {min_dist}")
    print(f"Total energy cost: {total_energy}")