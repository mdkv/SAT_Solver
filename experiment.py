from sudoku_utils import convert_to_dimacs, initialize_sudoku
from heuristic_utils import count_pairs
from cnf_utils import read_constraints, create_dict
from algorithms import dpll, mrv
import time
import collections

PATH_TO_CONSTRAINTS = 'sudoku-rules.txt'

def run_experiment(path):

    results = [] #Here are the time, number of evaluations an backtracks appended to
    num_sudoku = 1 #Keep track of the number of sudoku's

    sudokus = convert_to_dimacs(path)
    print(sudokus[0])

    with open('dpll.txt', 'w') as f:

        for sudoku in sudokus:

            if num_sudoku > 10:
                break

            print("Trying to solve sudoku: {}".format(num_sudoku))
            num_pairs = count_pairs(sudoku)

            cnf = read_constraints(PATH_TO_CONSTRAINTS)
            variables = create_dict(cnf)

            t0 = time.time()
            cnf, variables = initialize_sudoku(cnf, variables, sudoku)
            #mrv(variables)


            satisfiable, current_variables = dpll(cnf, variables, '-S1')

            t1 = time.time()
            runtime = t1-t0

            f.write('Sudoku {} : {}     Pairs: {}       Time: {:.4f}\n'.format(num_sudoku, satisfiable, num_pairs, runtime ))
            num_sudoku +=1


    f.close()