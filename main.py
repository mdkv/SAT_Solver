import time
import os
import sys
from cnf_utils import read_constraints, create_dict, read_dimacs, create_output
from sudoku_utils import initialize_sudoku, print_sudkoku, convert_to_dimacs
from heuristic_utils import count_pairs
from experiment import run_experiment
from algorithms import Algorithms


PATH_TO_CONSTRAINTS = 'sudoku-rules.txt'
PATH_TO_SUDOKU = 'sudoku-example.txt'


if __name__ == '__main__':

    #Run experiment only takes ... format!
    run_experiment('Sudoku/top2365.sdk.txt', '-S3')

    '''
    TODO: Add here code to test with file (rules+sudoku)
    
    - Split rules + sudoku
    - Sudoku in ... format or dimacs?
    

    #args = sys.argv #arg[0] = scriptname, arg[1]= = -S algo number, arg[2] = sudoku name
    args = ['', '-S1', 'sudoku-example.txt']


    cnf = read_constraints(PATH_TO_CONSTRAINTS)
    sudoku = read_sudoku(args[2])
    variables = create_dict(cnf)
    cnf, variables = initialize_sudoku(cnf, variables, sudoku)

    if args[1] == '-S3':
        satisfiable, current_variables = dlcs(cnf, variables)

    else:
        satisfiable, current_variables = dpll(cnf,variables, args[1])

    print("SAT: " + str(satisfiable))
    print_sudkoku(current_variables)

    #create_output(current_variables, args[2], satisfiable)



'''


