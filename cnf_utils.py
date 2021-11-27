import os

def read_dimacs(path):

    given_dimacs = []
    lines = open(path).readlines()
    for line in lines:

        if line.startswith("c") or line.startswith("p"): #Skip if it is a comment or info
            continue
        position = line.split(" ") #Split on whitespace
        position.pop() # Remove last element

        position = list(map(int, position)) #Convert to integers
        given_dimacs.append(position[0])

    return given_dimacs


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


def read_total(path):
    lines = open(path).readlines()
    constraints = []
    given_dimacs = []

    for line in lines:
        if line.startswith("c") or line.startswith("p"):
            continue

        clause = line.split(" ")
        clause.pop()

        clause = list(map(int, clause))

        if len(clause) == 1:
            given_dimacs.append(clause[0])
        else:
            constraints.append(clause)

    return constraints, given_dimacs


def create_dict(constraints):

    variables = dict()

    for clause in constraints: #Loop through the clauses
        for literal in clause: #Loop through the literals within the clause
            key = abs(literal)
            variables[key] = None #Initialize the key

    return variables


def create_output(variables, path, satisfiable):

    head, tail = os.path.split(path)
    tail = tail.split('.')[0] #The first element is the name, the second element is the extension

    if satisfiable == True:

        with open(tail+ '.out', 'w') as f:
            for key, value in variables.items():
                if value == False:
                    key = -key #If the value is set to false, negate the key
                f.write(str(key) + ' 0\n')

    else: #If the cnf can't be satisfied than create an empty file
        with open(tail + '.out', 'w') as f:
            f.write('')

    f.close()