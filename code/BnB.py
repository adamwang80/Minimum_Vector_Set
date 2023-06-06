import time
import sys
import util

sys.setrecursionlimit(25000)

def BnB(G, cut_time):
    print('Branch and Bound ...\n')

    global graph
    graph = G

    global start
    start = time.time()

    global trace
    trace=[]

    V = list(range(1, len(G.nodes) + 1))
    global first
    global second
    first = dict(zip(V, list(G.nodes)))
    second = dict(zip(list(G.nodes), V))

    degree_list = list(G.degree())
    for i in range(len(degree_list)):
        degree_list[i] = list(degree_list[i])
    degree_list = sorted(degree_list, key=lambda x: x[0])

    upperBound = len(G.nodes)
    lowerBound = upperBound / 2

    uncoveredEdges = list(G.edges)
    covered_set=[]
    uncovered_set=[]
    node_list = list(G.nodes)
    local_minimum = []
    arr=[0]*max(list(G.nodes))

    for n in node_list:
        arr[n-1]=len(G.adj[n])

    min, Cover = bnb(G, upperBound, covered_set, uncovered_set, node_list, local_minimum, len(G.nodes), uncoveredEdges, arr, cut_time)

    if len(Cover)==0:
        Cover=list(G.nodes)

    CoverSet=set(Cover)
    return CoverSet, trace


def bnb(G, upperBound, covered_set, uncovered_set, node_list, local_minimum, num_nodes, uncoveredEdges, arr, cut_time):

    if time.time() - start>=cut_time:
        return upperBound, local_minimum

    if len(covered_set)>=upperBound:
        return upperBound, local_minimum

    if len(uncoveredEdges)==0:
        if len(covered_set)<upperBound:
            local_minimum= covered_set[:]
            upperBound=len(local_minimum)
            trace.append(str(time.time() - start) + ',' + str(upperBound))
        return upperBound, local_minimum

    if len(node_list)==0:
        return upperBound, local_minimum

    lowerbound = len(covered_set) + len(node_list)
    temp=[]
    for i in range(0, len(node_list)):
        temp.append(arr[node_list[i] - 1])
    sorted_temp=[x for _, x in sorted(zip(temp, node_list), reverse=True)]

    sum = 0
    for i in range(0, len(sorted_temp)):
        sum = sum + arr[sorted_temp[i] - 1]
        if sum >= len(uncoveredEdges):
            lowerbound = len(covered_set) + i + 1
            break

    if lowerbound>=upperBound:
        return upperBound, local_minimum

    node_list_new= node_list[:]
    covered_set_new= covered_set[:]
    uncovered_set_new= uncovered_set[:]

    next_node=sorted_temp[0]
    node_list_new.remove(next_node)
    covered_set_new.append(next_node)
    d1= arr[:]
    uncovered_edges_new= uncoveredEdges[:]
    for v in list(G.adj[next_node]):
        d1[v-1]=d1[v-1]-1

        if (v,next_node) in uncovered_edges_new:
            uncovered_edges_new.remove((v,next_node))

        if (next_node,v) in uncovered_edges_new:
            uncovered_edges_new.remove((next_node,v))

    uncovered_set_new.append(next_node)


    upperBound_1, local_minimuim_1 = bnb(G, upperBound, covered_set_new, uncovered_set, node_list_new, local_minimum, num_nodes, uncovered_edges_new, d1, cut_time)
    upperBound2, local_minimum_2 = bnb(G, upperBound_1, covered_set, uncovered_set_new, node_list_new, local_minimuim_1, num_nodes, uncoveredEdges, arr, cut_time)
    return upperBound2, local_minimum_2

def Approx(degree_list):
    degree_dict = {}

    for i in range(len(degree_list)):
        degree_list[i] = list(degree_list[i])
        degree_dict[degree_list[i][0]] = degree_list[i][1]

    MVC = set()
    max_node = max(degree_dict.items(), key=lambda x: x[1])[0]

    while degree_dict[max_node] > 0:
        degree_dict[max_node] = 0
        MVC.add(max_node)
        for node in graph.neighbors(max_node):
            degree_dict[node] -= 1
        max_node = max(degree_dict.items(), key=lambda x: x[1])[0]
    return len(MVC)

def main(file, time, seed, alg):
    G, N, E = util.generateGraph(file)
    MVC, trace = BnB(G, time)
    util.generateOutput(MVC, trace, file, alg, time, seed)



