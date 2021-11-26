import time
import os
import sys
from cnf_utils import read_constraints, create_dict, read_dimacs, create_output, read_total
from sudoku_utils import initialize_sudoku, print_sudkoku, convert_to_dimacs
from heuristic_utils import count_pairs
from experiment import run_experiment
from algorithms import Algorithms


PATH_TO_CONSTRAINTS = 'sudoku-rules.txt'
PATH_TO_SUDOKU = 'sudoku-example.txt'


if __name__ == '__main__':

    arg = sys.argv

    #Run experiment only takes ... format!
    #run_experiment('Sudoku/top2365.sdk.txt', arg[1])

    args = sys.argv #arg[0] = scriptname, arg[1]= = -S algo number, arg[2] = sudoku name
    cnf, given = read_total(args[2])
    variables = create_dict(cnf)
    cnf, variables = initialize_sudoku(cnf, variables, given)

    algo = Algorithms()
    satisfiable, current_variables = algo.dpll(cnf, variables, args[1])

    create_output(current_variables, args[2], satisfiable)