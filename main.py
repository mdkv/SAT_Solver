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
    print("here at unit")

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


def dpll(cnf, variables):
    print("here")

    current_variables = deepcopy(variables)  # Copy the variables, so previous don't get changed

    new_cnf, current_variables = set_unit_clauses(cnf, current_variables)  # Check for unit clauses

    satisfiable = check_satisfiable(cnf)
    #print(satisfiable)

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


    #First try True
    current_variables[position] = True
    new_cnf = remove_redundant(cnf, position)
    satisfiable, variables = dpll(new_cnf, variables)
    if satisfiable == True:
        print("Trying True on: " + str(position))
        return satisfiable, variables

    #Now try False, hence the negated position
    current_variables[position] = False
    new_cnf = remove_redundant(cnf, -position)
    print("Trying false on: " + str(position))
    return dpll(new_cnf, variables)



if __name__ == '__main__':
    cnf = read_constraints(PATH_TO_CONSTRAINTS)
    sudoku = read_sudoku(PATH_TO_SUDOKU)
    variables = create_dict(cnf)
    cnf, variables = initialize_sudoku(cnf, variables, sudoku)
    satisfiable, current_variables = dpll(cnf,variables)
    print("SAT: " + str(satisfiable))
    print(current_variables)
