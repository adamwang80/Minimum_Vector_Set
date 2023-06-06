"""
python code/main.py -inst data/football.graph -alg LS1 -time 2.0 -seed 6
"""

import Approx
import BnB
import LS1
import LS2


import argparse

def main():
    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument('-inst', action='store', type=str, required=True, help='Input graph datafile')
    parser.add_argument('-alg', action='store', type=str, required=True, help='Input Alg  [BnB|Approx|LS1|LS2]')
    parser.add_argument('-time', action='store', default=2.0, type=float, required=False, help='Cutoff running time (s)')
    parser.add_argument('-seed', action='store', default=6, type=int, required=False, help='Random Seed for algorithm')
    args = parser.parse_args()

    alg = args.alg
    file = args.inst
    time = args.time
    seed = args.seed

    if alg == 'Approx':
        Approx.main(file, time, seed, alg)
    elif alg == 'LS1':
        LS1.main(file, time, seed, alg)
    elif alg == 'LS2':
        LS2.main(file, time, seed, alg)
    elif alg == 'BnB':
        BnB.main(file, time, seed, alg)

    else:
        print('Error! Alg should be one of [BnB|Approx|LS1|LS2]')

    print('...done!')

if __name__ == '__main__':
    main()