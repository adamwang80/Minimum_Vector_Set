import numpy as np
import time
import util

def LS1(graph, cut_time, seed):
    print('Local Search: Simulated Annealing ...\n')

    trace = []
    np.random.seed(seed)
    MVC = set(graph.nodes)
    Temperaute = 1.0
    alpha = 0.95
    start_time = time.time()
    while time.time() - start_time < cut_time:
        notVisited = set(graph.nodes)

        while True:
            if len(notVisited) == 0:
                return
            v = np.random.choice(list(notVisited))
            notVisited.remove(v)
            tmp = MVC.copy()
            if (v in tmp):
                tmp.remove(v)
            else:
                tmp.add(v)
            if isValid(tmp, graph.edges):
                break
        old_cost = len(MVC)
        new_cost = len(tmp)
        prob = np.exp(np.array((old_cost - new_cost) / Temperaute, dtype=np.float128))
        if prob > np.random.random():
            trace.append(str(time.time() - start_time) + ',' + str(new_cost))
            MVC = tmp
        elif new_cost < old_cost:
            trace.append(str(time.time() - start_time) + ',' + str(new_cost))
            MVC = tmp
        Temperaute = Temperaute * alpha

    return MVC, trace


def isValid(S, edges):
    for u, v in edges:
        if (u not in S and v not in S):
            return False
    return True

def main(file, time, seed, alg):
    G, N, E = util.generateGraph(file)
    MVC, trace = LS1(G, time, seed)
    util.generateOutput(MVC, trace, file, alg, time, seed)

