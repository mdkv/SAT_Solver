import time
import os
import sys
from algorithms import dlcs, dpll
from cnf_utils import read_constraints, create_dict
from sudoku_utils import read_sudoku, initialize_sudoku, print_sudkoku, convert_to_dimacs
from heuristic_utils import count_pairs


PATH_TO_CONSTRAINTS = 'sudoku-rules.txt'
PATH_TO_SUDOKU = 'sudoku-example.txt'


if __name__ == '__main__':
    new_sudokus = convert_to_dimacs('Sudoku/1000_sudokus.txt')
    count_pairs(new_sudokus[0])


    #args = sys.argv #arg[0] = scriptname, arg[1]= = -S algo number, arg[2] = sudoku name
    args = ['', '-S1', 'sudoku-example.txt']

    t0 = time.time()

    cnf = read_constraints(PATH_TO_CONSTRAINTS)
    sudoku = read_sudoku(args[2])
    variables = create_dict(cnf)
    cnf, variables = initialize_sudoku(cnf, variables, sudoku)


    if args[1] == '-S3':
        satisfiable, current_variables = dlcs(cnf, variables)

    else:
        satisfiable, current_variables = dpll(cnf,variables, args[1])

    t1 = time.time()
    print(("Total time: " + str(t1-t0)))

    print("SAT: " + str(satisfiable))
    print_sudkoku(current_variables)

    #create_output(current_variables, args[2], satisfiable)






