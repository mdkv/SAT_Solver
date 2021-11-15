from copy import deepcopy

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

def remove_redundant(cnf, literals):

    new_cnf = deepcopy(cnf)

    num_deleted = 0 #This keeps track of how many clauses are deleted, so that index is adjusted in new_cnf

    for literal in literals:
        for i in range(len(cnf)):

            if literal in cnf[i]: #If there is an exact match, the clause is True, so remove it
                new_cnf.pop(i - num_deleted)
                num_deleted +=1

            elif -literal in cnf[i]: #If the negated form is present, the clause can't be satisfied with that literal
                new_cnf[i-num_deleted].remove(-literal)


    return new_cnf


def set_unit_clauses(cnf, variables):

    units = []

    for i in range(len(cnf)):
        if len(cnf[i]) == 1: #Length 1 means clause has 1 literal, thus it is a unit clause
            if cnf[i][0] > 0: #If literal is positive, set variable to true
                variables[abs(cnf[i][0])] = True

            else: #If literal is negated, set variable to false
                variables[abs(cnf[i][0])] = False

            units.append(cnf[i][0])


    cnf = remove_redundant(cnf, units)


    return cnf, variables

def set_initial_sudoku(variables, sudoku):

    for position in sudoku:
        variables[position[0]] = True

    return variables

def check_satisfiable(cnf):

    if len(cnf) == 0: #All the clauses are removed, thus it is satisfied
        return 'SAT'

    if len(cnf) !=0: #If there are still clauses in the cnf
        print("here")
        for clause in cnf:
            if len(clause) == 0: #If the clause does exists, and it is empty, it can't be satisfied
                return 'UNSAT'

        return 'UNFIN' #Else the cnf can still be satisfied with remaining clauses


def dpll(cnf, variables):

    #Pick the first variable which is not set
    #Code from: https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/


    key_list = list(variables.keys()) #Get all the keys
    val_list = list(variables.values()) #Get all the values
    position = val_list.index(None) #Get the index of the first unset variable


    variables[position] = True #First try True

    cnf = remove_redundant(cnf, key)









if __name__ == '__main__':
    cnf = read_constraints(PATH_TO_CONSTRAINTS)
    sudoku = read_sudoku(PATH_TO_SUDOKU)
    variables = create_dict(cnf)
    variables = set_initial_sudoku(variables, sudoku)
    cnf, variables = set_unit_clauses(cnf, variables)
    dpll(cnf,variables)
