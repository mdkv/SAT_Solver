from copy import deepcopy
from statistics import mode
import time
import os

PATH_TO_CONSTRAINTS = 'sudoku-rules.txt'
PATH_TO_SUDOKU = 'sudoku-example.txt'

def read_constraints(path):

    constraints = []
    lines = open(path).readlines()
    for line in lines:

        if line.startswith("c") or line.startswith("p"): #Skip if it is a comment or info
            continue


        clause = line.split(" ") #Split on whitespace
        clause.pop() # Remove last element

        clause = list(map(int, clause)) #Convert to integers
        constraints.append(clause)

    return constraints

def read_sudoku(path):

    given_sudoku = []
    lines = open(path).readlines()
    for line in lines:

        if line.startswith("c") or line.startswith("p"): #Skip if it is a comment or info
            continue
        position = line.split(" ") #Split on whitespace
        position.pop() # Remove last element

        position = list(map(int, position)) #Convert to integers
        given_sudoku.append(position)

    return given_sudoku

def create_dict(constraints):

    variables = dict()

    for clause in constraints: #Loop through the clauses
        for literal in clause: #Loop through the literals within the clause
            key = abs(literal)
            variables[key] = None #Initialize the key

    return variables

def remove_redundant(cnf, literal):

    new_cnf = deepcopy(cnf)

    i = 0
    while i < len(new_cnf):

        if literal in new_cnf[i]: #If there is an exact match, the clause is True, so remove it
            del new_cnf[i]

        else:
            if -literal in new_cnf[i]: #If the negated form is present, the clause can't be satisfied with that literal
                new_cnf[i].remove(-literal)

            i +=1

    return new_cnf


def set_unit_clauses(cnf, variables):

    i = 0 #to do check if i = 0  in one of the if statements can be removed
    while i < len(cnf):
        if len(cnf[i]) == 1: #Length 1 means clause has 1 literal, thus it is a unit claus
            if cnf[i][0] > 0: #If literal is positive, set variable to true
                variables[abs(cnf[i][0])] = True
                cnf = remove_redundant(cnf, cnf[i][0])
                i = 0


            else: #If literal is negated, set variable to false
                variables[abs(cnf[i][0])] = False
                cnf = remove_redundant(cnf, cnf[i][0])
                i =0

        i+=1


    return cnf, variables

def initialize_sudoku(cnf, variables, sudoku):

    for position in sudoku:
        variables[position[0]] = True
        cnf = remove_redundant(cnf, position[0])

    return cnf, variables

def check_satisfiable(cnf):

    if len(cnf) == 0: #All the clauses are removed, thus it is satisfied
        return True

    if len(cnf) !=0: #If there are still clauses in the cnf
        for clause in cnf:
            if len(clause) == 0: #If the clause does exists, and it is empty, it can't be satisfied
                return False

        return 'UNFIN' #Else the cnf can still be satisfied with remaining clauses


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

    # choose literal with lowest J value
    min_literal = min(J, key=J.get)
    return min_literal

def dlcs(cnf, variables):

    current_variables = deepcopy(variables)  # Copy the variables, so previous don't get changed

    cnf, current_variables = set_unit_clauses(cnf, current_variables)  # Check for unit clauses

    satisfiable = check_satisfiable(cnf)
    print(satisfiable)


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
        current_variables[most_frequent] =True
        print("Trying true on " + str(most_frequent) + " pos > neg")
    else:
        current_variables[most_frequent] = False
        print("Trying False on " + str(most_frequent) + " pos < neg")
    new_cnf = remove_redundant(cnf, most_frequent)
    satisfiable, variables = dlcs(new_cnf, current_variables)
    if satisfiable == True:
        return satisfiable, variables

    #Now try False
    if positive > negative:
        current_variables[most_frequent] = False
        print("Trying False on " + str(most_frequent) + " pos > neg")
    else:
        current_variables[most_frequent] = True
        print("Trying true on " + str(most_frequent) + "  pos < neg")
    new_cnf = remove_redundant(cnf, most_frequent)
    return dlcs(new_cnf, current_variables)


def test_dlcs(cnf, current_variables):

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

    for element in cnf_list:
        if element == most_frequent:
            positive +=1
        elif element == -most_frequent:
            negative +=1

    if positive > negative:

        current_variables[most_frequent] = True
        new_cnf = remove_redundant(cnf, most_frequent)
        satisfiable, current_variables = test_dlcs(new_cnf, current_variables)
        if satisfiable == True:
            return satisfiable, current_variables

        current_variables[most_frequent] = False
        new_cnf = remove_redundant(cnf, -most_frequent)
        return test_dlcs(new_cnf, current_variables)


    else:

        current_variables[most_frequent] = False
        new_cnf = remove_redundant(cnf, -most_frequent)
        satisfiable, current_variables = test_dlcs(new_cnf, current_variables)
        if satisfiable == True:
            return satisfiable, current_variables

        current_variables[most_frequent] = True
        new_cnf = remove_redundant(cnf, most_frequent)
        return test_dlcs(new_cnf, current_variables)





def dpll(cnf, variables):

    current_variables = deepcopy(variables)  # Copy the variables, so previous don't get changed

    cnf, current_variables = set_unit_clauses(cnf, current_variables)  # Check for unit clauses

    satisfiable = check_satisfiable(cnf)

    # If this returns either True or False return that value back and either stop or try False. Else try next literal T
    if satisfiable != "UNFIN":
        return satisfiable, current_variables

    # Pick the first variable which is not set
    # Code from: https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/
    key_list = list(current_variables.keys()) #Get all the keys
    val_list = list(current_variables.values()) #Get all the values
    index = val_list.index(None) #Get the index of the first unset variable
    position = key_list[index]
    print(position)


    #position = jeroslow_wang(cnf, variables)


    #First try True
    current_variables[position] = True
    new_cnf = remove_redundant(cnf, position)
    satisfiable, variables = dpll(new_cnf, current_variables)
    if satisfiable == True:
        return satisfiable, variables

    #Now try False, hence the negated position
    current_variables[position] = False
    new_cnf = remove_redundant(cnf, -position)
    return dpll(new_cnf, current_variables)

def print_sudkoku(variables):

    values = []
    for key in variables:
        if variables[key] == True:
            values.append(key)

    values.sort()

    i = 1
    for position in values:
        print(str(position%10) + " ", end=" ")
        if i%3 ==0:
            print("|", end= " ")
        if i%9 ==0:
            print("\n")
        if i%27 == 0:
            print("-------------------------------------")
        i+=1

def create_output(variables, path):

    values = []

    for key in variables: #Get all the 'filled in' positions
        if variables[key] == True:
            values.append(key)

    head, tail = os.path.split(path)
    tail = tail.split('.')[0] #The first element is the name, the second element is the extension

    with open(tail+ '.out.txt', 'w') as f:
        for key in values:
            f.write(str(key) + ' 0\n')

    f.close()


if __name__ == '__main__':
    create_output()
    t0 = time.time()
    cnf = read_constraints(PATH_TO_CONSTRAINTS)
    sudoku = read_sudoku(PATH_TO_SUDOKU)
    variables = create_dict(cnf)
    cnf, variables = initialize_sudoku(cnf, variables, sudoku)
    satisfiable, current_variables = dpll(cnf,variables)
    #satisfiable, current_variables = dlcs(cnf, variables)
    #satisfiable, current_variables = test_dlcs(cnf, variables)

    print("SAT: " + str(satisfiable))
    print_sudkoku(current_variables)
    t1 = time.time()
    print(("Total time: " + str(t1-t0)))






