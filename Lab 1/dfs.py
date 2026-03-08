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

def dfs(maxenergy):
    start, end = '1', '50'
    totaldist = {start: 0}
    energy = {start: 0}
    parent = {}
    nextqueue = []
    heappush(nextqueue, (0, start))
    while len(nextqueue) != 0:
        accdist, cur = heappop(nextqueue)
        if cur == end:
            break
        for node in G_node[cur]:
            pair = cur + "," + node
            if cost[pair] + energy[cur] > maxenergy:
                continue
            elif node not in totaldist or distpair[pair] + accdist < totaldist[node]:
                totaldist[node] = distpair[pair] + accdist
                energy[node] = cost[pair] + energy[cur]
                heappush(nextqueue, (totaldist[node], node))

    print(totaldist["2"])
    print(f"Energy = {energy["50"]}")
    return totaldist["50"]
        


energy = 287932
w = dfs(energy)
print(w)