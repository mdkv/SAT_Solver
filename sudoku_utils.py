from heuristic_utils import remove_redundant

def read_sudoku(path):

    given_sudoku = []
    lines = open(path).readlines()
    for line in lines:

        if line.startswith("c") or line.startswith("p"): #Skip if it is a comment or info
            continue
        position = line.split(" ") #Split on whitespace
        position.pop() # Remove last element

        position = list(map(int, position)) #Convert to integers
        given_sudoku.append(position[0])

    return given_sudoku


def initialize_sudoku(cnf, variables, sudoku):

    for position in sudoku:
        variables[position] = True
        cnf = remove_redundant(cnf, position)

    return cnf, variables


def convert_to_dimacs(filename, size = 9):

    collection = []# Here are all the created sudokus added to

    with open(filename) as f: #Open the sudoku file in ..... format

        lines = f.readlines() # Expected that every line is one sudoku

        for line in lines:
            sudoku = []
            row = 0
            column = 0

            for i in range(len(line)):
                if i % size ==0: # if it reached the end of the row
                    row +=1
                    column = 1
                if line[i] != '.' and line[i] != '\n': #Skip dots and the end of the line
                    position = ((row *100)+ (column*10) + int(line[i])) # *100: for row, *10 for column + number
                    sudoku.append(position)
                column = column + 1

            collection.append(sudoku)

        return collection


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