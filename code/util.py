import networkx as nx
import os

def generateGraph(filename):
    with open(filename, 'r') as f:
        file = f.readlines()
    N = file[0][0]
    E = file[0][1]
    G = nx.Graph()
    for line_num, line in enumerate(file):
        data = list(map(lambda x: int(x), line.split()))
        if line_num!=0:
            for adj_nodes in data:
                G.add_edge(line_num, adj_nodes)
    return G,N,E

def generateOutput(MVC, trace, file, alg, time, seed):
    if not os.path.exists('./output'):
        os.makedirs('./output')
    solution = open('./output/' + os.path.splitext(os.path.basename(file))[0] +
                    '_' + alg +
                    '_' + str(time) +
                    '_' + str(seed) +
                    '.sol', 'w')
    solution.write(str(len(MVC)) + '\n')
    solution.write(','.join(map(str, list(MVC))))
    solution.close()
    trace_file = open('./output/' + os.path.splitext(os.path.basename(file))[0] +
                 '_' + alg +
                 '_' + str(time) +
                 '_' + str(seed) +
                 '.trace', 'w')
    for history in trace:
        trace_file.write(history + '\n')
    trace_file.close()