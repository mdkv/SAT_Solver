import sys
from cnf_utils import create_dict, create_output, read_total
from sudoku_utils import initialize_sudoku
from experiment import run_experiment
from algorithms import Algorithms


if __name__ == '__main__':

    args = sys.argv  # arg[0] = scriptname, arg[1]= = -S algo number, arg[2] = sudoku name
    #Run experiment only takes ... format!
    #run_experiment('Sudoku/top2365.sdk.txt', args[1])

    cnf, given = read_total(args[2])
    variables = create_dict(cnf)
    cnf, variables = initialize_sudoku(cnf, variables, given)

    algo = Algorithms()
    satisfiable, current_variables = algo.dpll(cnf, variables, args[1])

    create_output(current_variables, args[2], satisfiable)