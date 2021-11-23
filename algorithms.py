from copy import deepcopy
from statistics import mode
from heuristic_utils import remove_redundant, set_unit_clauses, check_satisfiable


def dlcs(cnf, variables):

    current_variables = deepcopy(variables)  # Copy the variables, so previous don't get changed

    cnf, current_variables = set_unit_clauses(cnf, current_variables)  # Check for unit clauses

    satisfiable = check_satisfiable(cnf)

    # If this returns either True or False return that value back and either stop or try False. Else try next literal T
    if satisfiable != "UNFIN":
        return satisfiable, current_variables


    cnf_list = []
    positive = 0
    negative = 0

    for row in cnf:
        for element in row:
            cnf_list.append(element)

    absolute_list = []

    for element in cnf_list:
        absolute_list.append(abs(element))

    most_frequent = mode(absolute_list)
    print(most_frequent)

    for element in cnf_list:
        if element == most_frequent:
            positive +=1
        elif element == -most_frequent:
            negative +=1

    if positive > negative:
        current_variables[most_frequent] = True
        new_cnf = remove_redundant(cnf, most_frequent)
        satisfiable, variables = dlcs(new_cnf, current_variables)
        if satisfiable == True:
            return satisfiable, variables

        current_variables[most_frequent] = False
        new_cnf = remove_redundant(cnf, -most_frequent)
        return dlcs(new_cnf, current_variables)


    else:
        current_variables[most_frequent] = False
        new_cnf = remove_redundant(cnf, -most_frequent)
        satisfiable, variables = dlcs(new_cnf, current_variables)
        if satisfiable == True:
            return satisfiable, variables

        current_variables[most_frequent] = True
        new_cnf = remove_redundant(cnf, most_frequent)
        return dlcs(new_cnf, current_variables)


def jeroslow_wang(cnf, variables):
    '''
    Uses the Jeroslow-Wang method (one-sided) to pick the next literal that has the lowest J(l) value.
    '''

    # save all literal scores in a dict
    J = {}

    # loop over each clause
    for clause in cnf:

        # look at each literal within the clause
        for literal in clause:

            # find literal that is not negated and has a None-value
            if literal > 0 and literal in variables and variables[literal] == None:

                # get the J-value of that literal
                J_literal = 2 ** -(abs(len(clause))) # TODO: waarom absoluut-strepen in formule, lengte is nooit <0?

                # save in dictionary
                if literal not in J:
                    J[literal] = J_literal

                else:
                    J[literal] += J_literal

    # choose literal with highest J value
    max_literal = max(J, key=J.get)
    return max_literal


def dpll(cnf, variables, algo):

    current_variables = deepcopy(variables)  # Copy the variables, so previous don't get changed

    cnf, current_variables = set_unit_clauses(cnf, current_variables)  # Check for unit clauses

    satisfiable = check_satisfiable(cnf)

    # If this returns either True or False return that value back and either stop or try False. Else try next literal T
    if satisfiable != "UNFIN":
        return satisfiable, current_variables

    if algo == '-S1':
        # Pick the first variable which is not set
        # Code from: https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/
        key_list = list(current_variables.keys()) #Get all the keys
        val_list = list(current_variables.values()) #Get all the values
        index = val_list.index(None) #Get the index of the first unset variable
        position = key_list[index]

    elif algo == '-S2':
        position = jeroslow_wang(cnf, variables)


    #First try True
    current_variables[position] = True
    new_cnf = remove_redundant(cnf, position)
    satisfiable, variables = dpll(new_cnf, current_variables, algo)
    if satisfiable == True:
        return satisfiable, variables

    #Now try False, hence the negated position
    current_variables[position] = False
    new_cnf = remove_redundant(cnf, -position)
    return dpll(new_cnf, current_variables, algo)