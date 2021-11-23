from copy import deepcopy

def count_pairs(sudoku):
    sudoku = list(map(str, sudoku)) #Convert to string so individual positions can be accessed

    row_list = []
    col_list = []

    pairs = 0

    for position in sudoku: #Get all the rows and the columns
        row_list.append(int(position[0]))
        col_list.append(int(position[1]))


    for i in range(1, 10):
        row_count = row_list.count(i)
        col_count = col_list.count(i)

        if row_count > 1:
            pairs += row_count

        if col_count > 1:
            pairs += col_count

    print("Number of pairs: " + str(pairs))



def check_satisfiable(cnf):

    if len(cnf) == 0: #All the clauses are removed, thus it is satisfied
        return True

    if len(cnf) !=0: #If there are still clauses in the cnf
        for clause in cnf:
            if len(clause) == 0: #If the clause does exists, and it is empty, it can't be satisfied
                return False

        return 'UNFIN' #Else the cnf can still be satisfied with remaining clauses

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