import time
import copy
import random
from collections import deque, defaultdict
from queue import PriorityQueue
from collections import OrderedDict
import util
import numpy as np
## python code/main.py -inst data/football.graph -alg LS2 -time 2.0 -seed 10

def removing(C, graph, vertices, confChange, dscores, uncovered_edges, vertex):
    dscores[vertex] *= -1
    neighbors = graph[vertex]
    for neighbor in neighbors:
        neighbor = int(neighbor)
        if neighbor in C:
            dscores[neighbor] -= 1
        else:
            uncovered_edges.append((vertex, neighbor))
            uncovered_edges.append((neighbor, vertex))
            dscores[neighbor] += 1


def adding(C, graph, vertices, confChange, dscores, uncovered_edges, vertex):
    dscores[vertex] *= -1
    neighbors = graph[vertex]
    for neighbor in neighbors:
        neighbor = int(neighbor)
        if neighbor in C:
            dscores[neighbor] += 1
        else:
            uncovered_edges.remove((vertex, neighbor))
            uncovered_edges.remove((neighbor, vertex))
            dscores[neighbor] -= 1


def finder(C, dscores):
    u = None
    max_temp = -float('inf')
    for i in C:
        if dscores[i] > max_temp:
            max_temp = dscores[i]
            # choose a vertex u from C with the highest dscore
            u = i
    return u


def HillClimbing(graph, vertices, cutoff_time, seed):
    start_time = time.time()
    uncovered_edges = []
    trace = []
    graph_copy = copy.deepcopy(graph)
    dscores = {}
    confChange = {}
    np.random.seed(seed)
    for v in vertices:
        dscores[int(v)] = 0
        confChange[int(v)] = 1
    # construct C greedily until it is a vertex cover
    timer = time.time()
    C, t = Approximate(graph_copy, vertices, cutoff_time)
    C = list(C)
    # start loop
    counter = 0
    while (time.time() - start_time < cutoff_time) and counter < 50000:
        if len(uncovered_edges) == 0:
            counter = 0
            u = finder(C, dscores)
            C.remove(u)
            trace.append(str(round(time.time() - start_time, 2)) + ' ' + str(len(C)))
            removing(C, graph, vertices, confChange, dscores, uncovered_edges, u)
            print(len(C))
        else:
            counter += 1

            u = finder(C, dscores)
            C.remove(u)
            removing(C, graph, vertices, confChange, dscores, uncovered_edges, u)

            e = random.choice(uncovered_edges)
            vertex = None
            if dscores[e[0]] > dscores[e[1]]:
                vertex = e[0]
            else:
                vertex = e[1]
            C.append(vertex)
            adding(C, graph, vertices, confChange, dscores, uncovered_edges, vertex)

            # w(e) := w(e) + 1 for each uncovered edge e;
            for x in uncovered_edges:
                dscores[x[0]] += 1
    return C, trace


def readfile(filename):
    with open(filename, "r") as f:
        first_line = f.readline()
        num_vertrix = int(first_line.split(" ")[0])
        num_edge = int(first_line.split(" ")[1])
        weight = int(first_line.split(" ")[2])
        graph = defaultdict(list)
        vertices = set()
        index = 1
        for line in f:
            l = line.split(" ")
            for i in l:
                if i != '\n':
                    graph[index].append(i)
                    vertices.add(i)
            index += 1
    return graph, vertices











def Approximate(graph, vertices, cutoff_time):
    start_time = time.time()
    Cover = set()
    trace = []
    size = len(Cover)
    start = max(graph, key = lambda k: len(graph[k]))
    edges = set()
    Cover.add(start)
    for i in graph[start]:
        edges.add(str(start) +'-' + i)
    while time.time() - start_time < cutoff_time and len(Cover) > size:
        size = len(Cover)
        while edges:
            edge = edges.pop()
            v = edge.split('-')[1]
            key =  edge.split('-')[0]
            graph[int(v)].remove(key)
            graph[int(key)].remove(v)
        start = max(graph, key = lambda k: len(graph[k]))
        Cover.add(start)#
        if len(Cover) > size:
            trace.append(str(round(time.time() -start_time ,2)) + ' ' + str(len(Cover)))
        for i in graph[start]:
            edges.add(str(start) +'-' + str(i))
        #print(edges)
    return Cover, trace

def main(file, time, seed, alg):
    G, N, E = util.generateGraph(file)
    graph,vertices = readfile(file)
    MVC, trace = HillClimbing(graph, vertices, time, seed)
    #dicts = '../output/'
    #writefile(dicts, file, MVC, trace)
    util.generateOutput(MVC, trace, file, alg, time, seed)