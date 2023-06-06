import time
import util

def Approx(G):
    print('Approximation ...\n')

    start = time.time()

    degree_dict = {}
    degree_list = list(G.degree())
    for i in range(len(degree_list)):
        degree_list[i] = list(degree_list[i])
        degree_dict[degree_list[i][0]] = degree_list[i][1]
    degree_list = sorted(degree_list, key=lambda x:x[0])
    MVC = set()
    max_node = max(degree_dict.items(), key=lambda x: x[1])[0]


    while degree_dict[max_node] > 0:
        degree_dict[max_node] = 0
        MVC.add(max_node)
        for node in G.neighbors(max_node):
            degree_dict[node] -= 1
        max_node = max(degree_dict.items(), key=lambda x: x[1])[0]
    runtime = time.time() - start
    trace = [str(runtime) + ',' + str(len(MVC))]
    return MVC, trace

def main(file, time, seed, alg):
    G, N, E = util.generateGraph(file)
    MVC, trace = Approx(G)
    util.generateOutput(MVC, trace, file, alg, time, seed)
    return len(MVC)

