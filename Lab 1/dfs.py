from heapq import heappop, heappush, heapify
import json

with open('G.json', 'r') as file:
    G_details = json.load(file)

with open('Coord.json', 'r') as file:
    coords = json.load(file)

with open('Dist.json', 'r') as file:
    distpair = json.load(file)

def dfs(maxenergy):
    start, end = '1', '50'
    distances = {}
    energy = {}
    prev = {}
    distances["1"] = 0
    energy["1"] = 0
    current = '0'
    nextqueue = [(0, "0,1")]
    visited = []
    i = 0
    prev['1'] = 0
    while current != end and len(nextqueue) != 0:
        newdist, pair = heappop(nextqueue)
        current, next = pair.split(",")
        #print(f"newdist = {newdist} and current = {current} and next = {next}")
        if next not in visited:
            visited.append(next)
            current = next
            neighbouring = G_details[current]
            d = distances[current]
            for x in neighbouring:
                if x in visited:
                    continue
                pair = current + "," + x
                #print(f"{pair} and distance: {distpair[pair]}")
                if x not in distances:
                    distances[x] = d+distpair[pair]
                    heappush(nextqueue, (distpair[pair], pair))
                    prev[x] = current
                elif d + distpair[pair] < distances[x]:
                    distances[x] = d+distpair[pair]
                    prev[x] = current
            print(current)

    print(distances["2"])
    return prev, distances["50"]


def printpath(prev, node):
    if prev[node] == 0:
        return node
    else:
        return printpath(prev, prev[node]) + "->" + (node)

energy = 287932
prev, w = dfs(energy)
print(w)
print(printpath(prev, '50'))