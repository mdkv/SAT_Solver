from sudoku_utils import convert_to_dimacs, initialize_sudoku
from heuristic_utils import count_pairs
from cnf_utils import read_constraints, create_dict, read_dimacs
from algorithms import Algorithms
import time
import csv
import os

PATH_TO_CONSTRAINTS = 'sudoku-rules.txt'

def run_experiment(path, strategy):

    header= ['Number', 'SAT', 'Pairs', 'Evals', 'Backtracks', 'Runtime']
    data = [] #Here are the time, number of evaluations an backtracks appended to
    num_sudoku = 1 #Keep track of the number of sudoku's

    head, tail = os.path.split(path)
    tail = tail.split('.')[0] #The first element is the name, the second element is the extension

    sudokus = convert_to_dimacs(path)

    with open(tail+'_logs_'+ strategy + '.txt', 'w') as f:
    #with open('removethis.txt', 'w') as f:

        for sudoku in sudokus:

            if num_sudoku > 1000:
                break

            print("Trying to solve sudoku: {}".format(num_sudoku))
            num_pairs = count_pairs(sudoku)

            cnf = read_constraints(PATH_TO_CONSTRAINTS)
            variables = create_dict(cnf)

            algo = Algorithms()

            t0 = time.time()
            cnf, variables = initialize_sudoku(cnf, variables, sudoku)
            satisfiable, current_variables = algo.dpll(cnf, variables, strategy)
            print("Number of evals: {} , backtracks: {}".format(algo.num_evaluations, algo.backtracks))
            t1 = time.time()
            runtime = t1-t0
            data.append([num_sudoku, satisfiable, num_pairs, algo.num_evaluations, algo.backtracks, runtime])
            f.write('Sudoku {} : {}     Pairs: {}       evals: {}       backtracks: {}       Time: {:.4f}\n'.format(num_sudoku, satisfiable, num_pairs, algo.num_evaluations, algo.backtracks, runtime ))
            num_sudoku +=1


    f.close()

    with open(tail+'_output_' + strategy + '.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

    f.close()