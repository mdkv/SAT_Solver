import os

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
        values = []

        for key in variables: #Get all the 'filled in' positions
            if variables[key] == True:
                values.append(key)


        with open(tail+ '.out.txt', 'w') as f:
            for key in values:
                f.write(str(key) + ' 0\n')

    else: #If the cnf can't be satisfied than create an empty file
        with open(tail + '.out.txt', 'w') as f:
            f.write()

    f.close()